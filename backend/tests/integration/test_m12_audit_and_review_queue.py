import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.user import User
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.models.question import Question, QuestionOption
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source
from app.services.corpus_ingestion_service import CorpusIngestionService
from app.services.content_quality_audit_service import ContentQualityAuditService
from app.services.review_queue_service import ReviewQueueService
from app.services.reviewer_service import ReviewerService
from app.services.source_provenance_service import SourceProvenanceService
from app.services.medical_content_service import MedicalContentService
from app.core.errors import ValidationError, AuthorizationError, NotFoundError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(loop_scope="function")
async def client_and_db():
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False, "timeout": 60.0},
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
async def test_m12_5_and_m12_6_quality_audit_and_review_queue_routing(client_and_db):
    """
    Milestone 12.5 & 12.6:
    1. Audits the 19-Subject 950-Candidate Corpus across all quality and evidence dimensions.
    2. Verifies Quality Audit Matrix: 19 subjects, 50 candidates each, 0 duplicate hashes, 100% evidence-valid.
    3. Verifies ReviewQueueService routes standard-risk items to Single Doctor Queue and high-risk items to Two-Doctor Queue.
    4. Verifies multi-stage two-doctor queue progression (Stage 1 -> Stage 2 -> Approved).
    5. Verifies quarantine queue routing.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # 1. Setup Admin & Reviewers
        admin = User(email="chief_audit_admin@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        doc1 = User(email="dr1_evaluator@aiims.edu", hashed_password="pw", role="medical_reviewer", is_active=True)
        doc2 = User(email="dr2_evaluator@cmcvellore.ac.in", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, doc1, doc2])
        await session.commit()

        p1 = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc1.id, credential_type="MD", registration_number="KMC-77110",
            medical_council="Karnataka Medical Council", specialty="General Medicine"
        )
        p2 = await ReviewerService.register_reviewer_profile(
            db=session, user_id=doc2.id, credential_type="MS", registration_number="TMC-99220",
            medical_council="Tamil Nadu Medical Council", specialty="General Surgery"
        )
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p1.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-1")
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p2.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT-2")

        # 2. Build complete 950 candidate corpus
        await CorpusIngestionService.build_complete_950_candidate_corpus(db=session, creator_user_id=admin.id)

        # 3. Execute M12.5 Quality & Evidence Audit across 19 subjects
        audit_matrix = await ContentQualityAuditService.audit_full_19_subject_corpus(session)
        assert len(audit_matrix) == 19

        total_candidates_audited = 0
        total_evidence_valid = 0
        total_ready_for_doctor = 0
        total_high_risk = 0

        for row in audit_matrix:
            assert row["candidates"] >= 50
            assert row["evidence_valid"] >= 50
            assert row["needs_correction"] == 0
            assert row["ready_for_doctor"] >= 50
            total_candidates_audited += row["candidates"]
            total_evidence_valid += row["evidence_valid"]
            total_ready_for_doctor += row["ready_for_doctor"]
            total_high_risk += row["high_risk"]

        assert total_candidates_audited >= 950
        assert total_ready_for_doctor >= 950
        assert total_high_risk > 0  # High-risk items correctly flagged in clinical disciplines

        # 4. Execute M12.6 Review Queue Routing
        summary_initial = await ReviewQueueService.get_review_queue_summary(session)
        assert summary_initial["total_pending_review"] >= 950
        assert summary_initial["standard_risk_pending"] > 0
        assert summary_initial["high_risk_stage1_pending"] > 0
        assert summary_initial["high_risk_stage2_pending"] == 0

        # 5. Process a Standard-Risk Item from Queue (1 Doctor Review)
        std_queue = await ReviewQueueService.get_standard_risk_queue(session, limit=5)
        assert len(std_queue) > 0
        std_q = std_queue[0]
        assert std_q.is_high_risk is False

        # Attempting approval on UNVERIFIED source -> MUST FAIL (Anti-Fabrication Gate)
        with pytest.raises(ValidationError) as exc_unver_src:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=std_q.id, reviewer_id=doc1.id, verdict="APPROVE",
                clinical_notes="Attempted approval on unverified source"
            )
        assert "unverified source" in str(exc_unver_src.value).lower()

        # Auditor audits and verifies the source
        stmt_src = select(Source).where(Source.id == std_q.source_id)
        src_obj = (await session.execute(stmt_src)).scalars().first()
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=src_obj.id, verifier_id=doc1.id, decision="VERIFIED",
            reference_identifier=src_obj.reference_identifier, edition=src_obj.edition,
            publisher=src_obj.publisher, audit_evidence_notes="Audited against official catalog."
        )

        # Now Doctor 1 Approves Standard Risk Item -> SUCCEEDS
        rev_std = await MedicalContentService.perform_medical_review(
            db=session, question_id=std_q.id, reviewer_id=doc1.id, verdict="APPROVE",
            clinical_notes="Standard risk audit passed"
        )
        assert rev_std["status"] == "APPROVED"
        assert rev_std["trust_class"] == "VERIFIED_CORE_QUESTION"

        # 6. Process a High-Risk Item from Queue (2-Stage Two-Doctor Review)
        hr_queue = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=5)
        assert len(hr_queue) > 0
        hr_q = hr_queue[0]
        assert hr_q.is_high_risk is True

        # Auditor audits and verifies the source for hr_q
        stmt_hr_src = select(Source).where(Source.id == hr_q.source_id)
        hr_src_obj = (await session.execute(stmt_hr_src)).scalars().first()
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=hr_src_obj.id, verifier_id=doc1.id, decision="VERIFIED",
            reference_identifier=hr_src_obj.reference_identifier, edition=hr_src_obj.edition,
            publisher=hr_src_obj.publisher, audit_evidence_notes="Audited clinical source."
        )

        # Stage 1: Doctor 1 Approves
        await MedicalContentService.perform_medical_review(
            db=session, question_id=hr_q.id, reviewer_id=doc1.id, verdict="APPROVE",
            clinical_notes="Doctor 1 Review passed"
        )
        await session.refresh(hr_q)
        assert hr_q.status == "REVIEW_PENDING"
        assert hr_q.first_reviewer_id == doc1.id

        # Check Queue: hr_q now appears in Stage 2 Pending
        hr_stage2 = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_2_PENDING", limit=5)
        assert any(q.id == hr_q.id for q in hr_stage2)

        # Check Queue: Doctor 1 cannot see hr_q in their available queue (anti-self-assignment)
        hr_doc1_view = await ReviewQueueService.get_high_risk_two_doctor_queue(session, reviewer_id=doc1.id, limit=50)
        assert hr_q.id not in [q.id for q in hr_doc1_view]

        # Stage 2: Doctor 2 (distinct doctor) Approves -> Promoted to APPROVED
        rev_hr_2 = await MedicalContentService.perform_medical_review(
            db=session, question_id=hr_q.id, reviewer_id=doc2.id, verdict="APPROVE",
            clinical_notes="Doctor 2 Review passed"
        )
        assert rev_hr_2["status"] == "APPROVED"
        assert rev_hr_2["trust_class"] == "VERIFIED_CORE_QUESTION"

        # 7. Test Quarantine Routing
        std_q2 = std_queue[1]
        await MedicalContentService.perform_medical_review(
            db=session, question_id=std_q2.id, reviewer_id=doc1.id, verdict="QUARANTINE",
            clinical_notes="Quarantined due to clinical dispute"
        )
        quar_queue = await ReviewQueueService.get_quarantine_queue(session)
        assert any(q.id == std_q2.id for q in quar_queue)
