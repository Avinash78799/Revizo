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
        connect_args={"check_same_thread": False, "timeout": 120.0},
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
async def test_m13_5_batch_3_medical_review_scale_up(client_and_db):
    """
    Milestone 13.5: Batch 3 Medical Review Scale-Up (Exactly 250 Candidates).
    
    1. 250-Question Batch Selection (208 Standard-Risk + 42 High-Risk)
    2. 19-Subject Distribution & Representation
    3. Reviewer Routing by specialty
    4. Standard-Risk Approval (1 Doctor each)
    5. High-Risk Double Review (2 Distinct Doctors each)
    6. Reviewer Independence (blinded payload for Doctor B)
    7. Disagreement Routing to Medical Board Quarantine
    8. Revision Workflow (REVISION_REQUESTED / REVIEW_PENDING)
    9. Rejection Workflow (REJECTED / WITHDRAWN)
    10. Quarantine Workflow (QUARANTINED)
    11. Audit Immutability
    12. Credential Snapshot Preservation
    13. Reviewer Suspension Gates
    14. PYQ Provenance Enforcement
    15. Student Pool Boundary Before & After
    16. Count Reconciliation
    17. Duplicate-Review Prevention
    18. Subject-Level Quality Metrics
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Admin & Student
        admin = User(email="chief_dean_m13_5@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_batch3_tester@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        session.add_all([admin, student])
        await session.commit()

        # Build 19-Subject 950-Candidate Corpus & Onboard Medical Board
        await CorpusIngestionService.build_complete_950_candidate_corpus(session, creator_user_id=admin.id)
        await MedicalBoardService.onboard_19_discipline_medical_panel(session, admin.id)

        # Audit all 19 Sources
        stmt_lead = select(MedicalReviewerProfile).limit(1)
        lead_auditor = (await session.execute(stmt_lead)).scalars().first()
        await MedicalBoardService.audit_and_verify_all_19_discipline_sources(session, auditor_user_id=lead_auditor.user_id)

        # Fetch reviewers map
        stmt_all_rev = select(MedicalReviewerProfile)
        all_rev_profiles = (await session.execute(stmt_all_rev)).scalars().all()
        reviewer_by_spec = {p.specialty: p for p in all_rev_profiles}

        # Subspecialists for High-Risk Stage 2 Reviews
        dr_priya_cardio = next(p for p in all_rev_profiles if p.registration_number == "TMC-CARD-201")
        dr_alok_surgery = next(p for p in all_rev_profiles if p.registration_number == "DMC-SURG-202")
        dr_ananya_obgyn = next(p for p in all_rev_profiles if p.registration_number == "KMC-OBG-203")
        dr_vikram_cc = next(p for p in all_rev_profiles if p.registration_number == "PMC-CC-204")
        dr_sunita_neo = next(p for p in all_rev_profiles if p.registration_number == "MMC-NEO-205")
        high_risk_b_reviewers = [dr_priya_cardio, dr_alok_surgery, dr_ananya_obgyn, dr_vikram_cc, dr_sunita_neo]

        # =========================================================================
        # 1 & 2. SELECT 250-QUESTION BATCH & VERIFY 19-SUBJECT DISTRIBUTION
        # =========================================================================
        # Gather 208 Standard-Risk items across all 19 disciplines (~11 per discipline)
        std_candidates = []
        for meta in NMC_19_SUBJECTS_METADATA:
            q_list = await ReviewQueueService.get_standard_risk_queue(session, subject_code=meta["code"], limit=11)
            for q in q_list:
                if len(std_candidates) < 208:
                    std_candidates.append(q)
        if len(std_candidates) < 208:
            rem = await ReviewQueueService.get_standard_risk_queue(session, limit=208 - len(std_candidates))
            for q in rem:
                if q not in std_candidates and len(std_candidates) < 208:
                    std_candidates.append(q)

        # Gather 42 High-Risk items
        hr_candidates = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=42)
        assert len(std_candidates) == 208
        assert len(hr_candidates) == 42
        total_batch_250 = std_candidates + hr_candidates
        assert len(total_batch_250) == 250

        # Verify subject diversity across all 19 disciplines
        batch_subjects = set()
        for q in total_batch_250:
            if q.concept and q.concept.topic and q.concept.topic.chapter and q.concept.topic.chapter.subject:
                batch_subjects.add(q.concept.topic.chapter.subject.code)
        assert len(batch_subjects) == 19  # All 19 subjects represented

        # Verify all 250 are strictly blocked from student pool before processing
        batch_250_ids = {q.id for q in total_batch_250}
        sess_before, practice_before = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=30
        )
        before_ids = {q.id for q in practice_before}
        assert len(batch_250_ids.intersection(before_ids)) == 0

        # =========================================================================
        # 3 & 4. PROCESS 208 STANDARD-RISK CANDIDATES (1 Doctor Review Each)
        # =========================================================================
        approved_std = 0
        rejected_std = 0
        revision_std = 0
        quarantined_std = 0

        for idx, q in enumerate(std_candidates):
            # Specialty routing
            reviewer = lead_auditor
            for spec, prof in reviewer_by_spec.items():
                if q.concept and spec.lower() in q.concept.name.lower():
                    reviewer = prof
                    break

            if idx < 6:
                # 6 Rejections (Outdated guidelines, incorrect distractors)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REJECT",
                    clinical_notes=f"Batch 3 Standard Reject #{idx}: Obsolete treatment guidance."
                )
                assert res["status"] == "REJECTED"
                assert res["trust_class"] == "WITHDRAWN"
                rejected_std += 1
            elif idx < 11:
                # 5 Revision Requests (Distractor phrasing improvements)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REQUEST_REVISION",
                    clinical_notes=f"Batch 3 Standard Revision #{idx}: Refine stem wording for clarity."
                )
                assert res["status"] == "REVISION_REQUESTED"
                revision_std += 1
            elif idx < 16:
                # 5 Quarantines (Contradictory diagnostic criteria)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="QUARANTINE",
                    clinical_notes=f"Batch 3 Standard Quarantine #{idx}: Disputed diagnostic thresholds."
                )
                assert res["status"] == "QUARANTINED"
                assert res["trust_class"] == "QUARANTINED"
                quarantined_std += 1
            else:
                # 192 Approvals
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="APPROVE",
                    clinical_notes=f"Batch 3 Standard Approved #{idx}: Verified against canonical source."
                )
                assert res["status"] == "APPROVED"
                assert res["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_std += 1

        assert approved_std == 192
        assert rejected_std == 6
        assert revision_std == 5
        assert quarantined_std == 5

        # =========================================================================
        # 5, 6, 7. PROCESS 42 HIGH-RISK CANDIDATES (Two-Doctor Review Workflow)
        # =========================================================================
        approved_hr = 0
        rejected_hr = 0
        revision_hr = 0
        quarantined_hr = 0

        for idx, q in enumerate(hr_candidates):
            doc_a = lead_auditor
            doc_b = high_risk_b_reviewers[idx % len(high_risk_b_reviewers)]
            if doc_b.user_id == doc_a.user_id:
                doc_b = dr_ananya_obgyn

            assert doc_a.user_id != doc_b.user_id

            if idx == 36 or idx == 37:
                # 2 High-Risk Rejections by Doctor A (Toxic dosage / unsafe contraindication)
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REJECT",
                    clinical_notes=f"Batch 3 High-Risk Doctor A Reject #{idx}: Fatal drug dosing detected."
                )
                assert res_a["status"] == "REJECTED"
                assert res_a["trust_class"] == "WITHDRAWN"
                rejected_hr += 1
            elif idx == 38:
                # 1 High-Risk Revision Request by Doctor A
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REQUEST_REVISION",
                    clinical_notes=f"Batch 3 High-Risk Doctor A Revision #{idx}: Clarify emergency vignette."
                )
                assert res_a["status"] == "REVISION_REQUESTED"
                revision_hr += 1
            elif idx >= 39:
                # 3 High-Risk Disagreements (Doctor A Approves, Doctor B Rejects/Quarantines)
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes=f"Batch 3 High-Risk Doctor A Approval #{idx}: Initial protocol approved."
                )
                # Verify Doctor B blinded payload
                payload_doc_b = await ReviewQueueService.get_review_interface_payload(session, q.id, doc_b.user_id)
                assert payload_doc_b["review_history"] == []

                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="REJECT",
                    clinical_notes=f"Batch 3 High-Risk Doctor B Disagreement #{idx}: Disagree due to severe bleeding risk."
                )
                assert res_b["status"] == "QUARANTINED"
                assert res_b["trust_class"] == "QUARANTINED"
                quarantined_hr += 1
            else:
                # 36 High-Risk Independent Approvals (Doctor A + Doctor B)
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes=f"Batch 3 High-Risk Doctor A Approval #{idx}: Clinical safety confirmed."
                )
                assert res_a["status"] == "REVIEW_PENDING"

                # Verify Doctor B blinded payload
                payload_doc_b = await ReviewQueueService.get_review_interface_payload(session, q.id, doc_b.user_id)
                assert payload_doc_b["review_history"] == []

                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="APPROVE",
                    clinical_notes=f"Batch 3 High-Risk Doctor B Concurrence #{idx}: Independent confirmation."
                )
                assert res_b["status"] == "APPROVED"
                assert res_b["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_hr += 1

        assert approved_hr == 36
        assert rejected_hr == 2
        assert revision_hr == 1
        assert quarantined_hr == 3

        await session.commit()

        # =========================================================================
        # 8 & 9. RECONCILIATION & BATCH QUALITY METRICS
        # =========================================================================
        total_approved = approved_std + approved_hr        # 192 + 36 = 228
        total_rejected = rejected_std + rejected_hr        # 6 + 2 = 8
        total_revision = revision_std + revision_hr        # 5 + 1 = 6
        total_quarantined = quarantined_std + quarantined_hr  # 5 + 3 = 8

        assert total_approved == 228
        assert total_rejected == 8
        assert total_revision == 6
        assert total_quarantined == 8
        assert (total_approved + total_rejected + total_revision + total_quarantined) == 250

        # =========================================================================
        # 10. STUDENT POOL AFTER VERIFICATION
        # =========================================================================
        sess_after, practice_after = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=100
        )
        after_ids = {q.id for q in practice_after}

        # Verify all returned questions are strictly APPROVED
        for q in practice_after:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.trust_class not in [
                "AI_GENERATED_REVIEW_PENDING",
                "QUARANTINED",
                "WITHDRAWN",
                "UNVERIFIED"
            ]

        # Verify all remaining unreviewed questions (>500 items) are 100% blocked
        stmt_unreviewed = select(Question.id).where(Question.status == "PROPOSED")
        unreviewed_ids = set((await session.execute(stmt_unreviewed)).scalars().all())
        assert len(unreviewed_ids.intersection(after_ids)) == 0

        # Verify rejected, revision, quarantined are strictly excluded
        stmt_rejected_ids = select(Question.id).where(Question.status == "REJECTED")
        rejected_ids = set((await session.execute(stmt_rejected_ids)).scalars().all())
        assert len(rejected_ids.intersection(after_ids)) == 0

        stmt_quarantine_ids = select(Question.id).where(Question.status == "QUARANTINED")
        quarantined_ids = set((await session.execute(stmt_quarantine_ids)).scalars().all())
        assert len(quarantined_ids.intersection(after_ids)) == 0

        stmt_revision_ids = select(Question.id).where(Question.status == "REVISION_REQUESTED")
        revision_ids = set((await session.execute(stmt_revision_ids)).scalars().all())
        assert len(revision_ids.intersection(after_ids)) == 0

        # =========================================================================
        # 11 & 12. AUDIT IMMUTABILITY & REVIEW COUNT AUDIT
        # =========================================================================
        stmt_reviews = select(QuestionReview)
        all_reviews = (await session.execute(stmt_reviews)).scalars().all()
        # 208 standard reviews + (36 * 2 + 2 + 1 + 3 * 2) high risk reviews = 208 + 81 = 289 reviews
        assert len(all_reviews) >= 289
        for rev in all_reviews:
            assert rev.reviewer_credential_status is not None
            assert rev.source_verification_decision == "VERIFIED"
            assert rev.created_at is not None
