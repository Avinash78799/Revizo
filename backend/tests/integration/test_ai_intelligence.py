import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept
from app.models.question import Question, AICallLog
from app.models.generation import AIEvaluationRun
from app.services.concept_priority_engine import ConceptPriorityEngine
from app.services.ai_question_service import AIQuestionService, QuestionGenerationRequest
from app.services.ai_evaluation_service import AIEvaluationService

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
async def test_concept_priority_calculation(client_and_db):
    """
    Evaluates multi-component high-yield priority score for a concept.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(Concept).limit(1)
        res = await session.execute(stmt)
        c = res.scalars().first()

        priority_res = await ConceptPriorityEngine.calculate_concept_priority(session, c.id)

        assert "overall_priority_score" in priority_res
        assert 0.0 <= priority_res["overall_priority_score"] <= 1.0
        assert "breakdown" in priority_res
        assert "why_priority" in priority_res
        assert len(priority_res["why_priority"]) >= 1

@pytest.mark.asyncio
async def test_ai_question_generation_concept_driven_and_no_auto_publish(client_and_db):
    """
    Generates a question from a concept with verified evidence.
    Asserts NO-AUTO-PUBLISH invariant: resulting status CANNOT be 'PUBLISHED' or 'VERIFIED_CORE_QUESTION'.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(Concept).limit(1)
        res = await session.execute(stmt)
        c = res.scalars().first()

        req = QuestionGenerationRequest(
            concept_id=c.id,
            question_type="CLINICAL_VIGNETTE",
            difficulty_target="MODERATE",
            exam_relevance_tag="HIGH_YIELD"
        )

        gen_res = await AIQuestionService.generate_concept_question_pipeline(
            db=session,
            req=req,
            actor_id="reviewer-dr-1",
            provider_name="mock"
        )

        assert gen_res["success"] is True
        q_id = gen_res["question_id"]

        # Verify in Database
        stmt_q = select(Question).options(selectinload(Question.options)).where(Question.id == q_id)
        res_q = await session.execute(stmt_q)
        q = res_q.scalars().first()

        # Absolute Rule Verification: AI-generated questions enter review, NEVER published directly
        assert q.status in ("AI_VALIDATED", "PROPOSED", "REVIEW_REQUIRED")
        assert q.trust_class in ("AI_PROPOSED", "REVIEW_PENDING")
        assert q.trust_class != "VERIFIED_CORE_QUESTION"
        assert q.status != "PUBLISHED"

        # Verify Structured Options & Corrective Explanations
        assert len(q.options) == 4
        assert any(o.is_correct for o in q.options)
        assert q.correct_explanation is not None
        assert q.remember_takeaway is not None

@pytest.mark.asyncio
async def test_insufficient_evidence_generation_refusal(client_and_db):
    """
    If a concept lacks approved notes/pearls, the pipeline refuses generation with INSUFFICIENT_EVIDENCE.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create an empty concept with no clinical notes or pearls
        empty_concept = Concept(
            topic_id="topic-1",
            name="Unresearched Concept",
            high_yield_notes=None,
            clinical_pearl=None
        )
        session.add(empty_concept)
        await session.commit()

        req = QuestionGenerationRequest(
            concept_id=empty_concept.id,
            question_type="SINGLE_BEST_ANSWER"
        )

        gen_res = await AIQuestionService.generate_concept_question_pipeline(
            db=session,
            req=req,
            actor_id="reviewer-dr-1"
        )

        assert gen_res["success"] is False
        assert gen_res["status"] == "INSUFFICIENT_EVIDENCE"

@pytest.mark.asyncio
async def test_duplicate_question_generation_rejection(client_and_db):
    """
    If generated text has high similarity to an existing question in the concept, it is rejected.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(Concept).limit(1)
        res = await session.execute(stmt)
        c = res.scalars().first()

        req = QuestionGenerationRequest(
            concept_id=c.id,
            question_type="CLINICAL_VIGNETTE"
        )

        # First generation
        res1 = await AIQuestionService.generate_concept_question_pipeline(db=session, req=req)
        assert res1["success"] is True

        # Second generation of identical concept proposal -> triggers duplicate rejection
        res2 = await AIQuestionService.generate_concept_question_pipeline(db=session, req=req)
        assert res2["success"] is False
        assert res2["status"] == "DUPLICATE_REJECTED"

@pytest.mark.asyncio
async def test_ai_evaluation_benchmark_framework(client_and_db):
    """
    Executes benchmark evaluation run against gold standard dataset.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        eval_run = await AIEvaluationService.run_benchmark_evaluation(
            db=session,
            prompt_version="neetpg-validator-v1.0",
            model_name="medical-validator-v1",
            provider_name="mock"
        )

        assert "run_id" in eval_run
        assert eval_run["total_items"] >= 3
        assert 0.0 <= eval_run["accuracy_score"] <= 1.0

        # Verify persisted in database
        stmt_r = select(AIEvaluationRun).where(AIEvaluationRun.id == eval_run["run_id"])
        res_r = await session.execute(stmt_r)
        run_record = res_r.scalars().first()
        assert run_record is not None
        assert run_record.prompt_version == "neetpg-validator-v1.0"

@pytest.mark.asyncio
async def test_ai_observability_and_api_endpoints(client_and_db):
    """
    Tests the admin AI intelligence REST endpoints: concept priority, evaluation, and observability.
    """
    client, session_maker = client_and_db

    admin_login = await client.post("/api/v1/auth/login", json={
        "email": "admin@neetpg.pro",
        "password": "AdminSecure123!"
    })
    headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    # Fetch a concept
    async with session_maker() as session:
        stmt = select(Concept).limit(1)
        res = await session.execute(stmt)
        c = res.scalars().first()
        c_id = c.id

    # 1. Concept Priority API
    cp_res = await client.get(f"/api/v1/admin/ai/concept-priority/{c_id}", headers=headers)
    assert cp_res.status_code == 200
    assert "overall_priority_score" in cp_res.json()

    # 2. Run Benchmark Evaluation API
    eval_res = await client.post("/api/v1/admin/ai/run-evaluation", json={
        "prompt_version": "v1.0-test",
        "model_name": "test-validator"
    }, headers=headers)
    assert eval_res.status_code == 200
    assert "accuracy_score" in eval_res.json()

    # 3. AI Observability API
    obs_res = await client.get("/api/v1/admin/ai/observability", headers=headers)
    assert obs_res.status_code == 200
    obs = obs_res.json()
    assert "total_ai_calls" in obs
    assert "total_tokens_consumed" in obs
    assert "total_estimated_cost_usd" in obs
