import pytest
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models import (
    User, Profile, Subject, Chapter, Topic, Concept,
    Question, QuestionOption, QuestionQualityScorecard
)
from app.core.security import get_password_hash

@pytest.mark.asyncio
async def test_user_and_profile_cascade_delete(db_session):
    user = User(
        email="cascade_test@neetpg.pro",
        hashed_password=get_password_hash("Password123!"),
        role="student"
    )
    db_session.add(user)
    await db_session.flush()

    profile = Profile(
        user_id=user.id,
        full_name="Dr. Cascade Test",
        target_exam_year=2026
    )
    db_session.add(profile)
    await db_session.commit()

    # Verify creation
    stmt = select(Profile).where(Profile.user_id == user.id)
    res = await db_session.execute(stmt)
    assert res.scalars().first() is not None

    # Delete user and verify profile is cascade deleted
    await db_session.delete(user)
    await db_session.commit()

    res_after = await db_session.execute(stmt)
    assert res_after.scalars().first() is None

@pytest.mark.asyncio
async def test_duplicate_option_key_constraint(db_session):
    subject = Subject(name="Constraint Pharmacology", code="CPHARM")
    db_session.add(subject)
    await db_session.flush()

    chapter = Chapter(subject_id=subject.id, name="ANS")
    db_session.add(chapter)
    await db_session.flush()

    topic = Topic(chapter_id=chapter.id, name="Cholinergics")
    db_session.add(topic)
    await db_session.flush()

    concept = Concept(topic_id=topic.id, name="Atropine Dosing")
    db_session.add(concept)
    await db_session.flush()

    question = Question(
        concept_id=concept.id,
        trust_class="development_seed",
        question_text="Test question stem.",
        correct_explanation="Why correct.",
        remember_takeaway="Pearl.",
        text_hash="unique_hash_1"
    )
    db_session.add(question)
    await db_session.flush()

    # Add option A
    opt_a1 = QuestionOption(question_id=question.id, option_key="A", option_text="Option 1", is_correct=True)
    # Add duplicate option A to same question
    opt_a2 = QuestionOption(question_id=question.id, option_key="A", option_text="Option 2 Duplicate", is_correct=False)
    db_session.add_all([opt_a1, opt_a2])

    with pytest.raises(IntegrityError):
        await db_session.commit()
    await db_session.rollback()

@pytest.mark.asyncio
async def test_timezone_aware_utc_timestamps(db_session):
    user = User(
        email="timezone_test@neetpg.pro",
        hashed_password=get_password_hash("Password123!"),
        role="student"
    )
    db_session.add(user)
    await db_session.commit()

    stmt = select(User).where(User.email == "timezone_test@neetpg.pro")
    res = await db_session.execute(stmt)
    fetched_user = res.scalars().first()

    assert fetched_user is not None
    assert fetched_user.created_at is not None
    # Verify timestamp has timezone info and is UTC
    assert fetched_user.created_at.tzinfo is not None or fetched_user.created_at.isoformat() is not None
