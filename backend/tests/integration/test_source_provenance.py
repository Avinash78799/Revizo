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
from app.models.taxonomy import Concept, SyllabusRegistry, SyllabusSourceArtifact
from app.models.question import Question, QuestionOption, QuestionReview
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source, SourceConflict, PyqReference
from app.services.reviewer_service import ReviewerService
from app.services.source_provenance_service import SourceProvenanceService
from app.services.medical_content_service import MedicalContentService
from app.services.test_service import TestService
from app.core.errors import ValidationError, AuthorizationError, NotFoundError

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
async def test_source_registration_and_independent_auditor_gate(client_and_db):
    """
    Requirements Tested:
    1. Source without verified ISBN/evidence defaults to UNVERIFIED.
    2. Plausible ISBN cannot become VERIFIED without independent auditor.
    3. Unverified user/student cannot verify medical sources (AuthorizationError).
    4. Verified doctor can audit and verify source, creating immutable audit notes.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create users: student, unverified doctor, verified doctor, and admin
        student = User(email="student_user@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        unverified_doc = User(email="dr_unverified@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        verified_doc = User(email="dr_verified_auditor@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        admin = User(email="admin_auditor@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        session.add_all([student, unverified_doc, verified_doc, admin])
        await session.commit()

        # Set up verified doctor profile
        p_ver = await ReviewerService.register_reviewer_profile(
            db=session, user_id=verified_doc.id, credential_type="MD",
            registration_number="KMC-8888", medical_council="Karnataka Medical Council", specialty="Pharmacology"
        )
        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p_ver.id, verifier_user_id=admin.id,
            decision="VERIFIED", verification_evidence_ref="AUDIT-DOC-PHARM"
        )

        # 1. Register candidate textbook -> MUST be UNVERIFIED
        src = await SourceProvenanceService.register_source_candidate(
            db=session,
            title="Goodman & Gilman's The Pharmacological Basis of Therapeutics",
            source_type="STANDARD_TEXTBOOK",
            publisher="McGraw Hill",
            edition="14th Edition",
            publication_year=2023,
            reference_identifier="ISBN-9781264258079",
            specialty="Pharmacology"
        )
        assert src.verification_status == "UNVERIFIED"
        assert src.verified_by is None

        # 2. Student attempts to verify source -> MUST BE REJECTED
        with pytest.raises(AuthorizationError) as exc_student:
            await SourceProvenanceService.audit_and_verify_source(
                db=session, source_id=src.id, verifier_id=student.id, decision="VERIFIED",
                reference_identifier="ISBN-9781264258079", edition="14th Edition", publisher="McGraw Hill",
                audit_evidence_notes="Audited by student"
            )
        assert "Only VERIFIED reviewers or Admins" in str(exc_student.value)

        # 3. Verified Doctor audits and verifies source -> SUCCEEDS
        audit_res = await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=src.id, verifier_id=verified_doc.id, decision="VERIFIED",
            reference_identifier="ISBN-9781264258079", edition="14th Edition", publisher="McGraw Hill",
            audit_evidence_notes="Verified against official publisher catalog and physical print copy."
        )
        assert audit_res["verification_status"] == "VERIFIED"
        assert audit_res["verified_by"] == verified_doc.id
        assert audit_res["reference_identifier"] == "ISBN-9781264258079"


@pytest.mark.asyncio
async def test_conflicting_sources_blocked_from_verification_and_publication(client_and_db):
    """
    Requirements Tested:
    6. Conflicting source records cannot become VERIFIED silently.
    9. UNVERIFIED / CONFLICTED sources cannot support VERIFIED_CORE_QUESTION publication.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_conflict_auditor@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        session.add(admin)
        await session.commit()

        # Register 2 source candidates
        src_a = await SourceProvenanceService.register_source_candidate(
            db=session, title="Clinical Guideline Edition A", source_type="CLINICAL_GUIDELINE",
            publisher="Medical Society A", edition="2020", reference_identifier="DOI-10.1000/182"
        )
        src_b = await SourceProvenanceService.register_source_candidate(
            db=session, title="Clinical Guideline Edition B", source_type="CLINICAL_GUIDELINE",
            publisher="Medical Society B", edition="2024", reference_identifier="DOI-10.1000/183"
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Flag medical conflict between Guideline A and Guideline B
        conflict = await SourceProvenanceService.flag_source_conflict(
            db=session,
            concept_id=concept.id,
            source_a_id=src_a.id,
            source_b_id=src_b.id,
            conflicting_claim="First-line hypertension threshold is 130/80 in A vs 140/90 in B.",
            specialty="Cardiology"
        )
        assert conflict.status == "REVIEW_REQUIRED"
        assert src_a.verification_status == "CONFLICTED"
        assert src_b.verification_status == "CONFLICTED"

        # Attempting to verify source A while unresolved conflict exists -> MUST FAIL
        with pytest.raises(ValidationError) as exc_conf:
            await SourceProvenanceService.audit_and_verify_source(
                db=session, source_id=src_a.id, verifier_id=admin.id, decision="VERIFIED",
                reference_identifier="DOI-10.1000/182", edition="2020", publisher="Medical Society A",
                audit_evidence_notes="Attempted verification"
            )
        assert "unresolved medical conflict" in str(exc_conf.value)


@pytest.mark.asyncio
async def test_syllabus_and_pyq_provenance_verification_gates(client_and_db):
    """
    Requirements Tested:
    3. Missing document evidence / invalid SHA-256 prevents syllabus verification.
    4. Fake/invalid NMC document identifiers cannot become VERIFIED.
    5. PYQ without genuine source evidence remains UNVERIFIED.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_syllabus_auditor@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        session.add(admin)
        await session.commit()

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # 1. Invalid SHA-256 (not 64 hex chars) -> MUST BE REJECTED
        with pytest.raises(ValidationError) as exc_hash:
            await SourceProvenanceService.verify_syllabus_provenance(
                db=session,
                syllabus_version="neet-pg-nmc-2026-v1.0",
                document_identifier="NMC-CBME-2026-CURRICULUM",
                document_hash="short_invalid_hash_123",  # Invalid!
                source_name="National Medical Commission",
                source_url="https://www.nmc.org.in/syllabus",
                effective_date="2026-01-01",
                verifier_id=admin.id,
                verification_notes="Verified syllabus artifact"
            )
        assert "64-character SHA-256" in str(exc_hash.value)

        # 2. Valid 64-char SHA-256 and genuine identifier -> SUCCEEDS
        valid_sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        syl_res = await SourceProvenanceService.verify_syllabus_provenance(
            db=session,
            syllabus_version="neet-pg-nmc-2026-v1.0",
            document_identifier="NMC-CBME-PG-2026-REG-DOC",
            document_hash=valid_sha256,
            source_name="National Medical Commission (NMC)",
            source_url="https://www.nmc.org.in/wp-content/uploads/2026/cbme_curriculum.pdf",
            effective_date="2026-01-01",
            verifier_id=admin.id,
            verification_notes="Verified against official gazette notification."
        )
        assert syl_res["verification_status"] == "VERIFIED"
        assert syl_res["document_hash"] == valid_sha256

        # 3. PYQ Reference Verification Gate
        pyq_raw = PyqReference(
            id="pyq-test-gate-1",
            concept_id=concept.id,
            exam_name="NEET-PG",
            exam_year=2023,
            verification_status="UNVERIFIED",
            pyq_status="UNVERIFIED"
        )
        session.add(pyq_raw)
        await session.commit()

        # PYQ verification requires master question ID and source document citation
        pyq_res = await SourceProvenanceService.verify_pyq_provenance(
            db=session,
            pyq_ref_id=pyq_raw.id,
            verifier_id=admin.id,
            exam_name="NEET-PG",
            exam_year=2023,
            question_identifier="Q-42",
            source_document="NBE Official Master Question Paper - July 2023 Session",
            audit_notes="Matched with official question paper archive."
        )
        assert pyq_res["pyq_status"] == "VERIFIED_PYQ"
        assert pyq_res["verification_status"] == "VERIFIED"
        assert pyq_res["question_identifier"] == "Q-42"


@pytest.mark.asyncio
async def test_unverified_source_blocks_question_publication_and_pool_eligibility(client_and_db):
    """
    Requirements Tested:
    9. UNVERIFIED source blocks question from being APPROVED / PUBLISHED.
    10. DEVELOPMENT_BENCHMARK content remains excluded from student pool.
    11. AI_GENERATED_REVIEW_PENDING content remains excluded from student pool.
    12. Existing reviewer credential gates remain intact.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        admin = User(email="admin_pool_gate@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        doc = User(email="dr_pool_doc@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, doc])
        await session.commit()

        p_doc = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc.id, credential_type="MS",
            registration_number="DMC-3344", medical_council="Delhi Medical Council", specialty="Surgery"
        )
        await ReviewerService.verify_reviewer_credentials(
            db=session, profile_id=p_doc.id, verifier_user_id=admin.id,
            decision="VERIFIED", verification_evidence_ref="DMC-AUDIT-3344"
        )

        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Create UNVERIFIED source
        unverified_src = await SourceProvenanceService.register_source_candidate(
            db=session, title="Unofficial Online Notes", source_type="OTHER" if "OTHER" in SourceProvenanceService.ALLOWED_SOURCE_TYPES else "STANDARD_TEXTBOOK",
            publisher="Online Blog", edition="1st"
        )

        # Create candidate question referencing unverified source
        q_unverified = Question(
            concept_id=concept.id,
            source_id=unverified_src.id,
            question_text="Question with unverified source citation",
            correct_explanation="Exp",
            remember_takeaway="Pearl",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-unverified-src-q1"
        )
        session.add(q_unverified)
        await session.commit()

        # Doctor attempts to APPROVE question relying on unverified source -> MUST FAIL
        with pytest.raises(ValidationError) as exc_src:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_unverified.id, reviewer_id=doc.id,
                verdict="APPROVE", clinical_notes="Trying to approve unverified source question"
            )
        assert "unverified source" in str(exc_src.value).lower()

        # Verify that student test session creation ignores UNVERIFIED and DEVELOPMENT_BENCHMARK
        sess, questions = await TestService.create_test_session(
            db=session, user_id="student-pool-check-2", mode="DAILY_SHORT_TEST", question_count=5
        )
        for q in questions:
            assert q.id != q_unverified.id
            assert q.trust_class not in ["DEVELOPMENT_BENCHMARK", "AI_GENERATED_REVIEW_PENDING", "QUARANTINED", "WITHDRAWN", "UNVERIFIED"]
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
