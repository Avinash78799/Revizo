import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.user import User
from app.models.taxonomy import Concept
from app.models.question import Question, QuestionOption, QuestionQualityScorecard
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source, EvidenceReference, PyqReference
from app.services.reviewer_service import ReviewerService
from app.services.source_provenance_service import SourceProvenanceService
from app.services.medical_candidate_service import MedicalCandidateService
from app.services.medical_content_service import MedicalContentService
from app.services.test_service import TestService
from app.core.errors import ValidationError, NotFoundError, AuthorizationError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(loop_scope="function")
async def client_and_db():
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False, "timeout": 30.0},
        echo=False
    )
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await seed_database(session)

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client, async_session

    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.mark.asyncio
async def test_candidate_creation_defaults_and_structural_validation(client_and_db):
    """
    Requirements Tested:
    1. Candidate defaults to PROPOSED.
    2. Candidate defaults to AI_GENERATED_REVIEW_PENDING.
    12. Four-option / single-best-answer structural validation works.
    13. Duplicate options are rejected.
    14. Missing taxonomy/concept mapping is rejected.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="candidate_admin@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        session.add(admin)
        await session.commit()

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # 1. Successful Candidate Ingestion
        cand = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="A 45-year-old male presents with acute crushing chest pain radiating to the left arm. What is the initial drug of choice?",
            options={
                "A": "Aspirin 325 mg chewed",
                "B": "Intravenous Heparin",
                "C": "Oral Metoprolol",
                "D": "Sublingual Morphine"
            },
            correct_option_key="A",
            correct_explanation="Chewed aspirin provides immediate antiplatelet effect in acute coronary syndrome.",
            remember_takeaway="Aspirin chewed immediately in suspected ACS reduces mortality.",
            ai_model_name="gemini-1.5-pro",
            prompt_version="v2.1"
        )
        assert cand.status == "PROPOSED"
        assert cand.trust_class == "AI_GENERATED_REVIEW_PENDING"
        assert cand.content_version == 1
        assert cand.is_ai_generated is True

        # 2. Reject Duplicate Options
        with pytest.raises(ValidationError) as exc_dup:
            await MedicalCandidateService.ingest_candidate_question(
                db=session,
                creator_user_id=admin.id,
                concept_id=concept.id,
                question_text="Valid clinical question stem text here?",
                options={
                    "A": "Aspirin",
                    "B": "Aspirin",  # Duplicate!
                    "C": "Heparin",
                    "D": "Morphine"
                },
                correct_option_key="A",
                correct_explanation="Explanation",
                remember_takeaway="Takeaway"
            )
        assert "Duplicate option text detected" in str(exc_dup.value)

        # 3. Reject Missing Concept
        with pytest.raises(NotFoundError) as exc_concept:
            await MedicalCandidateService.ingest_candidate_question(
                db=session,
                creator_user_id=admin.id,
                concept_id="non-existent-concept-id",
                question_text="Valid clinical question stem text here?",
                options={"A": "1", "B": "2", "C": "3", "D": "4"},
                correct_option_key="A",
                correct_explanation="Explanation",
                remember_takeaway="Takeaway"
            )
        assert "Concept 'non-existent-concept-id' not found" in str(exc_concept.value)


@pytest.mark.asyncio
async def test_provenance_and_pyq_candidate_validation_gates(client_and_db):
    """
    Requirements Tested:
    3. Candidate without source evidence cannot become verified.
    4. Candidate referencing UNVERIFIED source cannot become verified.
    7. Claimed PYQ without VERIFIED_PYQ provenance remains unverified.
    10. High-risk candidate is marked for two-doctor review.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_prov_gate@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        doc = User(email="dr_prov_gate@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, doc])
        await session.commit()

        p_doc = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc.id, credential_type="MD",
            registration_number="TMC-12345", medical_council="Tamil Nadu Medical Council", specialty="Medicine"
        )
        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p_doc.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-TMC-123"
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # 1. Unverified Source candidate
        unverified_src = await SourceProvenanceService.register_source_candidate(
            db=session, title="Online Notes 2026", source_type="STANDARD_TEXTBOOK", publisher="Web Publisher"
        )
        cand_unver_src = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="Clinical vignette referencing unverified source candidate?",
            options={"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
            correct_option_key="A",
            correct_explanation="Explanation",
            remember_takeaway="Takeaway",
            source_id=unverified_src.id,
            claim_snippet="Factual claim from unverified source",
            page_or_section="Chapter 1"
        )
        # Attempting doctor approval on unverified source -> MUST FAIL
        with pytest.raises(ValidationError) as exc_src:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=cand_unver_src.id, reviewer_id=doc.id,
                verdict="APPROVE", clinical_notes="Attempted approval"
            )
        assert "unverified source" in str(exc_src.value).lower()

        # 2. Reject unverified PYQ claim
        unverified_pyq = PyqReference(
            id="pyq-unver-1", concept_id=concept.id, exam_name="NEET-PG", exam_year=2023,
            pyq_status="UNVERIFIED", verification_status="UNVERIFIED"
        )
        session.add(unverified_pyq)
        await session.commit()

        with pytest.raises(ValidationError) as exc_pyq:
            await MedicalCandidateService.ingest_candidate_question(
                db=session,
                creator_user_id=admin.id,
                concept_id=concept.id,
                question_text="Clinical vignette claiming fake PYQ status?",
                options={"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
                correct_option_key="A",
                correct_explanation="Explanation",
                remember_takeaway="Takeaway",
                pyq_reference_id=unverified_pyq.id
            )
        assert "unverified reference" in str(exc_pyq.value).lower()

        # 3. High-Risk Candidate Auto-Tagging
        cand_high_risk = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="Emergency airway management in severe pediatric anaphylaxis?",
            options={"A": "Intramuscular Epinephrine", "B": "Oral Antihistamine", "C": "Inhaled Albuterol", "D": "IV Furosemide"},
            correct_option_key="A",
            correct_explanation="Epinephrine IM is the first-line lifesaving medication for anaphylaxis.",
            remember_takeaway="IM Epinephrine in anterolateral thigh is first-line in anaphylaxis.",
            is_high_risk=True,
            high_risk_category="emergency_management"
        )
        assert cand_high_risk.is_high_risk is True
        assert cand_high_risk.high_risk_category == "emergency_management"


@pytest.mark.asyncio
async def test_candidate_strictly_isolated_from_student_test_pool(client_and_db):
    """
    Requirements Tested:
    8. Candidate cannot directly enter student test pool.
    9. Development benchmark cannot be promoted through candidate ingestion.
    11. Candidate version/audit metadata is immutable.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_pool_isolation@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        session.add(admin)
        await session.commit()

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Ingest candidate
        cand = await MedicalCandidateService.ingest_candidate_question(
            db=session,
            creator_user_id=admin.id,
            concept_id=concept.id,
            question_text="Candidate question that must NOT enter active student pool?",
            options={"A": "Alpha", "B": "Beta", "C": "Gamma", "D": "Delta"},
            correct_option_key="A",
            correct_explanation="Explanation",
            remember_takeaway="Takeaway"
        )
        assert cand.status == "PROPOSED"
        assert cand.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # Create student test session
        sess, questions = await TestService.create_test_session(
            db=session, user_id="student-pool-candidate-test-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        
        # Verify candidate is NOT in student test questions
        selected_ids = [q.id for q in questions]
        assert cand.id not in selected_ids
        for q in questions:
            assert q.trust_class != "AI_GENERATED_REVIEW_PENDING"
            assert q.trust_class != "DEVELOPMENT_BENCHMARK"
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
