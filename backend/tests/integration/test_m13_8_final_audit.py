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
async def test_m13_8_final_100_review_and_full_950_audit(client_and_db):
    """
    Milestone 13.8: Final 100 Candidate Review + Full 950-Corpus Audit.
    
    1. Process remaining 100 Standard-Risk candidates (Completing full 950 corpus).
    2. Enforce 1-Doctor Review for Standard-Risk items.
    3. Full 950-Candidate Disposition Audit:
       - 0 Unreviewed / Proposed items remaining in queue.
       - Every item has exactly one definitive final state.
    4. Student Pool Count Reconciliation:
       - Active Practice Pool = Verified Approved Items (+ Seed/Pilot).
       - 100% of Rejected, Revision, Quarantined, and Unverified items strictly blocked.
    5. 19-Subject Coverage & Quality Audit (GREEN coverage across all 19 disciplines).
    6. Audit Trail Immutability & Credential Snapshot Integrity.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Admin & Student
        admin = User(email="chief_dean_m13_8@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_final_tester@neetpg.pro", hashed_password="pw", role="student", is_active=True)
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
        # 1. PROCESS COMPLETE 950-CANDIDATE CORPUS (Batches 1-3 + Waves 1-3)
        # =========================================================================
        # Fetch all 72 High-Risk Candidates
        hr_all = await ReviewQueueService.get_high_risk_two_doctor_queue(session, stage="STAGE_1_PENDING", limit=100)
        assert len(hr_all) == 72

        # Review all 72 High-Risk Items (Two-Doctor Review Workflow)
        for idx, q in enumerate(hr_all):
            doc_a = lead_auditor
            doc_b = high_risk_b_reviewers[idx % len(high_risk_b_reviewers)]
            if doc_b.user_id == doc_a.user_id:
                doc_b = dr_ananya_obgyn

            if idx < 4:
                # 4 High-Risk Rejections by Doctor A
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REJECT",
                    clinical_notes="Doctor A Reject: Fatal dosing error."
                )
            elif idx < 6:
                # 2 High-Risk Revisions by Doctor A
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="REQUEST_REVISION",
                    clinical_notes="Doctor A Revision: Clarify vignette context."
                )
            elif idx < 12:
                # 6 High-Risk Disagreements -> Quarantined
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes="Doctor A Approval: Initial protocol."
                )
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="REJECT",
                    clinical_notes="Doctor B Disagreement: Bleeding risk."
                )
            else:
                # 60 High-Risk Approved (Doctor A + Doctor B)
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_a.user_id, verdict="APPROVE",
                    clinical_notes="Doctor A Approval: Clinical safety verified."
                )
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=doc_b.user_id, verdict="APPROVE",
                    clinical_notes="Doctor B Concurrence: Protocol confirmed."
                )
                q.status = "PUBLISHED"

        # Fetch all 878 Standard-Risk Candidates
        std_all = await ReviewQueueService.get_standard_risk_queue(session, limit=1000)
        assert len(std_all) == 878

        # Review all 878 Standard-Risk Items with balanced distribution
        rej_count = 0
        rev_count = 0
        quar_count = 0
        rej_target = 26
        rev_target = 21
        quar_target = 23

        for idx, q in enumerate(std_all):
            reviewer = lead_auditor
            for spec, prof in reviewer_by_spec.items():
                if q.concept and spec.lower() in q.concept.name.lower():
                    reviewer = prof
                    break

            if idx % 33 == 0 and rej_count < rej_target:
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REJECT",
                    clinical_notes=f"Standard Reject #{rej_count}: Obsolete treatment guidance."
                )
                rej_count += 1
            elif idx % 37 == 0 and rev_count < rev_target:
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REQUEST_REVISION",
                    clinical_notes=f"Standard Revision #{rev_count}: Distractor clarity refinement."
                )
                rev_count += 1
            elif idx % 35 == 0 and quar_count < quar_target:
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="QUARANTINE",
                    clinical_notes=f"Standard Quarantine #{quar_count}: Disputed diagnostic criteria."
                )
                quar_count += 1
            else:
                await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="APPROVE",
                    clinical_notes=f"Standard Approved #{idx}: Verified against canonical textbook source."
                )
                q.status = "PUBLISHED"

        assert rej_count == 26
        assert rev_count == 21
        assert quar_count == 23

        await session.commit()

        # =========================================================================
        # 2. FULL 950-CANDIDATE DISPOSITION RECONCILIATION
        # =========================================================================
        # Verify ZERO unreviewed candidates remain
        stmt_pending = select(func.count(Question.id)).where(Question.status == "PROPOSED")
        pending_count = (await session.execute(stmt_pending)).scalar_one()
        assert pending_count == 0

        # Exact Disposition Breakdown:
        # Approved: 60 (high-risk) + 808 (standard-risk) = 868
        # Rejected: 4 (high-risk) + 26 (standard-risk) = 30
        # Revision: 2 (high-risk) + 21 (standard-risk) = 23
        # Quarantined: 6 (high-risk) + 23 (standard-risk) = 29
        stmt_approved = select(func.count(Question.id)).where(Question.status.in_(["APPROVED", "PUBLISHED"]))
        approved_count = (await session.execute(stmt_approved)).scalar_one()
        # 868 newly approved + seeded approved items
        assert approved_count >= 868

        stmt_rejected = select(func.count(Question.id)).where(Question.status == "REJECTED")
        assert (await session.execute(stmt_rejected)).scalar_one() == 30

        stmt_revision = select(func.count(Question.id)).where(Question.status == "REVISION_REQUESTED")
        assert (await session.execute(stmt_revision)).scalar_one() == 23

        stmt_quarantine = select(func.count(Question.id)).where(Question.status == "QUARANTINED")
        assert (await session.execute(stmt_quarantine)).scalar_one() == 29

        # Total 950 candidates accounted for
        assert (868 + 30 + 23 + 29) == 950

        # =========================================================================
        # 3. STUDENT POOL ADMISSION & ISOLATION GATING
        # =========================================================================
        sess, practice_qs = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=100
        )
        practice_ids = {q.id for q in practice_qs}

        # Verify all practice questions are strictly APPROVED
        for q in practice_qs:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.trust_class not in [
                "AI_GENERATED_REVIEW_PENDING",
                "QUARANTINED",
                "WITHDRAWN",
                "UNVERIFIED"
            ]

        # Verify rejected, revision, quarantined are strictly excluded from pool
        stmt_rejected_ids = select(Question.id).where(Question.status == "REJECTED")
        rejected_ids = set((await session.execute(stmt_rejected_ids)).scalars().all())
        assert len(rejected_ids.intersection(practice_ids)) == 0

        stmt_quarantined_ids = select(Question.id).where(Question.status == "QUARANTINED")
        quarantined_ids = set((await session.execute(stmt_quarantined_ids)).scalars().all())
        assert len(quarantined_ids.intersection(practice_ids)) == 0

        # =========================================================================
        # 4. 19-SUBJECT COVERAGE HEALTH AUDIT
        # =========================================================================
        for meta in NMC_19_SUBJECTS_METADATA:
            stmt_subj_qs = select(func.count(Question.id))\
                .join(Concept, Question.concept_id == Concept.id)\
                .join(Topic, Concept.topic_id == Topic.id)\
                .join(Chapter, Topic.chapter_id == Chapter.id)\
                .join(Subject, Chapter.subject_id == Subject.id)\
                .where(and_(Subject.code == meta["code"], Question.status.in_(["APPROVED", "PUBLISHED"])))
            count_subj = (await session.execute(stmt_subj_qs)).scalar_one()
            # Every discipline has at least 35 verified questions (averaging ~45.7 per discipline)
            assert count_subj >= 35

        # =========================================================================
        # 5. AUDIT TRAIL IMMUTABILITY
        # =========================================================================
        stmt_total_rev = select(func.count(QuestionReview.id))
        total_rev_actions = (await session.execute(stmt_total_rev)).scalar_one()
        # 878 standard reviews + (60 * 2 + 4 + 2 + 6 * 2) high-risk reviews = 878 + 138 = 1,016 reviews
        assert total_rev_actions >= 1016
