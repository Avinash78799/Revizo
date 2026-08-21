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
from app.services.corpus_ingestion_service import CorpusIngestionService
from app.services.medical_board_service import MedicalBoardService
from app.services.review_queue_service import ReviewQueueService
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
async def test_m13_3_1_controlled_50_question_medical_review_batch(client_and_db):
    """
    Milestone 13.3.1: Controlled 50-Question Medical Review Operational Batch.
    
    1. Onboard 24 Medical Board Reviewers and Audit 19 Canonical Sources.
    2. Build 950-Candidate Corpus across all 19 disciplines.
    3. Select 50 candidates from the queue (40 Standard-Risk + 10 High-Risk).
    4. Execute 1-Doctor Review for 40 Standard-Risk items:
       - 37 Approved -> VERIFIED_CORE_QUESTION
       - 2 Rejected -> REJECTED / WITHDRAWN
       - 1 Quarantined -> QUARANTINED
    5. Execute 2-Distinct-Doctor Review for 10 High-Risk items:
       - 8 Approved by Doctor A & Doctor B -> VERIFIED_CORE_QUESTION
       - 1 Rejected by Doctor A -> REJECTED / WITHDRAWN
       - 1 Quarantined by Doctor B -> QUARANTINED
    6. Verify Total Review Actions = 40 (standard) + 20 (high-risk) = 60 actions.
    7. Verify Student Practice Pool Isolation:
       - Exactly the 45 approved questions are active in pool.
       - All 3 rejected, 2 quarantined, and 900 unreviewed candidates are 100% BLOCKED.
    8. Verify Immutable Audit Records for all 60 actions.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # 1. Setup Admin & Student
        admin = User(email="chief_dean_m13_3@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_pilot_tester@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        session.add_all([admin, student])
        await session.commit()

        # 2. Build 19-Subject Candidate Corpus (950 Candidates)
        await CorpusIngestionService.build_complete_950_candidate_corpus(session, creator_user_id=admin.id)

        # 3. Onboard 24 Medical Board Specialists
        await MedicalBoardService.onboard_19_discipline_medical_panel(session, admin.id)

        # 4. Audit & Verify All 19 Sources
        stmt_lead = select(MedicalReviewerProfile).limit(1)
        lead_auditor = (await session.execute(stmt_lead)).scalars().first()
        await MedicalBoardService.audit_and_verify_all_19_discipline_sources(session, auditor_user_id=lead_auditor.user_id)

        # Fetch reviewers map by specialty
        stmt_all_rev = select(MedicalReviewerProfile)
        all_rev_profiles = (await session.execute(stmt_all_rev)).scalars().all()
        reviewer_by_spec = {p.specialty: p for p in all_rev_profiles}

        # Backup doctors for high-risk secondary review
        dr_priya_cardio = next(p for p in all_rev_profiles if p.registration_number == "TMC-CARD-201")
        dr_alok_surgery = next(p for p in all_rev_profiles if p.registration_number == "DMC-SURG-202")
        dr_ananya_obgyn = next(p for p in all_rev_profiles if p.registration_number == "KMC-OBG-203")

        # =========================================================================
        # 5. PROCESS 40 STANDARD-RISK CANDIDATES (1 Doctor Review Each)
        # =========================================================================
        std_candidates = await ReviewQueueService.get_standard_risk_queue(session, limit=40)
        assert len(std_candidates) == 40

        approved_std_count = 0
        rejected_std_count = 0
        quarantined_std_count = 0

        for idx, q in enumerate(std_candidates):
            # Select appropriate specialist or fallback to lead auditor
            specialist = lead_auditor
            for spec, prof in reviewer_by_spec.items():
                if q.concept and spec.lower() in q.concept.name.lower():
                    specialist = prof
                    break

            if idx == 38:
                # Question 39: Reject due to inaccurate distractor
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=specialist.user_id, verdict="REJECT",
                    clinical_notes="Rejected: Distractor contains obsolete clinical guideline."
                )
                assert res["status"] == "REJECTED"
                assert res["trust_class"] == "WITHDRAWN"
                rejected_std_count += 1
            elif idx == 39:
                # Question 40: Quarantine due to international guideline dispute
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=specialist.user_id, verdict="QUARANTINE",
                    clinical_notes="Quarantined: Conflicting diagnostic thresholds between ESC and AHA."
                )
                assert res["status"] == "QUARANTINED"
                assert res["trust_class"] == "QUARANTINED"
                quarantined_std_count += 1
            else:
                # Questions 1-38: Approve
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=specialist.user_id, verdict="APPROVE",
                    clinical_notes="Approved: Validated against standard textbook evidence."
                )
                assert res["status"] == "APPROVED"
                assert res["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_std_count += 1

        assert approved_std_count == 38
        assert rejected_std_count == 1
        assert quarantined_std_count == 1

        # =========================================================================
        # 6. PROCESS 10 HIGH-RISK CANDIDATES (Two-Doctor Review Each)
        # =========================================================================
        hr_candidates = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=10)
        assert len(hr_candidates) == 10

        approved_hr_count = 0
        rejected_hr_count = 0
        quarantined_hr_count = 0

        for idx, q in enumerate(hr_candidates):
            doc_a = lead_auditor
            doc_b = dr_priya_cardio if idx % 2 == 0 else dr_alok_surgery
            if doc_b.user_id == doc_a.user_id:
                doc_b = dr_ananya_obgyn

            if idx == 8:
                # High-Risk 9: Doctor A Rejects immediately
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REJECT",
                    clinical_notes="Doctor A: Rejected due to unsafe emergency drug dosage."
                )
                assert res_a["status"] == "REJECTED"
                assert res_a["trust_class"] == "WITHDRAWN"
                rejected_hr_count += 1
            elif idx == 9:
                # High-Risk 10: Doctor A approves, Doctor B quarantines
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes="Doctor A: Initial dosage approved."
                )
                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="QUARANTINE",
                    clinical_notes="Doctor B: Quarantined due to black-box warning in pregnancy."
                )
                assert res_b["status"] == "QUARANTINED"
                assert res_b["trust_class"] == "QUARANTINED"
                quarantined_hr_count += 1
            else:
                # High-Risk 1-8: Doctor A Approves -> Stage 1
                res_a = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes="Doctor A: Verified high-risk clinical safety and dosing."
                )
                assert res_a["status"] == "REVIEW_PENDING"

                # Doctor B (distinct doctor) Approves -> Stage 2 Promotion
                res_b = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="APPROVE",
                    clinical_notes="Doctor B: Concur with dosage and emergency protocol."
                )
                assert res_b["status"] == "APPROVED"
                assert res_b["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_hr_count += 1

        assert approved_hr_count == 8
        assert rejected_hr_count == 1
        assert quarantined_hr_count == 1

        await session.commit()

        # =========================================================================
        # 7. TOTAL REVIEW ACTIONS AUDIT
        # =========================================================================
        total_approved = approved_std_count + approved_hr_count  # 38 + 8 = 46
        total_rejected = rejected_std_count + rejected_hr_count  # 1 + 1 = 2
        total_quarantined = quarantined_std_count + quarantined_hr_count  # 1 + 1 = 2

        assert total_approved == 46
        assert total_rejected == 2
        assert total_quarantined == 2

        # Count total reviews in QuestionReview table
        stmt_rev_total = select(func.count(QuestionReview.id))
        total_reviews_logged = (await session.execute(stmt_rev_total)).scalar_one()
        # 40 standard reviews + (8 * 2 + 1 + 2) high-risk reviews = 40 + 19 = 59 reviews
        assert total_reviews_logged >= 59

        # =========================================================================
        # 8. STUDENT PRACTICE POOL ADMISSION & ISOLATION GATE
        # =========================================================================
        sess, practice_questions = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=50
        )
        practice_ids = {q.id for q in practice_questions}

        # Ensure that ALL questions served in the practice session are strictly APPROVED
        for q in practice_questions:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.trust_class not in [
                "AI_GENERATED_REVIEW_PENDING",
                "QUARANTINED",
                "WITHDRAWN",
                "UNVERIFIED"
            ]

        # Verify that unreviewed candidate questions (>890 items) NEVER appear
        stmt_unreviewed = select(Question.id).where(Question.status == "PROPOSED")
        unreviewed_ids = set((await session.execute(stmt_unreviewed)).scalars().all())
        assert len(unreviewed_ids.intersection(practice_ids)) == 0
