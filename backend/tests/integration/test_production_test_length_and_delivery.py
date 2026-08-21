import pytest
import pytest_asyncio
import hashlib
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import Base, get_db
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.models.question import Question, QuestionOption
from app.models.user import User
from app.models.test import TestSession, TestQuestion
from app.services.test_service import TestService
from app.services.question_selection_engine import QuestionSelectionEngine
from app.core.errors import ValidationError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

def get_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

@pytest_asyncio.fixture(loop_scope="function")
async def test_env():
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # 1. Create Subject, Chapter, Topic, Concepts
        subj = Subject(name="General Pharmacology", code="PHARM", order_index=1)
        session.add(subj)
        await session.flush()

        chap = Chapter(subject_id=subj.id, name="Autonomic Pharmacology", order_index=1)
        session.add(chap)
        await session.flush()

        top = Topic(chapter_id=chap.id, name="Cholinergic Pharmacology", order_index=1)
        session.add(top)
        await session.flush()

        # Create 35 Verified Questions in this topic/subject
        for i in range(1, 36):
            concept = Concept(topic_id=top.id, name=f"Concept #{i}", exam_relevance_score=0.90)
            session.add(concept)
            await session.flush()

            q_text = f"Verified medical question {i} regarding autonomic receptors."
            q = Question(
                concept_id=concept.id,
                trust_class="SOURCE_REFERENCED",
                question_type="clinical_vignette",
                difficulty="moderate",
                status="published",
                is_high_yield=True,
                question_text=q_text,
                correct_explanation=f"Explanation for question {i}.",
                remember_takeaway=f"High yield takeaway pearl {i}.",
                text_hash=get_hash(q_text)
            )
            session.add(q)
            await session.flush()

            session.add_all([
                QuestionOption(question_id=q.id, option_key="A", option_text="Option A", is_correct=(i % 4 == 1)),
                QuestionOption(question_id=q.id, option_key="B", option_text="Option B", is_correct=(i % 4 == 2)),
                QuestionOption(question_id=q.id, option_key="C", option_text="Option C", is_correct=(i % 4 == 3)),
                QuestionOption(question_id=q.id, option_key="D", option_text="Option D", is_correct=(i % 4 == 0)),
            ])

        # Create a single blocked/withdrawn question and a dev benchmark question
        concept_blocked = Concept(topic_id=top.id, name="Blocked Concept", exam_relevance_score=0.5)
        session.add(concept_blocked)
        await session.flush()

        q_blocked_text = "This is a rejected withdrawn question."
        q_blocked = Question(
            concept_id=concept_blocked.id,
            trust_class="WITHDRAWN",
            question_type="single_best_answer",
            difficulty="hard",
            status="REJECTED",
            is_high_yield=False,
            question_text=q_blocked_text,
            correct_explanation="Blocked explanation.",
            remember_takeaway="Blocked takeaway.",
            text_hash=get_hash(q_blocked_text)
        )
        session.add(q_blocked)

        q_quar_text = "This is a quarantined question."
        q_quarantine = Question(
            concept_id=concept_blocked.id,
            trust_class="QUARANTINED",
            question_type="single_best_answer",
            difficulty="hard",
            status="QUARANTINED",
            is_high_yield=False,
            question_text=q_quar_text,
            correct_explanation="Quarantined explanation.",
            remember_takeaway="Quarantined takeaway.",
            text_hash=get_hash(q_quar_text)
        )
        session.add(q_quarantine)

        q_dev_text = "This is a development benchmark question."
        q_dev = Question(
            concept_id=concept_blocked.id,
            trust_class="DEVELOPMENT_BENCHMARK",
            question_type="single_best_answer",
            difficulty="hard",
            status="WITHDRAWN",
            is_high_yield=False,
            question_text=q_dev_text,
            correct_explanation="Dev explanation.",
            remember_takeaway="Dev takeaway.",
            text_hash=get_hash(q_dev_text)
        )
        session.add(q_dev)

        await session.commit()

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
async def test_1_daily_short_creates_exactly_10_questions(test_env):
    """TEST 1: Daily Short creates exactly 10 questions."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        assert test_session.total_questions == 10
        assert len(qs) == 10


@pytest.mark.asyncio
async def test_2_topic_test_creates_exactly_15_questions(test_env):
    """TEST 2: Topic Test creates exactly 15 questions."""
    _, session_maker = test_env
    async with session_maker() as session:
        top = (await session.execute(select(Topic).limit(1))).scalars().first()
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="TOPIC_TEST", topic_id=top.id, question_count=15
        )
        assert test_session.total_questions == 15
        assert len(qs) == 15


@pytest.mark.asyncio
async def test_3_chapter_revision_creates_exactly_20_questions(test_env):
    """TEST 3: Chapter Revision creates exactly 20 questions."""
    _, session_maker = test_env
    async with session_maker() as session:
        chap = (await session.execute(select(Chapter).limit(1))).scalars().first()
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="CHAPTER_REVISION_TEST", chapter_id=chap.id, question_count=20
        )
        assert test_session.total_questions == 20
        assert len(qs) == 20


@pytest.mark.asyncio
async def test_4_subject_test_creates_exactly_30_questions(test_env):
    """TEST 4: Subject Test creates exactly 30 questions."""
    _, session_maker = test_env
    async with session_maker() as session:
        subj = (await session.execute(select(Subject).limit(1))).scalars().first()
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="SUBJECT_TEST", subject_id=subj.id, question_count=30
        )
        assert test_session.total_questions == 30
        assert len(qs) == 30


@pytest.mark.asyncio
@pytest.mark.parametrize("valid_count", [10, 15, 20, 25, 30])
async def test_5_to_9_custom_test_accepts_valid_counts(test_env, valid_count):
    """TEST 5-9: Custom test accepts 10, 15, 20, 25, 30."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="CUSTOM_TEST", question_count=valid_count
        )
        assert test_session.total_questions == valid_count
        assert len(qs) == valid_count


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_count", [0, 1, 2, 5, 8, 9])
async def test_10_custom_test_rejects_below_10(test_env, invalid_count):
    """TEST 10: Custom test rejects counts 1–9."""
    _, session_maker = test_env
    async with session_maker() as session:
        with pytest.raises(ValidationError) as exc:
            await TestService.create_test_session(
                db=session, user_id="student-1", mode="CUSTOM_TEST", question_count=invalid_count
            )
        assert "between 10 and 30" in str(exc.value)


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_count", [31, 50, 100])
async def test_11_custom_test_rejects_above_30(test_env, invalid_count):
    """TEST 11: Custom test rejects counts >30."""
    _, session_maker = test_env
    async with session_maker() as session:
        with pytest.raises(ValidationError) as exc:
            await TestService.create_test_session(
                db=session, user_id="student-1", mode="CUSTOM_TEST", question_count=invalid_count
            )
        assert "between 10 and 30" in str(exc.value)


@pytest.mark.asyncio
async def test_12_no_duplicate_question_ids_in_single_test(test_env):
    """TEST 12: Single test must contain 100% unique question IDs."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="SUBJECT_TEST", question_count=30
        )
        q_ids = [q.id for q in qs]
        assert len(q_ids) == len(set(q_ids)), "Duplicate question IDs detected in test"


@pytest.mark.asyncio
async def test_13_blocked_content_never_enters_generated_tests(test_env):
    """TEST 13: Blocked (WITHDRAWN, REJECTED, QUARANTINED) content never enters student tests."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="SUBJECT_TEST", question_count=30
        )
        for q in qs:
            assert q.status in ("published", "PUBLISHED", "approved", "APPROVED")
            assert q.trust_class not in ("WITHDRAWN", "QUARANTINED", "REVISION_REQUESTED", "UNVERIFIED")


@pytest.mark.asyncio
async def test_14_development_seed_questions_never_enter_tests(test_env):
    """TEST 14: Development seed / benchmark questions never enter student tests."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="SUBJECT_TEST", question_count=30
        )
        for q in qs:
            assert q.trust_class not in ("development_seed", "DEVELOPMENT_SEED", "DEVELOPMENT_BENCHMARK")
            assert "[DEVELOPMENT SEED QUESTION]" not in q.question_text


@pytest.mark.asyncio
async def test_15_pyq_remains_zero_and_locked(test_env):
    """TEST 15: VERIFIED_PYQ remains 0 and unavailable."""
    _, session_maker = test_env
    async with session_maker() as session:
        pyqs = (await session.execute(select(Question).where(Question.trust_class == "VERIFIED_PYQ"))).scalars().all()
        assert len(pyqs) == 0


@pytest.mark.asyncio
async def test_16_answer_keys_absent_during_in_progress(test_env):
    """TEST 16: Answer keys and explanations are absent from student runner formatting."""
    _, session_maker = test_env
    async with session_maker() as session:
        q = (await session.execute(select(Question).options(selectinload(Question.options), selectinload(Question.concept)).limit(1))).scalars().first()
        formatted = QuestionSelectionEngine.format_question_for_student_runner(q)
        assert "correct_option_key" not in formatted
        assert "correct_explanation" not in formatted
        assert "why_wrong_explanation" not in formatted
        for opt in formatted["options"]:
            assert "is_correct" not in opt


@pytest.mark.asyncio
async def test_17_actual_server_created_count_matches_session_total(test_env):
    """TEST 17: Actual server-created question count matches session total."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="TOPIC_TEST", question_count=15
        )
        assert test_session.total_questions == len(qs) == 15


@pytest.mark.asyncio
async def test_18_insufficient_eligible_questions_fails_cleanly(test_env):
    """TEST 18: Insufficient eligible questions produces a clear availability response."""
    _, session_maker = test_env
    async with session_maker() as session:
        with pytest.raises(ValidationError) as exc:
            await TestService.create_test_session(
                db=session,
                user_id="student-1",
                mode="TOPIC_TEST",
                topic_id="non-existent-topic-id",
                question_count=15
            )
        assert "INSUFFICIENT_CONTENT" in str(exc.value)


@pytest.mark.asyncio
async def test_19_reloading_test_session_preserves_question_set(test_env):
    """TEST 19: Refreshing/reloading an existing test does not change its question set."""
    _, session_maker = test_env
    async with session_maker() as session:
        test_session, qs = await TestService.create_test_session(
            db=session, user_id="student-1", mode="DAILY_SHORT_TEST", question_count=10
        )
        initial_ids = [q.id for q in qs]

        # Fetch session's TestQuestion rows again from DB
        tq_stmt = select(TestQuestion).where(TestQuestion.session_id == test_session.id).order_by(TestQuestion.order_index)
        tq_rows = (await session.execute(tq_stmt)).scalars().all()
        reloaded_ids = [tq.question_id for tq in tq_rows]
        assert initial_ids == reloaded_ids
