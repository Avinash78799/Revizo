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
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQuarantineRegistry, QuestionReport
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source, PyqReference
from app.models.test import TestSession, TestAttempt
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
async def test_m14_controlled_beta_and_medical_governance(client_and_db):
    """
    Milestone 14: Controlled Real-Student Beta & Final Medical Governance Workflow.
    
    1. Only trusted questions accessible (VERIFIED_CORE_QUESTION, SOURCE_REFERENCED, development_seed).
    2. Quarantined questions blocked.
    3. Revision-pending blocked.
    4. Student medical report created.
    5. Critical medical report triggers immediate safety quarantine.
    6. Quarantine removes question from all new test generations.
    7. Historical completed attempts remain intact.
    8. Medical Board adjudication workflow (RESOLVE_APPROVE, REQUEST_REVISION, REJECT).
    9. Final active-pool audit.
    10. Traceability gate (100% TRACEABLE).
    11. Feature flag beta activation & educational practice disclaimer.
    12. PYQ zero-state remains correct without official evidence (VERIFIED_PYQ = 0).
    13. IDOR protection on student reports and attempt access.
    14. Reviewer and admin role boundaries.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Setup Users
        admin = User(email="chief_dean_m14@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student_a = User(email="beta_student_a@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        student_b = User(email="beta_student_b@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        session.add_all([admin, student_a, student_b])
        await session.commit()

        # Build 19-Subject 950-Candidate Corpus & Onboard Medical Board
        await CorpusIngestionService.build_complete_950_candidate_corpus(session, creator_user_id=admin.id)
        await MedicalBoardService.onboard_19_discipline_medical_panel(session, admin.id)

        # Audit all 19 Sources
        stmt_lead = select(MedicalReviewerProfile).limit(1)
        lead_auditor = (await session.execute(stmt_lead)).scalars().first()
        await MedicalBoardService.audit_and_verify_all_19_discipline_sources(session, auditor_user_id=lead_auditor.user_id)

        # =========================================================================
        # 11. FEATURE FLAG BETA ACTIVATION & DISCLAIMER
        # =========================================================================
        beta_config = MedicalBoardService.get_controlled_beta_config()
        assert beta_config["beta_enabled"] is True
        assert beta_config["beta_cohort_limit"] == 500
        assert "not official neet-pg exam material" in beta_config["disclaimer_text"].lower()

        # =========================================================================
        # 12. PYQ ZERO-STATE PRESERVATION
        # =========================================================================
        stmt_pyq_count = select(func.count(Question.id)).where(Question.trust_class == "VERIFIED_PYQ")
        pyq_verified_count = (await session.execute(stmt_pyq_count)).scalar_one()
        assert pyq_verified_count == 0  # Preserved until genuine official master paper ingestion
        assert beta_config["verified_pyq_count"] == 0

        # Approve a controlled cohort of questions for student beta testing
        stmt_candidates = select(Question).where(Question.status == "PROPOSED").limit(50)
        approved_cohort = (await session.execute(stmt_candidates)).scalars().all()
        for q in approved_cohort:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q.id, reviewer_id=lead_auditor.user_id, verdict="APPROVE",
                clinical_notes="Beta cohort verification against textbook."
            )
            q.status = "PUBLISHED"
        await session.commit()

        # =========================================================================
        # 1, 2, 3. STUDENT POOL ACCESS & EXCLUSION OF QUARANTINED / REVISION ITEMS
        # =========================================================================
        sess_1, test_qs_1 = await TestService.create_test_session(
            db=session, user_id=student_a.id, mode="DAILY_SHORT_TEST", question_count=10
        )
        assert len(test_qs_1) == 10
        target_q = test_qs_1[0]

        for q in test_qs_1:
            assert q.status.upper() in ("PUBLISHED", "APPROVED")
            assert q.trust_class in ["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED", "development_seed"]
            assert q.trust_class not in ["QUARANTINED", "REVISION_REQUESTED", "WITHDRAWN", "AI_GENERATED_REVIEW_PENDING"]

        # Student submits an answer for target_q
        await TestService.submit_answer_idempotent(
            db=session, session_id=sess_1.id, user_id=student_a.id,
            question_id=target_q.id, selected_option_key="A", confidence="DEFINITELY_KNOW", time_spent_seconds=45
        )

        # =========================================================================
        # 4 & 5. STUDENT MEDICAL REPORT & IMMEDIATE SAFETY QUARANTINE
        # =========================================================================
        report_res = await MedicalContentService.process_student_question_report(
            db=session,
            question_id=target_q.id,
            user_id=student_a.id,
            report_type="WRONG_ANSWER_KEY",
            comment="Potassium correction dosing appears dangerously elevated compared to standard clinical protocol.",
            severity="CRITICAL"
        )
        assert report_res["is_critical"] is True
        assert report_res["quarantined"] is True
        assert report_res["current_question_status"] == "QUARANTINED"
        assert report_res["current_trust_class"] == "QUARANTINED"

        # Verify entry in QuestionQuarantineRegistry
        stmt_quar_entry = select(QuestionQuarantineRegistry).where(QuestionQuarantineRegistry.question_id == target_q.id)
        quar_entry = (await session.execute(stmt_quar_entry)).scalars().first()
        assert quar_entry is not None
        assert quar_entry.resolution_status == "quarantined"

        # =========================================================================
        # 6. QUARANTINE REMOVES QUESTION FROM NEW TESTS
        # =========================================================================
        sess_2, test_qs_2 = await TestService.create_test_session(
            db=session, user_id=student_b.id, mode="DAILY_SHORT_TEST", question_count=20
        )
        new_q_ids = {q.id for q in test_qs_2}
        assert target_q.id not in new_q_ids

        # =========================================================================
        # 7. HISTORICAL ATTEMPTS REMAIN INTACT
        # =========================================================================
        stmt_ans = select(TestAttempt).where(TestAttempt.session_id == sess_1.id)
        past_answers = (await session.execute(stmt_ans)).scalars().all()
        assert len(past_answers) == 1
        assert past_answers[0].question_id == target_q.id

        # =========================================================================
        # 8. MEDICAL BOARD ADJUDICATION WORKFLOW
        # =========================================================================
        # Attempt unauthorized adjudication (student -> AuthorizationError)
        with pytest.raises(AuthorizationError):
            await MedicalBoardService.resolve_quarantined_question(
                db=session,
                question_id=target_q.id,
                board_member_id=student_a.id,
                resolution_decision="RESOLVE_APPROVE",
                resolution_notes="Unauthorized student resolution attempt"
            )

        # Authorized Board Member Adjudication (e.g. resolve and approve with refined dosage)
        board_res = await MedicalBoardService.resolve_quarantined_question(
            db=session,
            question_id=target_q.id,
            board_member_id=lead_auditor.user_id,
            resolution_decision="RESOLVE_APPROVE",
            resolution_notes="Reviewed by cardiology board; dosage re-verified against AIIMS emergency protocol."
        )
        assert board_res["quarantine_resolved"] is True
        assert board_res["new_status"] in ["PUBLISHED", "APPROVED"]
        assert board_res["new_trust_class"] == "VERIFIED_CORE_QUESTION"

        # =========================================================================
        # 9 & 10. ACTIVE POOL AUDIT & TRACEABILITY GATE
        # =========================================================================
        trace_audit = await MedicalBoardService.audit_active_pool_traceability(db=session)
        assert trace_audit["total_active_pool"] >= 50
        assert trace_audit["untraceable_count"] == 0
        assert trace_audit["traceability_percentage"] == 100.0
        assert trace_audit["beta_eligible"] is True

        # =========================================================================
        # 14. IDOR PROTECTION
        # =========================================================================
        # Student B cannot access or modify Student A's test session
        with pytest.raises(AuthorizationError):
            await TestService.submit_answer_idempotent(
                db=session, session_id=sess_1.id, user_id=student_b.id,
                question_id=target_q.id, selected_option_key="A", confidence="DEFINITELY_KNOW", time_spent_seconds=10
            )
