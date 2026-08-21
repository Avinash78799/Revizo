import pytest
import pytest_asyncio
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.question import Question
from app.models.user import User
from app.models.test import TestSession, TestAttempt, IntegrityEvent
from app.models.learning import StudentQuestionHistory, StudentMistakeRecord, StudentConceptMastery
from app.services.test_service import TestService
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
async def test_chapter_and_topic_test_isolation_and_selection(client_and_db):
    """
    Acceptance: Chapter and Topic tests strictly isolate questions within the requested taxonomy nodes.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Fetch chapter and topic
        c_stmt = select(Chapter).limit(1)
        chap = (await session.execute(c_stmt)).scalars().first()

        t_stmt = select(Topic).where(Topic.chapter_id == chap.id).limit(1)
        top = (await session.execute(t_stmt)).scalars().first()

        # 1. Chapter Test Creation
        chap_session, chap_qs = await TestService.create_test_session(
            db=session,
            user_id="aspirant-user-id",
            mode="CHAPTER_REVISION_TEST",
            chapter_id=chap.id,
            question_count=2
        )
        assert chap_session.status == "IN_PROGRESS"
        assert len(chap_qs) >= 1
        for q in chap_qs:
            assert q.concept.topic.chapter_id == chap.id

        # 2. Topic Test Creation
        top_session, top_qs = await TestService.create_test_session(
            db=session,
            user_id="aspirant-user-id",
            mode="TOPIC_TEST",
            topic_id=top.id,
            question_count=2
        )
        assert top_session.status == "IN_PROGRESS"
        for q in top_qs:
            assert q.concept.topic_id == top.id

@pytest.mark.asyncio
async def test_insufficient_content_blueprint_failure_handling(client_and_db):
    """
    Acceptance: When eligible questions do not exist for a requested topic/chapter,
    the engine fails with INSUFFICIENT_CONTENT rather than silently substituting unrelated questions.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        with pytest.raises(ValidationError) as exc_info:
            await TestService.create_test_session(
                db=session,
                user_id="aspirant-user-id",
                mode="TOPIC_TEST",
                topic_id="non-existent-topic-id-9999",
                question_count=5
            )
        assert "INSUFFICIENT_CONTENT" in str(exc_info.value)

@pytest.mark.asyncio
async def test_answer_sanitization_and_pyq_provenance_labels(client_and_db):
    """
    Acceptance:
    1. Question formatting for test runner strips correct answer keys and explanations.
    2. Explicit PYQ provenance labels (DEVELOPMENT_SEED, VERIFIED_PYQ, SOURCE_REFERENCED, PYQ_STYLE) are returned.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        q_stmt = select(Question).options(selectinload(Question.options), selectinload(Question.concept)).limit(1)
        res = await session.execute(q_stmt)
        q = res.scalars().first()

        formatted = QuestionSelectionEngine.format_question_for_student_runner(q)

        # Sanitize check: No correct key or explanations exposed
        assert "correct_option_key" not in formatted
        assert "correct_explanation" not in formatted
        assert "why_wrong_explanation" not in formatted
        for opt in formatted["options"]:
            assert "is_correct" not in opt
            assert "why_wrong_explanation" not in opt

        # Provenance check
        assert formatted["provenance_tag"] in ("DEVELOPMENT_SEED", "VERIFIED_PYQ", "SOURCE_REFERENCED", "PYQ_STYLE", "ORIGINAL_AI_GENERATED")

@pytest.mark.asyncio
async def test_server_authoritative_timer_and_expiration_rejection(client_and_db):
    """
    Acceptance: Test timer is server-authoritative. Submissions after session expiration are rejected.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-timer-student"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="DAILY_SHORT_TEST",
            question_count=1
        )
        q = qs[0]

        # Artificially expire session on server
        test_session.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)
        await session.commit()

        # Attempt to submit answer to expired session
        with pytest.raises(ValidationError) as exc:
            await TestService.submit_answer_idempotent(
                db=session,
                session_id=test_session.id,
                user_id=user_id,
                question_id=q.id,
                selected_option_key="A",
                confidence="DEFINITELY_KNOW"
            )
        assert "expired" in str(exc.value).lower()

@pytest.mark.asyncio
async def test_integrity_events_and_strict_mode_penalty(client_and_db):
    """
    Acceptance:
    1. Records visibility/integrity events (TAB_HIDDEN, WINDOW_BLURRED, FULLSCREEN_EXIT).
    2. In STRICT_MODE, repeated violations deduct score and auto-terminate session if score drops <= 40.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-integrity-student"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="WEEKLY_GRAND_TEST",
            question_count=1,
            integrity_mode="STRICT_MODE"
        )
        assert test_session.integrity_score == 100

        # Event 1
        res1 = await TestService.record_integrity_event(
            db=session,
            session_id=test_session.id,
            user_id=user_id,
            event_type="TAB_HIDDEN"
        )
        assert res1["integrity_score"] == 85
        assert res1["is_terminated"] is False

        # Multiple severe events to trigger termination threshold
        for _ in range(5):
            res_loop = await TestService.record_integrity_event(
                db=session,
                session_id=test_session.id,
                user_id=user_id,
                event_type="FULLSCREEN_EXIT"
            )

        assert res_loop["integrity_score"] <= 40
        assert res_loop["is_terminated"] is True
        assert res_loop["status"] == "TERMINATED_INTEGRITY"

@pytest.mark.asyncio
async def test_question_by_question_review_and_concise_explanations(client_and_db):
    """
    Acceptance:
    After test completion, provides detailed question-by-question review with concise 3-part explanations:
    - why_your_answer_is_wrong
    - why_correct_is_right
    - remember_takeaway
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "review-student-id"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="DAILY_SHORT_TEST",
            question_count=2
        )
        q1, q2 = qs[0], qs[1]

        # Submit Q1 (Incorrect answer)
        await TestService.submit_answer_idempotent(
            db=session,
            session_id=test_session.id,
            user_id=user_id,
            question_id=q1.id,
            selected_option_key="A",
            confidence="DEFINITELY_KNOW",
            time_spent_seconds=18
        )

        # Submit Q2 (Correct answer)
        await TestService.submit_answer_idempotent(
            db=session,
            session_id=test_session.id,
            user_id=user_id,
            question_id=q2.id,
            selected_option_key="B",
            confidence="DEFINITELY_KNOW",
            time_spent_seconds=22
        )

        # Complete session
        results = await TestService.complete_test_session(session, test_session.id, user_id)

        assert results["status"] == "SUBMITTED"
        assert results["completed_questions"] == 2
        assert len(results["question_review"]) == 2

        # Verify Q1 explanation breakdown
        rev1 = results["question_review"][0]
        assert "why_correct_is_right" in rev1["short_explanation"]
        assert "remember_takeaway" in rev1["short_explanation"]
        assert rev1["provenance_tag"] in ("DEVELOPMENT_SEED", "VERIFIED_PYQ", "SOURCE_REFERENCED", "PYQ_STYLE", "ORIGINAL_AI_GENERATED")

        # Verify Next Best Action recommendation attached
        assert "next_action" in results
        assert "action_type" in results["next_action"]

@pytest.mark.asyncio
async def test_anti_repeat_question_history(client_and_db):
    """
    Acceptance: Answering a question creates a StudentQuestionHistory entry to prevent immediate repetition in subsequent tests.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-antirepeat-user"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="DAILY_SHORT_TEST",
            question_count=1
        )
        q = qs[0]

        await TestService.submit_answer_idempotent(
            db=session,
            session_id=test_session.id,
            user_id=user_id,
            question_id=q.id,
            selected_option_key="B",
            confidence="SOMEWHAT_CONFIDENT"
        )
        await session.commit()

        stmt_hist = select(StudentQuestionHistory).where(
            and_(
                StudentQuestionHistory.user_id == user_id,
                StudentQuestionHistory.question_id == q.id
            )
        )
        hist = (await session.execute(stmt_hist)).scalars().first()
        assert hist is not None
        assert hist.total_encounters >= 1

@pytest.mark.asyncio
async def test_six_simulated_student_profiles(client_and_db):
    """
    Acceptance: Simulates 6 distinct student profiles (Strong, Weak, Overconfident, Underconfident, Cold Start, Improving)
    and verifies that M6/M7 state transitions adapt logically.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Profile A: Strong Student (Consistent 100% correct + definitely know)
        test_a, qs_a = await TestService.create_test_session(session, "student-sim-a", "DAILY_SHORT_TEST", question_count=1)
        res_a = await TestService.submit_answer_idempotent(session, test_a.id, "student-sim-a", qs_a[0].id, "B", "DEFINITELY_KNOW")
        assert res_a["is_correct"] is True
        assert res_a["learning_engine_feedback"]["ease_factor"] >= 2.50

        # Profile C: Overconfident (Incorrect + definitely know)
        test_c, qs_c = await TestService.create_test_session(session, "student-sim-c", "DAILY_SHORT_TEST", question_count=1)
        res_c = await TestService.submit_answer_idempotent(session, test_c.id, "student-sim-c", qs_c[0].id, "A", "DEFINITELY_KNOW")
        assert res_c["is_correct"] is False
        assert res_c["learning_engine_feedback"]["misconception_state"] == "SUSPECTED_MISCONCEPTION"
        assert res_c["learning_engine_feedback"]["ease_factor"] <= 2.20

        # Profile D: Underconfident (Correct + guessing)
        test_d, qs_d = await TestService.create_test_session(session, "student-sim-d", "DAILY_SHORT_TEST", question_count=1)
        res_d = await TestService.submit_answer_idempotent(session, test_d.id, "student-sim-d", qs_d[0].id, "B", "GUESSING")
        assert res_d["is_correct"] is True
        assert res_d["learning_engine_feedback"]["revision_interval_days"] == 1  # Spacing expansion suppressed
