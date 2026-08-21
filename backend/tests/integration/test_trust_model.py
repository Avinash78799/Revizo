import pytest
from sqlalchemy import select, and_
from app.db.seed import seed_database
from app.models import Question, User

@pytest.mark.asyncio
async def test_trust_model_isolates_development_seeds_from_verified_pool(db_session):
    # Seed database with development items
    await seed_database(db_session)

    # 1. Query verified production questions (what a production test engine queries)
    stmt_production = select(Question).where(
        and_(
            Question.trust_class == "verified_core_question",
            Question.status == "published"
        )
    )
    res_production = await db_session.execute(stmt_production)
    prod_questions = res_production.scalars().all()

    # Must be 0 because all seed items are strictly tagged as 'development_seed'
    assert len(prod_questions) == 0

    # 2. Query development seed questions
    stmt_dev = select(Question).where(Question.trust_class == "development_seed")
    res_dev = await db_session.execute(stmt_dev)
    dev_questions = res_dev.scalars().all()

    assert len(dev_questions) >= 3
    for q in dev_questions:
        assert q.trust_class == "development_seed"
        assert "[DEVELOPMENT SEED" in q.question_text
        assert len(q.options) == 4
        correct_opts = [opt for opt in q.options if opt.is_correct]
        assert len(correct_opts) == 1
        assert q.quality_scorecard is not None
