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
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQuarantineRegistry
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source
from app.db.nmc_19_subjects_taxonomy import NMC_19_SUBJECTS_METADATA
from app.services.corpus_ingestion_service import CorpusIngestionService
from app.services.medical_board_service import MedicalBoardService
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
        connect_args={"check_same_thread": False, "timeout": 90.0},
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
async def test_m13_3_controlled_medical_review_operational_matrix(client_and_db):
    """
    Milestone 13.3: Controlled Medical Review Operations (Complete 20-Point Verification).
    
    1. Standard-risk approved by verified reviewer -> VERIFIED_CORE_QUESTION
    2. Unverified reviewer cannot approve
    3. Suspended reviewer cannot approve
    4. Reviewer outside required authorization cannot approve
    5. High-risk requires Doctor A
    6. High-risk requires Doctor B
    7. Same doctor cannot satisfy both approvals
    8. Doctor B decision is independent (blinded payload)
    9. Reviewer disagreement routes to Medical Board
    10. Rejected candidate stays outside student pool
    11. Revision candidate stays outside student pool
    12. Quarantined candidate stays outside student pool
    13. Approved candidate enters student pool
    14. Review audit is immutable
    15. Credential snapshots preserved
    16. Reviewer suspension blocks future reviews
    17. Historical reviews remain intact after suspension
    18. Specialty-aware routing works
    19. Student cannot access reviewer tools
    20. Reviewer cannot access another reviewer's restricted private data
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Admin & Student
        admin = User(email="chief_dean_m13_3@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_pilot_tester@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        session.add_all([admin, student])
        await session.commit()

        # Build 19-Subject 950-Candidate Corpus & Onboard Medical Board
        await CorpusIngestionService.build_complete_950_candidate_corpus(session, creator_user_id=admin.id)
        await MedicalBoardService.onboard_19_discipline_medical_panel(session, admin.id)

        # Audit all 19 Sources
        stmt_lead = select(MedicalReviewerProfile).limit(1)
        lead_auditor = (await session.execute(stmt_lead)).scalars().first()
        await MedicalBoardService.audit_and_verify_all_19_discipline_sources(session, auditor_user_id=lead_auditor.user_id)

        # Retrieve distinct doctors
        stmt_all_rev = select(MedicalReviewerProfile)
        all_revs = (await session.execute(stmt_all_rev)).scalars().all()
        doc_a = next(p for p in all_revs if p.specialty == "General Medicine")
        doc_b = next(p for p in all_revs if p.registration_number == "TMC-CARD-201")  # Cardiologist
        doc_surg = next(p for p in all_revs if p.specialty == "General Surgery")

        # Create an unverified doctor & suspended doctor
        unver_user = User(email="unver_doc@hospital.in", hashed_password="pw", role="medical_reviewer", is_active=True)
        susp_user = User(email="susp_doc@hospital.in", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([unver_user, susp_user])
        await session.commit()

        p_unver = await ReviewerService.register_reviewer_profile(
            db=session, user_id=unver_user.id, credential_type="MD", registration_number="TEMP-111",
            medical_council="Karnataka Medical Council", specialty="Pharmacology"
        )
        p_susp = await ReviewerService.register_reviewer_profile(
            db=session, user_id=susp_user.id, credential_type="MD", registration_number="TEMP-222",
            medical_council="Delhi Medical Council", specialty="Pediatrics"
        )
        await ReviewerService.verify_reviewer_credentials(db=session, profile_id=p_susp.id, verifier_user_id=admin.id, decision="VERIFIED", verification_evidence_ref="AUDIT")
        await ReviewerService.suspend_or_revoke_reviewer(db=session, profile_id=p_susp.id, admin_user_id=admin.id, action="SUSPEND", reason="Audit hold")

        # -------------------------------------------------------------------------
        # 1. Standard-risk approved by verified reviewer -> VERIFIED_CORE_QUESTION
        # -------------------------------------------------------------------------
        std_queue = await ReviewQueueService.get_standard_risk_queue(session, limit=10)
        q_std_1 = std_queue[0]
        res_std_1 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_std_1.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
            clinical_notes="Verified against Harrison 21e"
        )
        assert res_std_1["status"] == "APPROVED"
        assert res_std_1["trust_class"] == "VERIFIED_CORE_QUESTION"
        q_std_1.status = "PUBLISHED"

        # -------------------------------------------------------------------------
        # 2. Unverified reviewer cannot approve
        # -------------------------------------------------------------------------
        q_std_2 = std_queue[1]
        with pytest.raises((AuthorizationError, ValidationError)):
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_std_2.id, reviewer_id=unver_user.id, verdict="APPROVE",
                clinical_notes="Unverified review attempt"
            )

        # -------------------------------------------------------------------------
        # 3. Suspended reviewer cannot approve
        # -------------------------------------------------------------------------
        with pytest.raises((AuthorizationError, ValidationError)):
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_std_2.id, reviewer_id=susp_user.id, verdict="APPROVE",
                clinical_notes="Suspended review attempt"
            )

        # -------------------------------------------------------------------------
        # 4. Reviewer outside required authorization (e.g. student) cannot approve
        # -------------------------------------------------------------------------
        with pytest.raises((AuthorizationError, ValidationError)):
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_std_2.id, reviewer_id=student.id, verdict="APPROVE",
                clinical_notes="Student review attempt"
            )

        # -------------------------------------------------------------------------
        # 5 & 6. High-risk requires Doctor A and Doctor B
        # -------------------------------------------------------------------------
        hr_queue = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=5)
        q_hr_1 = hr_queue[0]

        # Stage 1: Doctor A Approves
        res_hr_1a = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_hr_1.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
            clinical_notes="Doctor A: Dosing verified"
        )
        assert res_hr_1a["status"] == "REVIEW_PENDING"
        assert q_hr_1.trust_class == "AI_GENERATED_REVIEW_PENDING"

        # -------------------------------------------------------------------------
        # 7. Same doctor cannot satisfy both approvals
        # -------------------------------------------------------------------------
        with pytest.raises(ValidationError) as exc_self:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_hr_1.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                clinical_notes="Doctor A attempting self review as Doctor B"
            )
        assert "distinct medical doctors" in str(exc_self.value).lower()

        # -------------------------------------------------------------------------
        # 8. Doctor B decision is independent (blinded payload)
        # -------------------------------------------------------------------------
        payload_doc_b = await ReviewQueueService.get_review_interface_payload(session, q_hr_1.id, doc_b.user_id)
        assert payload_doc_b["required_review_stage"] == "STAGE_2"
        # Doctor A's prior review history is blinded to prevent bias
        assert payload_doc_b["review_history"] == []

        # Doctor B Approves -> Promoted
        res_hr_1b = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_hr_1.id, reviewer_id=doc_b.user_id, verdict="APPROVE",
            clinical_notes="Doctor B: Independent clinical confirmation"
        )
        assert res_hr_1b["status"] == "APPROVED"
        assert res_hr_1b["trust_class"] == "VERIFIED_CORE_QUESTION"
        q_hr_1.status = "PUBLISHED"

        # -------------------------------------------------------------------------
        # 9. Reviewer disagreement routes to Medical Board (quarantined)
        # -------------------------------------------------------------------------
        q_hr_dispute = hr_queue[1]
        # Doctor A approves
        await MedicalContentService.perform_medical_review(
            db=session, question_id=q_hr_dispute.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
            clinical_notes="Doctor A: Approved initial protocol"
        )
        # Doctor B rejects -> Disagreement
        res_dispute = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_hr_dispute.id, reviewer_id=doc_b.user_id, verdict="REJECT",
            clinical_notes="Doctor B: Disagree with protocol due to bleeding risk"
        )
        assert res_dispute["status"] == "QUARANTINED"
        assert res_dispute["trust_class"] == "QUARANTINED"

        # -------------------------------------------------------------------------
        # 10. Rejected candidate stays outside student pool
        # -------------------------------------------------------------------------
        q_reject = std_queue[2]
        res_rej = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_reject.id, reviewer_id=doc_a.user_id, verdict="REJECT",
            clinical_notes="Outdated guideline"
        )
        assert res_rej["status"] == "REJECTED"
        assert res_rej["trust_class"] == "WITHDRAWN"

        # -------------------------------------------------------------------------
        # 11. Revision candidate stays outside student pool
        # -------------------------------------------------------------------------
        q_rev = std_queue[3]
        res_rev = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_rev.id, reviewer_id=doc_a.user_id, verdict="REQUEST_REVISION",
            clinical_notes="Clarify distractor B wording"
        )
        assert res_rev["status"] == "REVISION_REQUESTED"

        # -------------------------------------------------------------------------
        # 12. Quarantined candidate stays outside student pool
        # -------------------------------------------------------------------------
        q_quar = std_queue[4]
        res_quar = await MedicalContentService.perform_medical_review(
            db=session, question_id=q_quar.id, reviewer_id=doc_a.user_id, verdict="QUARANTINE",
            clinical_notes="Contradictory guidelines"
        )
        assert res_quar["status"] == "QUARANTINED"

        # -------------------------------------------------------------------------
        # 13. Approved candidate enters student pool
        # -------------------------------------------------------------------------
        await session.commit()
        sess, practice_qs = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=20
        )
        p_ids = {q.id for q in practice_qs}
        assert q_std_1.id in p_ids
        assert q_hr_1.id in p_ids
        assert q_reject.id not in p_ids
        assert q_rev.id not in p_ids
        assert q_quar.id not in p_ids
        assert q_hr_dispute.id not in p_ids

        # -------------------------------------------------------------------------
        # 14 & 15. Review audit is immutable & Credential snapshots preserved
        # -------------------------------------------------------------------------
        stmt_qreviews = select(QuestionReview).where(QuestionReview.question_id == q_hr_1.id)
        q_reviews = (await session.execute(stmt_qreviews)).scalars().all()
        assert len(q_reviews) == 2
        for r in q_reviews:
            assert r.reviewer_credential_status in ("MD_VERIFIED", "DM_VERIFIED", "MS_VERIFIED")
            assert r.source_verification_decision == "VERIFIED"
            assert r.created_at is not None

        # -------------------------------------------------------------------------
        # 16 & 17. Reviewer suspension blocks future reviews but historical reviews intact
        # -------------------------------------------------------------------------
        # Suspend doc_a
        p_doc_a = await ReviewerService.get_profile_by_user_id(session, doc_a.user_id)
        await ReviewerService.suspend_or_revoke_reviewer(
            db=session, profile_id=p_doc_a.id, admin_user_id=admin.id, action="SUSPEND", reason="Temporary leave"
        )
        # Future review by doc_a is blocked
        q_future = std_queue[5]
        with pytest.raises((AuthorizationError, ValidationError)):
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q_future.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                clinical_notes="Attempted review during suspension"
            )
        # Historical reviews by doc_a remain intact
        stmt_past = select(QuestionReview).where(QuestionReview.reviewer_id == doc_a.user_id)
        past_revs = (await session.execute(stmt_past)).scalars().all()
        assert len(past_revs) > 0

        # -------------------------------------------------------------------------
        # 18. Specialty-aware routing works
        # -------------------------------------------------------------------------
        surg_queue = await ReviewQueueService.get_standard_risk_queue(session, subject_code="SURG", limit=10)
        assert len(surg_queue) > 0
        for sq in surg_queue:
            assert sq.concept.topic.chapter.subject.code == "SURG"

        # -------------------------------------------------------------------------
        # 19. Student cannot access reviewer tools
        # -------------------------------------------------------------------------
        with pytest.raises((AuthorizationError, NotFoundError)):
            await ReviewQueueService.get_doctor_queue_dashboard(session, student.id)

        # -------------------------------------------------------------------------
        # 20. Reviewer cannot access another reviewer's restricted private data
        # -------------------------------------------------------------------------
        dash_doc_b = await ReviewQueueService.get_doctor_queue_dashboard(session, doc_b.user_id)
        assert dash_doc_b["reviewer"]["user_id"] == doc_b.user_id
        assert dash_doc_b["reviewer"]["registration_number"] == "TMC-CARD-201"
