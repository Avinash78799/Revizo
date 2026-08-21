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
from app.models.question import Question, QuestionOption, QuestionReview
from app.models.source import Source, EvidenceReference
from app.models.reviewer import MedicalReviewerProfile
from app.services.corpus_ingestion_service import CorpusIngestionService
from app.services.review_queue_service import ReviewQueueService
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
async def test_m12_8_doctor_review_operations_workflow(client_and_db):
    """
    Milestone 12.8: Doctor Review Operations & Queue Enforcement.
    
    1. Reviewer Queue Dashboard & Metrics.
    2. Review Interface Data Payload (stem, 4 options, evidence, source, history).
    3. Standard-Risk Flow: 1 Doctor Review -> VERIFIED_CORE_QUESTION -> Student Pool Admission.
    4. High-Risk Flow: Doctor A -> Doctor B (Doctor A != Doctor B) -> VERIFIED_CORE_QUESTION.
    5. Anti-Self-Review Gate: Doctor A blocked from acting as Doctor B on same question.
    6. Negative Security Gates: Unverified reviewer, suspended reviewer, student blocked from review.
    7. Post-Review Rejection & Quarantine: Rejected/Quarantined items strictly excluded from student pool.
    8. Immutable Review Audit Records snapshot verification.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # 1. Setup Admin & Medical Doctors
        admin = User(email="super_admin_m12_8@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        dr_a = User(email="dr_a_surgeon@pgimer.edu.in", hashed_password="pw", role="medical_reviewer", is_active=True)
        dr_b = User(email="dr_b_internist@aiims.edu", hashed_password="pw", role="medical_reviewer", is_active=True)
        dr_suspended = User(email="dr_suspended@hospital.org", hashed_password="pw", role="medical_reviewer", is_active=True)
        dr_unverified = User(email="dr_unverified@clinic.org", hashed_password="pw", role="medical_reviewer", is_active=True)
        student = User(email="student_user@neetpg.pro", hashed_password="pw", role="student", is_active=True)

        session.add_all([admin, dr_a, dr_b, dr_suspended, dr_unverified, student])
        await session.commit()

        p_a = await ReviewerService.register_reviewer_profile(
            db=session, user_id=dr_a.id, credential_type="MS", registration_number="PMC-11001",
            medical_council="Punjab Medical Council", specialty="General Surgery"
        )
        p_b = await ReviewerService.register_reviewer_profile(
            db=session, user_id=dr_b.id, credential_type="MD", registration_number="DMC-22002",
            medical_council="Delhi Medical Council", specialty="General Medicine"
        )
        p_susp = await ReviewerService.register_reviewer_profile(
            db=session, user_id=dr_suspended.id, credential_type="MD", registration_number="KMC-33003",
            medical_council="Karnataka Medical Council", specialty="Pharmacology"
        )
        p_unver = await ReviewerService.register_reviewer_profile(
            db=session, user_id=dr_unverified.id, credential_type="MD", registration_number="TMC-44004",
            medical_council="Tamil Nadu Medical Council", specialty="Pediatrics"
        )

        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_a.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="PMC-AUDIT-1")
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_b.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="DMC-AUDIT-2")
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_susp.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="KMC-AUDIT-3")
        await ReviewerService.suspend_or_revoke_reviewer(db=session, profile_id=p_susp.id, admin_user_id=admin.id, action="SUSPEND", reason="Audit hold")

        # 2. Build complete 950 candidate corpus
        await CorpusIngestionService.build_complete_950_candidate_corpus(db=session, creator_user_id=admin.id)

        # 3. Doctor Dashboard Operations
        dashboard_dr_a = await ReviewQueueService.get_doctor_queue_dashboard(session, dr_a.id)
        assert dashboard_dr_a["reviewer"]["user_id"] == dr_a.id
        assert dashboard_dr_a["reviewer"]["qualification"] == "MS"
        assert dashboard_dr_a["reviewer"]["verification_status"] == "VERIFIED"
        assert dashboard_dr_a["metrics"]["global_standard_pending"] > 0
        assert dashboard_dr_a["metrics"]["global_high_risk_pending"] > 0

        # Unverified / Suspended doctor accessing dashboard -> BLOCKED
        with pytest.raises(AuthorizationError):
            await ReviewQueueService.get_doctor_queue_dashboard(session, dr_unverified.id)
        with pytest.raises(AuthorizationError):
            await ReviewQueueService.get_doctor_queue_dashboard(session, dr_suspended.id)

        # 4. Review Interface Data Payload Verification
        std_queue = await ReviewQueueService.get_standard_risk_queue(session, limit=10)
        target_std_q = std_queue[0]

        # Audit and verify source first (provenance chain)
        stmt_src = select(Source).where(Source.id == target_std_q.source_id)
        src_obj = (await session.execute(stmt_src)).scalars().first()
        await SourceProvenanceService.audit_and_verify_source(
            db=session, source_id=src_obj.id, verifier_id=dr_a.id, decision="VERIFIED",
            reference_identifier=src_obj.reference_identifier, edition=src_obj.edition,
            publisher=src_obj.publisher, audit_evidence_notes="Verified source catalog."
        )

        interface_payload = await ReviewQueueService.get_review_interface_payload(session, target_std_q.id, dr_a.id)
        assert interface_payload["question_id"] == target_std_q.id
        assert len(interface_payload["options"]) == 4
        assert interface_payload["source"]["verification_status"] == "VERIFIED"
        assert interface_payload["required_review_stage"] == "STAGE_1"

        # 5. Standard-Risk Approval (1 Doctor Review)
        rev_res = await MedicalContentService.perform_medical_review(
            db=session, question_id=target_std_q.id, reviewer_id=dr_a.id, verdict="APPROVE",
            clinical_notes="Doctor A clinical validation passed."
        )
        assert rev_res["status"] == "APPROVED"
        assert rev_res["trust_class"] == "VERIFIED_CORE_QUESTION"
        target_std_q.status = "PUBLISHED"
        await session.commit()

        # 6. High-Risk Two-Doctor Workflow & Anti-Self-Review Gate
        hr_queue = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=5)
        target_hr_q = hr_queue[0]

        stmt_hr_src = select(Source).where(Source.id == target_hr_q.source_id)
        hr_src_obj = (await session.execute(stmt_hr_src)).scalars().first()
        if hr_src_obj.verification_status != "VERIFIED":
            await SourceProvenanceService.audit_and_verify_source(
                db=session, source_id=hr_src_obj.id, verifier_id=dr_a.id, decision="VERIFIED",
                reference_identifier=hr_src_obj.reference_identifier, edition=hr_src_obj.edition,
                publisher=hr_src_obj.publisher, audit_evidence_notes="Verified clinical textbook."
            )

        # Stage 1: Doctor A Approves
        await MedicalContentService.perform_medical_review(
            db=session, question_id=target_hr_q.id, reviewer_id=dr_a.id, verdict="APPROVE",
            clinical_notes="Doctor A: Dosage and safety verified."
        )
        await session.refresh(target_hr_q)
        assert target_hr_q.status == "REVIEW_PENDING"
        assert target_hr_q.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # Anti-Self-Review: Doctor A attempting Stage 2 Review on same question -> MUST FAIL
        with pytest.raises((AuthorizationError, ValidationError)):
            await ReviewQueueService.get_review_interface_payload(session, target_hr_q.id, dr_a.id)

        with pytest.raises(ValidationError) as exc_self_doc:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=target_hr_q.id, reviewer_id=dr_a.id, verdict="APPROVE",
                clinical_notes="Doctor A attempting self approval as Doctor B."
            )
        assert "distinct medical doctors" in str(exc_self_doc.value).lower()

        # Stage 2: Doctor B (distinct doctor) Approves -> Successfully Promoted
        rev_hr_res = await MedicalContentService.perform_medical_review(
            db=session, question_id=target_hr_q.id, reviewer_id=dr_b.id, verdict="APPROVE",
            clinical_notes="Doctor B: Independent clinical confirmation."
        )
        assert rev_hr_res["status"] == "APPROVED"
        assert rev_hr_res["trust_class"] == "VERIFIED_CORE_QUESTION"
        target_hr_q.status = "PUBLISHED"
        await session.commit()

        # 7. Negative Security Gates: Unauthorized Review Attempts
        target_q3 = std_queue[1]
        # Student review attempt -> BLOCKED
        with pytest.raises((AuthorizationError, ValidationError)):
            await MedicalContentService.perform_medical_review(
                db=session, question_id=target_q3.id, reviewer_id=student.id, verdict="APPROVE",
                clinical_notes="Student review attempt"
            )

        # Suspended doctor review attempt -> BLOCKED
        with pytest.raises((AuthorizationError, ValidationError)):
            await MedicalContentService.perform_medical_review(
                db=session, question_id=target_q3.id, reviewer_id=dr_suspended.id, verdict="APPROVE",
                clinical_notes="Suspended doctor review attempt"
            )

        # 8. Rejection and Quarantine Lifecycles
        target_reject_q = std_queue[2]
        rev_reject = await MedicalContentService.perform_medical_review(
            db=session, question_id=target_reject_q.id, reviewer_id=dr_a.id, verdict="REJECT",
            clinical_notes="Clinically outdated guideline."
        )
        assert rev_reject["status"] == "REJECTED"
        assert rev_reject["trust_class"] == "WITHDRAWN"

        target_quar_q = std_queue[3]
        rev_quar = await MedicalContentService.perform_medical_review(
            db=session, question_id=target_quar_q.id, reviewer_id=dr_b.id, verdict="QUARANTINE",
            clinical_notes="Conflicting recommendations between international guidelines."
        )
        assert rev_quar["status"] == "QUARANTINED"
        assert rev_quar["trust_class"] == "QUARANTINED"

        # 9. Student Practice Pool Boundary Verification
        await session.commit()
        sess, practice_questions = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=10
        )
        practice_ids = {q.id for q in practice_questions}

        # Approved questions MUST be eligible
        assert target_std_q.id in practice_ids
        assert target_hr_q.id in practice_ids

        # Rejected, Quarantined, and Unapproved candidates MUST NOT be in practice pool
        assert target_reject_q.id not in practice_ids
        assert target_quar_q.id not in practice_ids
        for q in practice_questions:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.trust_class not in ["AI_GENERATED_REVIEW_PENDING", "QUARANTINED", "WITHDRAWN", "UNVERIFIED"]

        # 10. Immutable Review Audit Records Verification
        stmt_audits = select(QuestionReview).where(QuestionReview.question_id == target_hr_q.id).order_index if hasattr(select(QuestionReview), "order_index") else select(QuestionReview).where(QuestionReview.question_id == target_hr_q.id)
        audits = (await session.execute(stmt_audits)).scalars().all()
        assert len(audits) == 2
        reviewers_in_audit = {a.reviewer_id for a in audits}
        assert reviewers_in_audit == {dr_a.id, dr_b.id}
        for a in audits:
            assert a.reviewer_credential_status in ("MS_VERIFIED", "MD_VERIFIED")
            assert a.source_verification_decision == "VERIFIED"
            assert a.created_at is not None
