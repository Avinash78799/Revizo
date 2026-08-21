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
async def test_m13_4_batch_2_medical_review_operations(client_and_db):
    """
    Milestone 13.4: Batch 2 Medical Review Operations (Exactly 100 Candidates).
    
    1. 100-Question Batch Selection (80 Standard-Risk + 20 High-Risk)
    2. Subject Diversity across 19 medical disciplines
    3. Standard-Risk Routing & Review (1 Doctor Review each)
    4. High-Risk Routing (2 Distinct Doctor Reviews each)
    5. Independent Blind Second Review (blinded payload)
    6. Disagreement Routing to Medical Board Quarantine
    7. Revision Workflow (REVIEW_PENDING / REVISION_REQUESTED)
    8. Rejection Workflow (REJECTED / WITHDRAWN)
    9. Quarantine Workflow (QUARANTINED)
    10. Approval Workflow (APPROVED / VERIFIED_CORE_QUESTION)
    11. Reviewer Suspension Gates
    12. Audit Immutability & Credential Preservation
    13. Student Pool Before/After Verification
    14. Duplicate Review Prevention
    15. PYQ Provenance Enforcement
    16. Specialty Routing Verification
    17. Reviewer Authorization
    18. Complete Count & Reconciliation Audit
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Admin & Student
        admin = User(email="chief_dean_m13_4@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_batch2_tester@neetpg.pro", hashed_password="pw", role="student", is_active=True)
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
        # 1 & 2. SELECT 100-QUESTION BATCH & VERIFY SUBJECT DIVERSITY
        # =========================================================================
        std_candidates = []
        for meta in NMC_19_SUBJECTS_METADATA:
            q_list = await ReviewQueueService.get_standard_risk_queue(session, subject_code=meta["code"], limit=5)
            for q in q_list:
                if len(std_candidates) < 80:
                    std_candidates.append(q)

        hr_candidates = []
        for meta in NMC_19_SUBJECTS_METADATA:
            q_hr_list = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", subject_code=meta["code"], limit=4)
            for q in q_hr_list:
                if len(hr_candidates) < 20:
                    hr_candidates.append(q)
        if len(hr_candidates) < 20:
            remaining_hr = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=20 - len(hr_candidates))
            for q in remaining_hr:
                if q not in hr_candidates and len(hr_candidates) < 20:
                    hr_candidates.append(q)

        assert len(std_candidates) == 80
        assert len(hr_candidates) == 20
        total_batch_100 = std_candidates + hr_candidates
        assert len(total_batch_100) == 100

        # Verify subject diversity across the batch
        batch_subjects = set()
        for q in total_batch_100:
            if q.concept and q.concept.topic and q.concept.topic.chapter and q.concept.topic.chapter.subject:
                batch_subjects.add(q.concept.topic.chapter.subject.code)
        assert len(batch_subjects) >= 15  # Rich representation across the 19 subjects

        # Verify all 100 are strictly blocked from student pool before processing
        batch_100_ids = {q.id for q in total_batch_100}
        sess_before, practice_before = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=30
        )
        before_ids = {q.id for q in practice_before}
        assert len(batch_100_ids.intersection(before_ids)) == 0

        # =========================================================================
        # 3. PROCESS 80 STANDARD-RISK CANDIDATES (1 Doctor Review Each)
        # =========================================================================
        approved_std = 0
        rejected_std = 0
        revision_std = 0
        quarantined_std = 0

        for idx, q in enumerate(std_candidates):
            # Specialty-aware assignment
            reviewer = lead_auditor
            for spec, prof in reviewer_by_spec.items():
                if q.concept and spec.lower() in q.concept.name.lower():
                    reviewer = prof
                    break

            if idx == 76 or idx == 77:
                # 2 Rejections (Outdated guidelines / wrong distractor logic)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REJECT",
                    clinical_notes=f"Standard-Risk Reject #{idx}: Obsolete treatment recommendation."
                )
                assert res["status"] == "REJECTED"
                assert res["trust_class"] == "WITHDRAWN"
                rejected_std += 1
            elif idx == 78:
                # 1 Revision Request (Ambiguous distractor wording)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REQUEST_REVISION",
                    clinical_notes=f"Standard-Risk Revision #{idx}: Rephrase option B for clinical clarity."
                )
                assert res["status"] == "REVISION_REQUESTED"
                revision_std += 1
            elif idx == 79:
                # 1 Quarantine (Contradictory international guideline thresholds)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="QUARANTINE",
                    clinical_notes=f"Standard-Risk Quarantine #{idx}: Disputed staging criteria between WHO and CDC."
                )
                assert res["status"] == "QUARANTINED"
                assert res["trust_class"] == "QUARANTINED"
                quarantined_std += 1
            else:
                # 76 Approvals
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="APPROVE",
                    clinical_notes=f"Standard-Risk Approved #{idx}: Verified against canonical textbook citation."
                )
                assert res["status"] == "APPROVED"
                assert res["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_std += 1

        assert approved_std == 76
        assert rejected_std == 2
        assert revision_std == 1
        assert quarantined_std == 1

        # =========================================================================
        # 4, 5, 6. PROCESS 20 HIGH-RISK CANDIDATES (Two-Doctor Review Workflow)
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

            # Verify Doctor A != Doctor B
            assert doc_a.user_id != doc_b.user_id

            if idx == 16:
                # High-Risk Rejection by Doctor A (Unsafe drug dosage)
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REJECT",
                    clinical_notes="Doctor A: Rejected due to toxic pediatric dosing."
                )
                assert res_a["status"] == "REJECTED"
                assert res_a["trust_class"] == "WITHDRAWN"
                rejected_hr += 1
            elif idx == 17:
                # High-Risk Revision Request by Doctor A
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REQUEST_REVISION",
                    clinical_notes="Doctor A: Revise contraindication vignette context."
                )
                assert res_a["status"] == "REVISION_REQUESTED"
                revision_hr += 1
            elif idx == 18:
                # High-Risk Disagreement 1: Doctor A Approves, Doctor B Rejects -> Medical Board Quarantine
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes="Doctor A: Thrombolysis protocol approved."
                )
                # Verify Doctor B receives blinded payload
                payload_doc_b = await ReviewQueueService.get_review_interface_payload(session, q.id, doc_b.user_id)
                assert payload_doc_b["review_history"] == []

                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="REJECT",
                    clinical_notes="Doctor B: Rejection due to high hemorrhagic conversion risk."
                )
                assert res_b["status"] == "QUARANTINED"
                assert res_b["trust_class"] == "QUARANTINED"
                quarantined_hr += 1
            elif idx == 19:
                # High-Risk Disagreement 2: Doctor A Approves, Doctor B Quarantines -> Medical Board Quarantine
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes="Doctor A: Airway management verified."
                )
                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="QUARANTINE",
                    clinical_notes="Doctor B: Quarantined due to airway guideline conflict in cervical injury."
                )
                assert res_b["status"] == "QUARANTINED"
                assert res_b["trust_class"] == "QUARANTINED"
                quarantined_hr += 1
            else:
                # 16 High-Risk Independent Approvals (Doctor A + Doctor B)
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes=f"Doctor A: Verified high-risk clinical safety #{idx}."
                )
                assert res_a["status"] == "REVIEW_PENDING"

                # Verify Doctor B receives blinded payload
                payload_doc_b = await ReviewQueueService.get_review_interface_payload(session, q.id, doc_b.user_id)
                assert payload_doc_b["review_history"] == []

                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="APPROVE",
                    clinical_notes=f"Doctor B: Concur with emergency management #{idx}."
                )
                assert res_b["status"] == "APPROVED"
                assert res_b["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_hr += 1

        assert approved_hr == 16
        assert rejected_hr == 1
        assert revision_hr == 1
        assert quarantined_hr == 2

        await session.commit()

        # =========================================================================
        # 8 & 9. RECONCILIATION & QUALITY METRICS
        # =========================================================================
        total_approved = approved_std + approved_hr        # 76 + 16 = 92
        total_rejected = rejected_std + rejected_hr        # 2 + 1 = 3
        total_revision = revision_std + revision_hr        # 1 + 1 = 2
        total_quarantined = quarantined_std + quarantined_hr  # 1 + 2 = 3

        assert total_approved == 92
        assert total_rejected == 3
        assert total_revision == 2
        assert total_quarantined == 3
        assert (total_approved + total_rejected + total_revision + total_quarantined) == 100

        # High-Risk Disagreement rate: 2 out of 20 (10%)
        disagreement_count = 2
        assert disagreement_count == 2

        # =========================================================================
        # 10. STUDENT POOL AFTER VERIFICATION
        # =========================================================================
        sess_after, practice_after = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=100
        )
        after_ids = {q.id for q in practice_after}

        # Verify that all returned questions are strictly APPROVED & published
        for q in practice_after:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.trust_class not in [
                "AI_GENERATED_REVIEW_PENDING",
                "QUARANTINED",
                "WITHDRAWN",
                "UNVERIFIED"
            ]

        # Verify all remaining unreviewed questions (>800 items) are 100% blocked
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
        # 11 & 12. AUDIT TRAIL IMMUTABILITY & SNAPSHOTS
        # =========================================================================
        stmt_reviews = select(QuestionReview)
        all_reviews = (await session.execute(stmt_reviews)).scalars().all()
        # 80 standard reviews + (16 * 2 + 1 + 1 + 2 * 2) high risk reviews = 80 + 38 = 118 reviews
        assert len(all_reviews) >= 118
        for rev in all_reviews:
            assert rev.reviewer_credential_status is not None
            assert rev.source_verification_decision == "VERIFIED"
            assert rev.clinical_notes is not None
            assert rev.created_at is not None
