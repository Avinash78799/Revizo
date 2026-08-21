import pytest
import pytest_asyncio
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept, Topic, Chapter, Subject, SyllabusRegistry
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQuarantineRegistry
from app.models.source import Source, PyqReference, SourceConflict
from app.models.reviewer import MedicalReviewerProfile
from app.models.user import User
from app.services.medical_content_service import MedicalContentService
from app.services.content_gap_engine import ContentGapEngine
from app.services.test_service import TestService
from app.core.errors import ValidationError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(loop_scope="function")
async def client_and_db():
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
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
async def test_two_person_review_enforcement_for_high_risk_content(client_and_db):
    """
    Acceptance:
    1. High-risk content (drug dosing, emergency management, pregnancy safety, contraindications)
       requires approval by TWO distinct medical doctors.
    2. 1 approval leaves status as REVIEW_PENDING.
    3. Same reviewer attempting to approve twice is rejected.
    4. 2nd distinct reviewer approval promotes to APPROVED / VERIFIED_CORE_QUESTION.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create high-risk question
        c_stmt = select(Concept).limit(1)
        res_c = await session.execute(c_stmt)
        concept = res_c.scalars().first()

        # Seed Verified Source and Doctor Profiles
        src = Source(title="Harrison Principles of Internal Medicine 21st Ed", source_type="STANDARD_TEXTBOOK", verification_status="VERIFIED")
        u1 = User(id="doctor-reviewer-1", email="doc1@aiims.edu", hashed_password="pw", role="reviewer")
        p1 = MedicalReviewerProfile(user_id="doctor-reviewer-1", credential_type="MD", specialty="OBGYN", verification_status="VERIFIED", active_status=True)
        u2 = User(id="doctor-reviewer-2", email="doc2@aiims.edu", hashed_password="pw", role="reviewer")
        p2 = MedicalReviewerProfile(user_id="doctor-reviewer-2", credential_type="MD", specialty="Cardiology", verification_status="VERIFIED", active_status=True)
        session.add_all([src, u1, p1, u2, p2])

        q = Question(
            concept_id=concept.id,
            source_id=src.id,
            question_text="A pregnant patient in 3rd trimester presents with severe hypertensive emergency. Which drug is contraindicated?",
            correct_explanation="ACE inhibitors and ARBs are strictly fetotoxic in 2nd and 3rd trimesters.",
            remember_takeaway="Avoid ACE-I/ARBs in pregnancy due to fetal renal dysgenesis.",
            is_high_risk=True,
            high_risk_category="pregnancy_safety",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-high-risk-1"
        )
        session.add(q)
        await session.commit()
        await session.refresh(q)

        # Doctor 1 Approval
        res1 = await MedicalContentService.perform_medical_review(
            db=session,
            question_id=q.id,
            reviewer_id="doctor-reviewer-1",
            verdict="APPROVE",
            clinical_notes="Medically accurate pregnancy contraindication question."
        )
        assert res1["status"] == "REVIEW_PENDING"
        assert res1["trust_class"] == "AI_GENERATED_REVIEW_PENDING"
        assert res1["first_reviewer_id"] == "doctor-reviewer-1"
        assert res1["second_reviewer_id"] is None

        # Same Doctor attempting second approval fails
        with pytest.raises(ValidationError) as exc:
            await MedicalContentService.perform_medical_review(
                db=session,
                question_id=q.id,
                reviewer_id="doctor-reviewer-1",
                verdict="APPROVE",
                clinical_notes="Approving again"
            )
        assert "two distinct" in str(exc.value).lower()

        # Doctor 2 Approval (Distinct reviewer)
        res2 = await MedicalContentService.perform_medical_review(
            db=session,
            question_id=q.id,
            reviewer_id="doctor-reviewer-2",
            verdict="APPROVE",
            clinical_notes="Second doctor verification complete. Approved for core pool."
        )
        assert res2["status"] == "APPROVED"
        assert res2["trust_class"] == "VERIFIED_CORE_QUESTION"
        assert res2["second_reviewer_id"] == "doctor-reviewer-2"

@pytest.mark.asyncio
async def test_verified_pyq_provenance_verification(client_and_db):
    """
    Acceptance:
    1. Unverified PYQ cannot display as VERIFIED_PYQ.
    2. Independent verification promotes PYQ status to VERIFIED_PYQ and upgrades trust class.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        res_c = await session.execute(c_stmt)
        concept = res_c.scalars().first()

        # Create unverified PYQ reference
        pyq_ref = PyqReference(
            concept_id=concept.id,
            exam_name="NEET-PG",
            exam_year=2024,
            exam_session="Regular",
            question_identifier="NEET-2024-Q42",
            pyq_status="UNVERIFIED",
            verification_status="UNVERIFIED"
        )
        session.add(pyq_ref)
        await session.commit()
        await session.refresh(pyq_ref)

        # Independent human verification
        res_verify = await MedicalContentService.verify_pyq_provenance(
            db=session,
            pyq_ref_id=pyq_ref.id,
            verifier_id="lead-doctor-audit",
            is_verified=True,
            notes="Cross-verified with official NBE NEET-PG 2024 master paper."
        )
        assert res_verify["verification_status"] == "VERIFIED"
        assert res_verify["pyq_status"] == "VERIFIED_PYQ"

@pytest.mark.asyncio
async def test_source_conflict_detection_and_high_risk_tagging(client_and_db):
    """
    Acceptance:
    When two authoritative guidelines disagree, the system registers a SourceConflict
    and flags concept questions as high-risk source conflicts for medical board review.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Create two sources
        s1 = Source(title="Harrison Principles of Internal Medicine 21st Ed", source_type="STANDARD_TEXTBOOK")
        s2 = Source(title="Goldman-Cecil Medicine 26th Ed", source_type="STANDARD_TEXTBOOK")
        session.add_all([s1, s2])
        await session.commit()

        conflict = await MedicalContentService.register_source_conflict(
            db=session,
            concept_id=concept.id,
            source_a_id=s1.id,
            source_b_id=s2.id,
            conflicting_claim="Discrepancy on first-line drug duration for secondary prevention.",
            specialty="Cardiology"
        )
        assert conflict.status == "REVIEW_REQUIRED"

        # Verify concept questions are flagged as high risk
        stmt_q = select(Question).where(Question.concept_id == concept.id)
        questions = (await session.execute(stmt_q)).scalars().all()
        for q in questions:
            assert q.is_high_risk is True
            assert q.high_risk_category == "source_conflict"

@pytest.mark.asyncio
async def test_content_gap_engine_coverage_matrix(client_and_db):
    """
    Acceptance: ContentGapEngine scans the curriculum and classifies into RED (missing), YELLOW (limited), GREEN (healthy).
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        matrix = await ContentGapEngine.generate_coverage_matrix(session)

        assert "summary" in matrix
        assert "total_concepts" in matrix["summary"]
        assert matrix["summary"]["syllabus_version"] == "neet-pg-nmc-2026-v1.0"
        assert "red_critical_gaps" in matrix
        assert "yellow_limited_gaps" in matrix
        assert "green_coverage" in matrix

@pytest.mark.asyncio
async def test_gold_medical_benchmark_16_categories(client_and_db):
    """
    Acceptance: Verifies all 16 standard gold medical benchmark categories are defined.
    """
    categories = MedicalContentService.GOLD_BENCHMARK_CATEGORIES
    assert len(categories) == 16
    assert "single_best_answer" in categories
    assert "drug_contraindication" in categories
    assert "emergency_management" in categories
    assert "pregnancy_safety" in categories
    assert "hallucinated_citation" in categories
    assert "fake_pyq" in categories
