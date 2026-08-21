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
async def test_integrity_severity_model_and_zero_network_penalty(client_and_db):
    """
    Acceptance:
    - NETWORK_INTERRUPTION has severity weight 0 (0 penalty)
    - WINDOW_BLURRED has severity weight 1
    - TAB_HIDDEN has severity weight 3
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-sev-user"
        test_session, _ = await TestService.create_test_session(
            db=session, user_id=user_id, mode="WEEKLY_GRAND_TEST", question_count=10, integrity_mode="STRICT_MODE"
        )
        assert test_session.integrity_score == 100

        # Network interruption (0 penalty)
        res_net = await TestService.record_integrity_event(
            db=session, session_id=test_session.id, user_id=user_id, event_type="NETWORK_INTERRUPTION"
        )
        assert res_net["event_severity_weight"] == 0
        assert res_net["integrity_score"] == 100  # No score deduction

        # Window blurred (1 * 5 = 5 penalty)
        res_blur = await TestService.record_integrity_event(
            db=session, session_id=test_session.id, user_id=user_id, event_type="WINDOW_BLURRED"
        )
        assert res_blur["event_severity_weight"] == 1
        assert res_blur["integrity_score"] == 95

        # Tab hidden (3 * 5 = 15 penalty)
        res_tab = await TestService.record_integrity_event(
            db=session, session_id=test_session.id, user_id=user_id, event_type="TAB_HIDDEN"
        )
        assert res_tab["event_severity_weight"] == 3
        assert res_tab["integrity_score"] == 80

@pytest.mark.asyncio
async def test_integrity_does_not_alter_academic_score(client_and_db):
    """
    Acceptance: Integrity events strictly NEVER alter academic score, correctness, or mastery.
    Academic performance and integrity tracking are decoupled.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-decoupled-student"
        test_session, qs = await TestService.create_test_session(
            db=session, user_id=user_id, mode="DAILY_SHORT_TEST", question_count=10, integrity_mode="WARNING_MODE"
        )
        q = qs[0]

        # Submit correct answer (+4 marks)
        sub = await TestService.submit_answer_idempotent(
            db=session, session_id=test_session.id, user_id=user_id, question_id=q.id,
            selected_option_key="B", confidence="DEFINITELY_KNOW"
        )
        assert sub["is_correct"] is True

        # Incur 10 integrity events
        for _ in range(10):
            await TestService.record_integrity_event(
                db=session, session_id=test_session.id, user_id=user_id, event_type="WINDOW_BLURRED"
            )

        # Complete test and verify academic score is preserved at +4
        res = await TestService.complete_test_session(session, test_session.id, user_id)
        assert res["score"] == 4
        assert res["accuracy_percentage"] == 100.0

@pytest.mark.asyncio
async def test_m6_revision_overrides_anti_repeat_policy(client_and_db):
    """
    Acceptance:
    Routine practice avoids recently seen questions (<= 7 days).
    BUT M6 learning evidence (Danger Zone, Mistake Retest, Due Revision) explicitly overrides it.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-override-student"
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        # Step 1: Create a recent encounter (seen today)
        hist = StudentQuestionHistory(
            user_id=user_id,
            question_id=q.id,
            total_encounters=1,
            last_encountered_at=datetime.now(timezone.utc)
        )
        session.add(hist)

        # Step 2: Trigger Danger Zone for this concept
        mastery = StudentConceptMastery(
            user_id=user_id,
            concept_id=q.concept_id,
            danger_zone_active=True,
            high_confidence_wrong_count=2
        )
        session.add(mastery)
        await session.commit()

        # Step 3: Danger Zone Retest selection explicitly overrides anti-repeat
        selected_qs, override_reason = await QuestionSelectionEngine.select_questions_for_test(
            db=session,
            user_id=user_id,
            mode="DANGER_ZONE_RETEST",
            question_count=10
        )
        assert len(selected_qs) >= 1
        assert override_reason == "M6_DANGER_ZONE_OVERRIDE"

@pytest.mark.asyncio
async def test_weekly_grand_test_reproducibility_and_ranking_safeguards(client_and_db):
    """
    Acceptance:
    1. Weekly Grand Test stores full test reproducibility snapshot (gt-blueprint-v1.0, question hashes, versions).
    2. Cohort ranking on small sample sizes (N < 20) flags is_statistically_authoritative=False.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-repro-student"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="WEEKLY_GRAND_TEST",
            question_count=10
        )
        await session.commit()

        # Verify reproducibility snapshot
        snap = test_session.test_reproducibility_snapshot
        assert snap["blueprint_version"] == "gt-blueprint-v1.0"
        assert snap["selection_strategy_version"] == "selection-v1.0"
        assert snap["algorithm_version"] == "adaptive-v1.0"
        assert len(snap["question_ids"]) == 10
        assert len(snap["question_versions"]) == 10

        # Complete test and verify ranking output
        res = await TestService.complete_test_session(session, test_session.id, user_id)
        assert "ranking" in res
        assert res["ranking"]["is_statistically_authoritative"] is False
        assert "small" in res["ranking"]["disclaimer"].lower()

@pytest.mark.asyncio
async def test_offline_client_cannot_extend_server_authoritative_timer(client_and_db):
    """
    Acceptance: Reconnection after server expiration is rejected regardless of client clock.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-clock-student"
        test_session, qs = await TestService.create_test_session(
            db=session, user_id=user_id, mode="DAILY_SHORT_TEST", question_count=10
        )
        q = qs[0]

        # Server expiration time elapsed
        test_session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=10)
        await session.commit()

        # Submission rejected by server authority
        with pytest.raises(ValidationError) as exc:
            await TestService.submit_answer_idempotent(
                db=session, session_id=test_session.id, user_id=user_id,
                question_id=q.id, selected_option_key="B"
            )
        assert "expired" in str(exc.value).lower()
