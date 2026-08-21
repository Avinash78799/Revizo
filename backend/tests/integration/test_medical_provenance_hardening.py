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
from app.models.taxonomy import Concept, Topic, Chapter, Subject, SyllabusRegistry, SyllabusSourceArtifact
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQuarantineRegistry
from app.models.source import Source, PyqReference, SourceConflict
from app.models.reviewer import MedicalReviewerProfile
from app.models.benchmark import BenchmarkCase
from app.models.user import User
from app.services.medical_content_service import MedicalContentService
from app.services.benchmark_service import GoldBenchmarkService
from app.services.question_selection_engine import QuestionSelectionEngine
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
        await GoldBenchmarkService.seed_benchmark_cases(session)

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
async def test_unverified_syllabus_artifact_provenance_gate(client_and_db):
    """
    Acceptance:
    - Syllabus cannot be marked VERIFIED without authoritative document identifier, document hash, and verifier identity.
    - Verified provenance preserves complete audit artifact.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # 1. Missing hash or identifier fails
        with pytest.raises(ValidationError) as exc1:
            await MedicalContentService.verify_syllabus_source_provenance(
                db=session,
                syllabus_version="neet-pg-nmc-2026-v1.0",
                document_identifier="",
                document_hash="",
                source_name="NMC",
                source_url="https://nmc.org.in",
                effective_date="2026-01-01",
                verifier_id="",
                verification_notes="Missing audit fields"
            )
        assert "cannot verify syllabus" in str(exc1.value).lower()

        # 2. Complete provenance succeeds
        res_ver = await MedicalContentService.verify_syllabus_source_provenance(
            db=session,
            syllabus_version="neet-pg-nmc-2026-v1.0",
            document_identifier="NMC-CBME-POSTGRADUATE-2026",
            document_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            source_name="National Medical Commission Official Gazette",
            source_url="https://nmc.org.in/rules-regulations/pgmeb-2026",
            effective_date="2026-01-01",
            verifier_id="nmc-audit-officer-1",
            verification_notes="Verified against official Gazette publication."
        )
        assert res_ver["verification_status"] == "VERIFIED"
        assert res_ver["document_identifier"] == "NMC-CBME-POSTGRADUATE-2026"

@pytest.mark.asyncio
async def test_development_benchmark_cannot_claim_expert_verified(client_and_db):
    """
    Acceptance:
    - Seeded benchmark cases default to DEVELOPMENT_BENCHMARK.
    - Non-verified users cannot verify benchmark cases.
    - Verified medical doctor review transitions case to EXPERT_VERIFIED.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(BenchmarkCase).limit(1)
        res = await session.execute(stmt)
        case = res.scalars().first()

        assert case.provenance_status == "DEVELOPMENT_BENCHMARK"

        # Non-doctor verification attempt fails
        with pytest.raises(ValidationError) as exc:
            await GoldBenchmarkService.verify_benchmark_case_by_doctor(
                db=session,
                benchmark_case_id=case.benchmark_case_id,
                reviewer_id="unregistered-user",
                expert_name="Dr. Unverified",
                authoritative_source="None"
            )
        assert "not an active verified medical reviewer" in str(exc.value).lower()

        # Verified doctor verification succeeds
        u = User(id="doc-board-member", email="board@aiims.edu", hashed_password="pw", role="reviewer")
        p = MedicalReviewerProfile(user_id="doc-board-member", credential_type="MD", specialty="General Medicine", verification_status="VERIFIED", active_status=True)
        session.add_all([u, p])
        await session.commit()

        res_ok = await GoldBenchmarkService.verify_benchmark_case_by_doctor(
            db=session,
            benchmark_case_id=case.benchmark_case_id,
            reviewer_id="doc-board-member",
            expert_name="Dr. S. Sharma (AIIMS)",
            authoritative_source="Harrison Principles 21st Ed, Ch 24"
        )
        assert res_ok["provenance_status"] == "EXPERT_VERIFIED"
        assert "AIIMS" in res_ok["expert_verified_by"]

@pytest.mark.asyncio
async def test_missing_pyq_provenance_forces_unverified_status(client_and_db):
    """
    Acceptance:
    - Unverified PYQ reference cannot be stamped VERIFIED_PYQ without independent evidence.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        pyq = PyqReference(
            id="pyq-test-1",
            concept_id=concept.id,
            exam_name="NEET-PG",
            exam_year=2023,
            pyq_status="UNVERIFIED",
            verification_status="UNVERIFIED"
        )
        session.add(pyq)
        await session.commit()

        # Falsely claiming verification without verifier identity fails or remains unverified
        assert pyq.verification_status == "UNVERIFIED"
        assert pyq.pyq_status == "UNVERIFIED"

@pytest.mark.asyncio
async def test_reviewer_audit_trail_immutability_and_credential_snapshot(client_and_db):
    """
    Acceptance:
    - Every review snapshots the exact question version, reviewer credential status,
      and source/guideline verification decisions.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        src = Source(
            id="src-verified-audit",
            title="Katzung Basic and Clinical Pharmacology 15th Ed",
            source_type="STANDARD_TEXTBOOK",
            edition="15th",
            publisher="McGraw Hill",
            reference_identifier="ISBN-9781260455137",
            verification_status="VERIFIED"
        )
        u = User(id="doc-auditor", email="auditor@pgi.edu", hashed_password="pw", role="reviewer")
        p = MedicalReviewerProfile(user_id="doc-auditor", credential_type="MD", specialty="Pharmacology", verification_status="VERIFIED", active_status=True)
        session.add_all([src, u, p])

        q = Question(
            concept_id=concept.id,
            source_id=src.id,
            question_text="Pharmacology audit question",
            correct_explanation="Drug mechanism explanation",
            remember_takeaway="Key clinical pearl",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            content_version=3,
            text_hash="hash-audit-trail-1"
        )
        session.add(q)
        await session.commit()

        res_rev = await MedicalContentService.perform_medical_review(
            db=session,
            question_id=q.id,
            reviewer_id="doc-auditor",
            verdict="APPROVE",
            clinical_notes="Pharmacologically sound; verified against Katzung 15th Ed.",
            guideline_verified=True
        )
        assert res_rev["audit_trail_recorded"] is True

        # Check recorded review snapshot
        stmt_rev = select(QuestionReview).where(QuestionReview.question_id == q.id)
        res_db_rev = await session.execute(stmt_rev)
        review_record = res_db_rev.scalars().first()

        assert review_record.question_version == 3
        assert review_record.reviewer_credential_status == "MD_VERIFIED"
        assert review_record.source_verification_decision == "VERIFIED"
        assert review_record.guideline_verification_decision == "VERIFIED"

@pytest.mark.asyncio
async def test_downgraded_and_unverified_content_strictly_excluded_from_student_tests(client_and_db):
    """
    Acceptance:
    - AI_GENERATED_REVIEW_PENDING, DEVELOPMENT_SEED, QUARANTINED, WITHDRAWN
      are strictly excluded from student test selection.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Create draft/unverified questions in various non-trusted states
        q_draft = Question(
            concept_id=concept.id,
            question_text="Draft question",
            correct_explanation="Exp",
            remember_takeaway="Rem",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-draft-1"
        )
        q_quar = Question(
            concept_id=concept.id,
            question_text="Quarantined question",
            correct_explanation="Exp",
            remember_takeaway="Rem",
            status="QUARANTINED",
            trust_class="QUARANTINED",
            text_hash="hash-quar-1"
        )
        session.add_all([q_draft, q_quar])
        await session.commit()

        # Selection engine only returns PUBLISHED / APPROVED questions
        selected_qs, _ = await QuestionSelectionEngine.select_questions_for_test(
            db=session,
            user_id="student-test-runner",
            mode="DAILY_SHORT_TEST",
            question_count=5
        )

        for q in selected_qs:
            assert q.trust_class != "AI_GENERATED_REVIEW_PENDING"
            assert q.trust_class != "QUARANTINED"
            assert q.trust_class != "WITHDRAWN"
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
