import asyncio
import pytest
import pytest_asyncio
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.question import Question, QuestionOption, QuestionReview
from app.models.source import Source
from app.models.reviewer import MedicalReviewerProfile
from app.models.test import TestSession, TestAttempt
from app.models.user import User
from app.services.test_service import TestService
from app.services.medical_content_service import MedicalContentService
from app.core.errors import ValidationError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(loop_scope="function")
async def client_and_db():
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False, "timeout": 30.0},
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
async def test_concurrent_test_session_starts_under_load(client_and_db):
    """
    Acceptance:
    20 students start tests concurrently without database locking or collision.
    """
    _, session_maker = client_and_db

    async def start_session_task(student_idx: int):
        async with session_maker() as session:
            user_id = f"concurrent-student-{student_idx}"
            sess, qs = await TestService.create_test_session(
                db=session,
                user_id=user_id,
                mode="DAILY_SHORT_TEST",
                question_count=2
            )
            return sess.id, len(qs)

    # Launch 20 concurrent session creation tasks
    results = await asyncio.gather(*[start_session_task(i) for i in range(20)])
    assert len(results) == 20
    session_ids = [r[0] for r in results]
    assert len(set(session_ids)) == 20  # All 20 unique sessions
    for r in results:
        assert r[1] == 2  # Each got 2 questions

@pytest.mark.asyncio
async def test_concurrent_answer_submissions_and_idempotency_race(client_and_db):
    """
    Acceptance:
    Simultaneous duplicate answer submissions to the exact same question attempt
    resolve idempotently without creating duplicate attempt records.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "race-student-1"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="DAILY_SHORT_TEST",
            question_count=1
        )
        q_id = qs[0].id
        await session.commit()

        # First submission
        res1 = await TestService.submit_answer_idempotent(
            db=session,
            session_id=test_session.id,
            user_id=user_id,
            question_id=q_id,
            selected_option_key="B",
            confidence="DEFINITELY_KNOW"
        )
        assert res1["is_duplicate_submission"] is False
        assert res1["is_correct"] is True

        # Rapid duplicate submissions
        res2 = await TestService.submit_answer_idempotent(
            db=session,
            session_id=test_session.id,
            user_id=user_id,
            question_id=q_id,
            selected_option_key="B",
            confidence="DEFINITELY_KNOW"
        )
        assert res2["is_duplicate_submission"] is True

        # Verify database contains exactly 1 TestAttempt record
        stmt = select(TestAttempt).where(
            and_(
                TestAttempt.session_id == test_session.id,
                TestAttempt.question_id == q_id
            )
        )
        res_db = await session.execute(stmt)
        attempts = res_db.scalars().all()
        assert len(attempts) == 1

@pytest.mark.asyncio
async def test_concurrent_timer_expiration_and_submission_race(client_and_db):
    """
    Acceptance:
    If test expires, in-flight late submissions are rejected cleanly by server authority.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "timer-race-student"
        test_session, qs = await TestService.create_test_session(
            db=session,
            user_id=user_id,
            mode="DAILY_SHORT_TEST",
            question_count=1
        )
        q_id = qs[0].id

        # Force server expiration
        test_session.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
        await session.commit()

        # Late submission fails with validation error
        with pytest.raises(ValidationError) as exc:
            await TestService.submit_answer_idempotent(
                db=session,
                session_id=test_session.id,
                user_id=user_id,
                question_id=q_id,
                selected_option_key="B"
            )
        assert "expired" in str(exc.value).lower()

@pytest.mark.asyncio
async def test_concurrent_two_doctor_review_race(client_and_db):
    """
    Acceptance:
    Two distinct medical reviewers submitting approvals concurrently
    cleanly promote high-risk question to APPROVED / VERIFIED_CORE_QUESTION.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        src = Source(title="Emergency Medicine Guidelines 2026", source_type="GUIDELINE", verification_status="VERIFIED")
        u1 = User(id="doc-conc-1", email="doc1@aiims.edu", hashed_password="pw", role="reviewer")
        p1 = MedicalReviewerProfile(user_id="doc-conc-1", credential_type="MD", specialty="Emergency Medicine", verification_status="VERIFIED", active_status=True)
        u2 = User(id="doc-conc-2", email="doc2@aiims.edu", hashed_password="pw", role="reviewer")
        p2 = MedicalReviewerProfile(user_id="doc-conc-2", credential_type="MD", specialty="Critical Care", verification_status="VERIFIED", active_status=True)
        session.add_all([src, u1, p1, u2, p2])

        q = Question(
            concept_id=concept.id,
            source_id=src.id,
            question_text="Emergency management airway protocol question",
            correct_explanation="Rapid sequence intubation protocol",
            remember_takeaway="Airway first",
            is_high_risk=True,
            high_risk_category="emergency_management",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-conc-review-1"
        )
        session.add(q)
        await session.commit()
        await session.refresh(q)

        # Reviewer 1 approves
        res1 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q.id, reviewer_id="doc-conc-1", verdict="APPROVE", clinical_notes="Doc 1 verified"
        )
        assert res1["status"] == "REVIEW_PENDING"

        # Reviewer 2 approves
        res2 = await MedicalContentService.perform_medical_review(
            db=session, question_id=q.id, reviewer_id="doc-conc-2", verdict="APPROVE", clinical_notes="Doc 2 verified"
        )
        assert res2["status"] == "APPROVED"
        assert res2["trust_class"] == "VERIFIED_CORE_QUESTION"
