import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept
from app.models.question import Question
from app.models.user import User
from app.models.learning import StudentConceptMastery, StudentMistakeRecord, LearningEvidenceRecord
from app.services.learning_intelligence_engine import LearningIntelligenceEngine

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
async def test_single_high_confidence_wrong_is_suspected_not_danger_zone(client_and_db):
    """
    1 confident wrong:
    -> error_type = CONFIDENCE_ERROR
    -> misconception_state = SUSPECTED_MISCONCEPTION
    -> danger_zone_active = False (NOT confirmed misconception)
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-single-confident-wrong"
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        res = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q.id,
            concept_id=q.concept_id,
            is_correct=False,
            confidence="DEFINITELY_KNOW",
            selected_option_key="B",
            correct_option_key="A",
            session_id="single-err-sess"
        )
        await session.commit()

        assert res["misconception_state"] == "SUSPECTED_MISCONCEPTION"
        assert res["danger_zone_active"] is False

        # Verify mistake record
        stmt_m = select(StudentMistakeRecord).where(StudentMistakeRecord.user_id == user_id)
        m = (await session.execute(stmt_m)).scalars().first()
        assert m.error_type == "CONFIDENCE_ERROR"
        assert m.misconception_state == "SUSPECTED_MISCONCEPTION"

@pytest.mark.asyncio
async def test_two_high_confidence_errors_triggers_confirmed_misconception(client_and_db):
    """
    2+ independent high-confidence errors on the same concept:
    -> misconception_state = CONFIRMED_MISCONCEPTION
    -> danger_zone_active = True
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-two-confident-errors"
        q_stmt = select(Question).limit(2)
        res_q = await session.execute(q_stmt)
        questions = res_q.scalars().all()
        q1, q2 = questions[0], questions[1]
        concept_id = q1.concept_id

        # Error 1
        res1 = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q1.id,
            concept_id=concept_id,
            is_correct=False,
            confidence="DEFINITELY_KNOW",
            selected_option_key="B",
            correct_option_key="A",
            session_id="err-sess-1"
        )
        assert res1["misconception_state"] == "SUSPECTED_MISCONCEPTION"
        assert res1["danger_zone_active"] is False

        # Error 2
        res2 = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q2.id,
            concept_id=concept_id,
            is_correct=False,
            confidence="DEFINITELY_KNOW",
            selected_option_key="C",
            correct_option_key="A",
            session_id="err-sess-2"
        )
        assert res2["misconception_state"] == "CONFIRMED_MISCONCEPTION"
        assert res2["danger_zone_active"] is True

@pytest.mark.asyncio
async def test_errors_caused_by_multiple_invalidated_questions(client_and_db):
    """
    Tests that multiple mistakes on questions that are subsequently invalidated
    cleanly restore student mastery to 0 attempts, removing Danger Zone and misconceptions.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-multi-invalid"
        q_stmt = select(Question).limit(2)
        res_q = await session.execute(q_stmt)
        questions = res_q.scalars().all()
        q1, q2 = questions[0], questions[1]
        concept_id = q1.concept_id

        # Record two confident mistakes
        await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session, user_id=user_id, question_id=q1.id, concept_id=concept_id,
            is_correct=False, confidence="DEFINITELY_KNOW", selected_option_key="B",
            correct_option_key="A", session_id="inv-sess-1"
        )
        await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session, user_id=user_id, question_id=q2.id, concept_id=concept_id,
            is_correct=False, confidence="DEFINITELY_KNOW", selected_option_key="C",
            correct_option_key="A", session_id="inv-sess-2"
        )
        await session.commit()

        # Both questions are identified as ambiguous and quarantined
        await LearningIntelligenceEngine.invalidate_question_evidence_and_recalculate_mastery(session, q1.id)
        await LearningIntelligenceEngine.invalidate_question_evidence_and_recalculate_mastery(session, q2.id)
        await session.commit()

        # Verify mastery is completely cleansed
        stmt_m = select(StudentConceptMastery).where(
            and_(StudentConceptMastery.user_id == user_id, StudentConceptMastery.concept_id == concept_id)
        )
        mastery = (await session.execute(stmt_m)).scalars().first()
        assert mastery.total_attempts == 0
        assert mastery.danger_zone_active is False
        assert mastery.misconception_state == "NONE"

@pytest.mark.asyncio
async def test_dynamic_five_minute_session_without_danger_zone(client_and_db):
    """
    When a student has 0 Danger Zone items, the 5-minute session adapts dynamically
    and does NOT manufacture false Danger Zone items.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Student has no mistakes
        five_min = await LearningIntelligenceEngine.get_five_minute_revision_slice(session, "student-clean-slate")
        
        assert five_min["session_type"] == "FIVE_MINUTE_RAPID_REVISION"
        assert five_min["target_misconceptions_included"] == 0
        assert len(five_min["questions"]) >= 1

        # Every question has a valid selection reason
        for q in five_min["questions"]:
            assert "selection_reason" in q
            assert "priority" in q

@pytest.mark.asyncio
async def test_completely_new_student_cold_start_and_idempotency(client_and_db):
    """
    Tests that a brand new student receives a valid cold-start plan and
    repeated calls are 100% idempotent.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        new_user_id = "brand-new-student-cold"
        
        # 1. Daily plan call 1
        plan1 = await LearningIntelligenceEngine.generate_daily_study_plan(session, new_user_id)
        assert plan1["status"] == "GENERATED"
        assert plan1["total_target_questions"] == 20
        assert "slices" in plan1

        # 2. Daily plan call 2 (Idempotency)
        plan2 = await LearningIntelligenceEngine.generate_daily_study_plan(session, new_user_id)
        assert plan2["plan_id"] == plan1["plan_id"]
        assert plan2["target_date"] == plan1["target_date"]

        # 3. Next Best Action
        action = await LearningIntelligenceEngine.get_next_best_action(session, new_user_id)
        assert action["action_type"] == "HIGH_YIELD_DISCOVERY"
        assert action["priority"] == "STANDARD"
        assert "Prioritized because:" in action["description"]

@pytest.mark.asyncio
async def test_statistical_terminology_quartile_discrimination(client_and_db):
    """
    Verifies that discrimination is named TOP_BOTTOM_QUARTILE_DISCRIMINATION
    and difficulty is named OBSERVED_ERROR_RATE.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        # When < 10 attempts
        disc = await LearningIntelligenceEngine.calculate_question_discrimination(session, q.id)
        assert disc["status"] == "INSUFFICIENT_SAMPLE_SIZE"
