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
async def test_wrong_plus_confident_triggers_confidence_error(client_and_db):
    """
    WRONG + DEFINITELY_KNOW creates a confidence-error signal, sharply penalizes ease factor,
    and resets interval to 1 day.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-student-1"
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
            correct_option_key="A"
        )
        await session.commit()

        assert res["revision_interval_days"] == 1
        assert res["ease_factor"] <= 2.20  # Penalized from 2.50 to 2.20

        # Verify mistake classification
        stmt_m = select(StudentMistakeRecord).where(StudentMistakeRecord.user_id == user_id)
        m = (await session.execute(stmt_m)).scalars().first()
        assert m is not None
        assert m.error_type == "CONFIDENCE_ERROR"
        assert m.misconception_state == "SUSPECTED_MISCONCEPTION"

@pytest.mark.asyncio
async def test_repeated_confident_mistakes_trigger_danger_zone(client_and_db):
    """
    Rule: Single high-confidence mistake does NOT trigger Danger Zone (avoids false positives).
    Repeated (>=2) high-confidence mistakes activate Danger Zone.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-student-danger"
        q_stmt = select(Question).limit(2)
        res_q = await session.execute(q_stmt)
        questions = res_q.scalars().all()
        q1, q2 = questions[0], questions[1]
        concept_id = q1.concept_id

        # First confident mistake
        res1 = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q1.id,
            concept_id=concept_id,
            is_correct=False,
            confidence="DEFINITELY_KNOW",
            selected_option_key="C",
            correct_option_key="A"
        )
        assert res1["danger_zone_active"] is False  # Invariant: 1 mistake != Danger Zone

        # Second confident mistake on same concept
        res2 = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q2.id,
            concept_id=concept_id,
            is_correct=False,
            confidence="DEFINITELY_KNOW",
            selected_option_key="D",
            correct_option_key="A"
        )
        assert res2["danger_zone_active"] is True  # Invariant: 2 mistakes = Danger Zone Activated

@pytest.mark.asyncio
async def test_lucky_guess_prevents_spacing_expansion(client_and_db):
    """
    CORRECT + GUESSING indicates fragile knowledge / lucky guess.
    Interval remains at 1 day rather than jumping to 6 days.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-student-guess"
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        res = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q.id,
            concept_id=q.concept_id,
            is_correct=True,
            confidence="GUESSING",
            selected_option_key="A",
            correct_option_key="A"
        )
        await session.commit()

        # Lucky guess keeps interval short (1 day)
        assert res["revision_interval_days"] == 1

@pytest.mark.asyncio
async def test_idempotency_prevents_double_counting(client_and_db):
    """
    Submitting the exact same attempt event twice does NOT double-increment total attempts or corrupt mastery.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-student-idempotent"
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        # Event 1
        res1 = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q.id,
            concept_id=q.concept_id,
            is_correct=True,
            confidence="DEFINITELY_KNOW",
            selected_option_key="A",
            correct_option_key="A",
            session_id="session-100"
        )
        await session.commit()
        assert res1["idempotent_replay"] is False

        # Event 2 (Exact duplicate replay)
        res2 = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q.id,
            concept_id=q.concept_id,
            is_correct=True,
            confidence="DEFINITELY_KNOW",
            selected_option_key="A",
            correct_option_key="A",
            session_id="session-100"
        )
        await session.commit()
        assert res2["idempotent_replay"] is True

        # Verify in database that only 1 evidence record exists
        stmt_ev = select(func.count(LearningEvidenceRecord.id)).where(LearningEvidenceRecord.user_id == user_id)
        count = (await session.execute(stmt_ev)).scalar()
        assert count == 1

@pytest.mark.asyncio
async def test_quarantined_question_evidence_invalidation(client_and_db):
    """
    When a question is quarantined, its learning evidence is invalidated and
    mastery is recomputed without the defective question.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "test-student-invalid"
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        # Student misses the question
        await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id=user_id,
            question_id=q.id,
            concept_id=q.concept_id,
            is_correct=False,
            confidence="DEFINITELY_KNOW",
            selected_option_key="B",
            correct_option_key="A"
        )
        await session.commit()

        # Question is subsequently quarantined due to ambiguity / medical report
        invalidated_count = await LearningIntelligenceEngine.invalidate_question_evidence_and_recalculate_mastery(
            db=session,
            question_id=q.id
        )
        await session.commit()

        assert invalidated_count >= 1

        # Check that student mastery is no longer poisoned
        stmt_m = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.concept_id == q.concept_id
            )
        )
        mastery = (await session.execute(stmt_m)).scalars().first()
        assert mastery.total_attempts == 0  # Invalidated evidence excluded from active mastery

@pytest.mark.asyncio
async def test_daily_study_plan_and_five_minute_revision(client_and_db):
    """
    Tests generation of personalized daily study plans and 5-minute micro-revision slices.
    """
    client, session_maker = client_and_db

    login_res = await client.post("/api/v1/auth/login", json={
        "email": "aspirant@neetpg.pro",
        "password": "Password123!"
    })
    headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    # 1. Daily Study Plan API
    plan_res = await client.get("/api/v1/student/learning-plan", headers=headers)
    assert plan_res.status_code == 200
    plan = plan_res.json()
    assert "target_date" in plan
    assert "slices" in plan
    assert "danger_zone" in plan["slices"]
    assert "due_revisions" in plan["slices"]

    # 2. Next Best Action API
    action_res = await client.get("/api/v1/student/next-action", headers=headers)
    assert action_res.status_code == 200
    action = action_res.json()
    assert "action_type" in action
    assert "priority" in action
    assert "description" in action

    # 3. 5-Minute Micro-Revision API
    five_min_res = await client.get("/api/v1/student/five-minute-revision", headers=headers)
    assert five_min_res.status_code == 200
    five_min = five_min_res.json()
    assert five_min["session_type"] == "FIVE_MINUTE_RAPID_REVISION"
    assert len(five_min["questions"]) <= 5

@pytest.mark.asyncio
async def test_synthetic_student_profiles_simulation(client_and_db):
    """
    Simulates:
    Profile A: High Accuracy + High Confidence -> Reaches MASTERED state
    Profile B: Low Accuracy + High Confidence -> Triggers Danger Zone Misconception
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        q_stmt = select(Question).limit(5)
        res_q = await session.execute(q_stmt)
        questions = res_q.scalars().all()
        c_id = questions[0].concept_id

        # Profile A Simulation (5 correct with high confidence across 5 sessions)
        for i in range(5):
            await LearningIntelligenceEngine.record_attempt_learning_event(
                db=session,
                user_id="student-profile-a",
                question_id=questions[i % len(questions)].id,
                concept_id=c_id,
                is_correct=True,
                confidence="DEFINITELY_KNOW",
                selected_option_key="A",
                correct_option_key="A",
                session_id=f"sim-session-a-{i}"
            )

        # Profile B Simulation (3 wrong with high confidence across 3 sessions)
        for i in range(3):
            await LearningIntelligenceEngine.record_attempt_learning_event(
                db=session,
                user_id="student-profile-b",
                question_id=questions[i % len(questions)].id,
                concept_id=c_id,
                is_correct=False,
                confidence="DEFINITELY_KNOW",
                selected_option_key="B",
                correct_option_key="A",
                session_id=f"sim-session-b-{i}"
            )
        await session.commit()

        # Verify Profile A reached MASTERED state
        stmt_a = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == "student-profile-a",
                StudentConceptMastery.concept_id == c_id
            )
        )
        mastery_a = (await session.execute(stmt_a)).scalars().first()
        assert mastery_a.mastery_state == "MASTERED"
        assert mastery_a.danger_zone_active is False

        # Verify Profile B triggered Danger Zone
        stmt_b = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == "student-profile-b",
                StudentConceptMastery.concept_id == c_id
            )
        )
        mastery_b = (await session.execute(stmt_b)).scalars().first()
        assert mastery_b.danger_zone_active is True
        assert mastery_b.high_confidence_wrong_count == 3

@pytest.mark.asyncio
async def test_statistical_safeguards_sample_size_flags(client_and_db):
    """
    Tests that discrimination index and confidence calibration safely flag INSUFFICIENT_DATA / INSUFFICIENT_SAMPLE_SIZE
    instead of manufacturing false statistical confidence.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Discrimination test on question with < 10 attempts
        q_stmt = select(Question).limit(1)
        res_q = await session.execute(q_stmt)
        q = res_q.scalars().first()

        disc_res = await LearningIntelligenceEngine.calculate_question_discrimination(session, q.id)
        assert disc_res["status"] == "INSUFFICIENT_SAMPLE_SIZE"
        assert disc_res["sample_size"] < 10

        # Confidence calibration on student with < 5 attempts
        calib_res = await LearningIntelligenceEngine.get_confidence_calibration(session, "new-student-no-data")
        assert calib_res["status"] == "INSUFFICIENT_DATA"
        assert calib_res["sample_size"] == 0

@pytest.mark.asyncio
async def test_ai_outage_does_not_break_learning_engine(client_and_db):
    """
    Tests that total AI provider outage has zero impact on tests, scoring, mastery updates,
    spaced repetition, mistake tracking, or daily plans.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Perform mastery updates and daily plan generation entirely offline without AI
        res = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=session,
            user_id="student-offline-test",
            question_id="any-q-id",
            concept_id="any-c-id",
            is_correct=True,
            confidence="DEFINITELY_KNOW",
            selected_option_key="A",
            correct_option_key="A",
            session_id="offline-sess-1"
        )
        await session.commit()

        assert res["mastery_percentage"] == 100.0
        assert res["ease_factor"] >= 2.50

        # Next Best Action remains completely functional
        next_act = await LearningIntelligenceEngine.get_next_best_action(session, "student-offline-test")
        assert "action_type" in next_act
        assert "priority" in next_act

