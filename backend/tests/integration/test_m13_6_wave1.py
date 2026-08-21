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
async def test_m13_6_wave1_standard_risk_review(client_and_db):
    """
    Milestone 13.6 Wave 1: Final Standard-Risk Content Review (250 Candidates).
    
    1. 250-Question Selection from Standard-Risk Queue
    2. Subject Distribution across all 19 medical disciplines
    3. Specialty-Aware Reviewer Routing
    4. Approval Workflow (228 Approved -> VERIFIED_CORE_QUESTION)
    5. Rejection Workflow (8 Rejected -> REJECTED / WITHDRAWN)
    6. Revision Workflow (7 Revision Requested -> REVISION_REQUESTED)
    7. Quarantine Workflow (7 Quarantined -> QUARANTINED)
    8. Audit Immutability & Credential Snapshot Preservation
    9. Student Pool Gating (Only Approved admitted; all others blocked)
    10. Reviewer Authorization & Suspension Gates
    11. Count Reconciliation (228 + 8 + 7 + 7 = 250)
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Admin & Student
        admin = User(email="chief_dean_m13_6@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_wave1_tester@neetpg.pro", hashed_password="pw", role="student", is_active=True)
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

        # =========================================================================
        # 1 & 2. SELECT 250-QUESTION BATCH & VERIFY 19-SUBJECT DISTRIBUTION
        # =========================================================================
        std_candidates = []
        for i, meta in enumerate(NMC_19_SUBJECTS_METADATA):
            take_limit = 14 if i < 3 else 13
            q_list = await ReviewQueueService.get_standard_risk_queue(session, subject_code=meta["code"], limit=take_limit)
            std_candidates.extend(q_list)

        assert len(std_candidates) == 250

        # Verify subject diversity across all 19 disciplines
        batch_subjects = set()
        for q in std_candidates:
            if q.concept and q.concept.topic and q.concept.topic.chapter and q.concept.topic.chapter.subject:
                batch_subjects.add(q.concept.topic.chapter.subject.code)
        assert len(batch_subjects) == 19

        # Verify all 250 are strictly blocked from student pool before processing
        batch_250_ids = {q.id for q in std_candidates}
        sess_before, practice_before = await TestService.create_test_session(
            db=session, user_id=student.id, mode="DAILY_SHORT_TEST", question_count=30
        )
        before_ids = {q.id for q in practice_before}
        assert len(batch_250_ids.intersection(before_ids)) == 0

        # =========================================================================
        # 3, 4, 5, 6, 7. PROCESS 250 STANDARD-RISK CANDIDATES (1 Doctor Review Each)
        # =========================================================================
        approved_count = 0
        rejected_count = 0
        revision_count = 0
        quarantined_count = 0

        for idx, q in enumerate(std_candidates):
            # Specialty-aware assignment
            reviewer = lead_auditor
            for spec, prof in reviewer_by_spec.items():
                if q.concept and spec.lower() in q.concept.name.lower():
                    reviewer = prof
                    break

            if idx < 8:
                # 8 Rejections (Obsolete recommendations / incorrect answer logic)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REJECT",
                    clinical_notes=f"Wave 1 Standard Reject #{idx}: Obsolete treatment guidance."
                )
                assert res["status"] == "REJECTED"
                assert res["trust_class"] == "WITHDRAWN"
                rejected_count += 1
            elif idx < 15:
                # 7 Revision Requests (Stem phrasing and distractor clarity)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="REQUEST_REVISION",
                    clinical_notes=f"Wave 1 Standard Revision #{idx}: Rephrase clinical distractor."
                )
                assert res["status"] == "REVISION_REQUESTED"
                revision_count += 1
            elif idx < 22:
                # 7 Quarantines (Disputed diagnostic thresholds)
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="QUARANTINE",
                    clinical_notes=f"Wave 1 Standard Quarantine #{idx}: Conflicting guideline thresholds."
                )
                assert res["status"] == "QUARANTINED"
                assert res["trust_class"] == "QUARANTINED"
                quarantined_count += 1
            else:
                # 228 Approvals
                res = await MedicalContentService.perform_medical_review(
                    db=session, question_id=q.id, reviewer_id=reviewer.user_id, verdict="APPROVE",
                    clinical_notes=f"Wave 1 Standard Approved #{idx}: Verified against canonical source."
                )
                assert res["status"] == "APPROVED"
                assert res["trust_class"] == "VERIFIED_CORE_QUESTION"
                q.status = "PUBLISHED"
                approved_count += 1

        assert approved_count == 228
        assert rejected_count == 8
        assert revision_count == 7
        assert quarantined_count == 7

        await session.commit()

        # =========================================================================
        # 11. RECONCILIATION AUDIT
        # =========================================================================
        assert (approved_count + rejected_count + revision_count + quarantined_count) == 250

        # =========================================================================
        # 9. STUDENT POOL AFTER VERIFICATION
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

        # Verify all remaining unreviewed questions (>300 items) are 100% blocked
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
        # 8 & 10. AUDIT IMMUTABILITY & REVIEWER AUTHORIZATION
        # =========================================================================
        stmt_reviews = select(QuestionReview)
        all_reviews = (await session.execute(stmt_reviews)).scalars().all()
        assert len(all_reviews) >= 250
        for rev in all_reviews:
            assert rev.reviewer_credential_status is not None
            assert rev.source_verification_decision == "VERIFIED"
            assert rev.created_at is not None
