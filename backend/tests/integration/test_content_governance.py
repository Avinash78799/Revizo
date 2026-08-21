import pytest
import pytest_asyncio
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.question import Question, QuestionOption, QuestionVersion, QuestionReview, AICallLog
from app.services.question_lifecycle_service import QuestionLifecycleService
from app.services.content_validation_engine import ContentValidationEngine
from app.services.ai_provider import AIProviderRegistry, MockAIProvider
from app.services.multi_pass_validator import MultiPassValidatorService
from app.services.governance_service import GovernanceService
from app.core.errors import InvalidStateTransitionError, AuthorizationError

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
async def test_invalid_lifecycle_state_transitions(client_and_db):
    """
    State transitions must follow strict legal paths. Illegal transitions are rejected.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        # Create a proposed question
        q = Question(
            concept_id="some-concept-id",
            question_text="Sample proposed question",
            correct_explanation="Explanation",
            remember_takeaway="Takeaway",
            text_hash="hash-123",
            status="PROPOSED"
        )
        session.add(q)
        await session.commit()
        q_id = q.id

        # Illegal: PROPOSED directly to PUBLISHED without review
        with pytest.raises(InvalidStateTransitionError):
            await QuestionLifecycleService.transition_state(
                db=session,
                question_id=q_id,
                target_status="PUBLISHED",
                actor_id="test-actor",
                is_human_reviewer=False
            )

        # Illegal: PROPOSED directly to MONITORED
        with pytest.raises(InvalidStateTransitionError):
            await QuestionLifecycleService.transition_state(
                db=session,
                question_id=q_id,
                target_status="MONITORED",
                actor_id="test-actor"
            )

@pytest.mark.asyncio
async def test_single_best_answer_validation_rules():
    """
    Validates single-best-answer rules:
    - Exactly 1 correct option
    - Rejects 2 correct options
    - Rejects 0 correct options
    - Rejects duplicate option texts
    """
    # Case 1: Multiple correct options
    options_two_correct = [
        {"option_key": "A", "option_text": "Atropine", "is_correct": True},
        {"option_key": "B", "option_text": "Glycopyrrolate", "is_correct": True},
        {"option_key": "C", "option_text": "Physostigmine", "is_correct": False},
        {"option_key": "D", "option_text": "Pralidoxime", "is_correct": False},
    ]
    valid_2, errors_2 = ContentValidationEngine.validate_single_best_answer(options_two_correct)
    assert valid_2 is False
    assert any("2 options were marked correct" in err for err in errors_2)

    # Case 2: No correct option
    options_zero_correct = [
        {"option_key": "A", "option_text": "Atropine", "is_correct": False},
        {"option_key": "B", "option_text": "Glycopyrrolate", "is_correct": False},
        {"option_key": "C", "option_text": "Physostigmine", "is_correct": False},
        {"option_key": "D", "option_text": "Pralidoxime", "is_correct": False},
    ]
    valid_0, errors_0 = ContentValidationEngine.validate_single_best_answer(options_zero_correct)
    assert valid_0 is False
    assert any("none was marked correct" in err for err in errors_0)

    # Case 3: Duplicate option text
    options_duplicate = [
        {"option_key": "A", "option_text": "Atropine", "is_correct": True},
        {"option_key": "B", "option_text": "Atropine", "is_correct": False},
        {"option_key": "C", "option_text": "Physostigmine", "is_correct": False},
        {"option_key": "D", "option_text": "Pralidoxime", "is_correct": False},
    ]
    valid_dup, errors_dup = ContentValidationEngine.validate_single_best_answer(options_duplicate)
    assert valid_dup is False
    assert any("Duplicate option texts" in err for err in errors_dup)

@pytest.mark.asyncio
async def test_clinical_vignette_contradiction_detection():
    """
    Detects internal factual contradictions in clinical vignette stems.
    """
    # Contradiction: Stated hypotensive but BP is 150/90
    contradictory_stem = "A 45-year-old male is severely hypotensive in septic shock with BP 150/90 mmHg."
    valid, errors = ContentValidationEngine.validate_clinical_vignette(contradictory_stem)
    assert valid is False
    assert any("hypotensive" in err.lower() for err in errors)

    # Coherent vignette: BP 70/40 is genuinely hypotensive
    coherent_stem = "A 45-year-old male is severely hypotensive with BP 70/40 mmHg and pulse 125 bpm."
    valid_ok, errors_ok = ContentValidationEngine.validate_clinical_vignette(coherent_stem)
    assert valid_ok is True
    assert len(errors_ok) == 0

@pytest.mark.asyncio
async def test_ai_malformed_output_safety(client_and_db):
    """
    If an AI provider returns unparseable non-JSON text, the pipeline safely catches the error,
    logs the failure to AICallLog, and keeps the question untrusted in REVIEW_REQUIRED (never auto-publishes).
    """
    _, session_maker = client_and_db

    # Register malformed mock provider
    AIProviderRegistry.register_provider("malformed_mock", MockAIProvider(simulate_malformed=True))

    async with session_maker() as session:
        stmt = select(Question).where(Question.status.in_(["published", "draft", "ai_generated"]))
        res = await session.execute(stmt)
        q = res.scalars().first()

        result = await MultiPassValidatorService.run_multi_pass_validation(
            db=session,
            question_id=q.id,
            primary_provider_name="malformed_mock",
            secondary_provider_name="malformed_mock"
        )
        await session.commit()

        assert result["all_passed"] is False
        assert result["status"] == "REVIEW_REQUIRED"
        assert result["trust_class"] == "REVIEW_PENDING"

        # Verify AICallLog recorded the failure
        stmt_log = select(AICallLog).where(AICallLog.question_id == q.id)
        res_log = await session.execute(stmt_log)
        logs = res_log.scalars().all()
        assert len(logs) >= 1
        assert logs[0].success is False
        assert "JSONDecodeError" in logs[0].error_message

    # Reset registry to default mock provider
    AIProviderRegistry.register_provider("mock", MockAIProvider())

@pytest.mark.asyncio
async def test_ai_validator_disagreement_routes_to_review(client_and_db):
    """
    If Validator A passes and Validator B rejects, the pipeline flags validator disagreement
    and routes the question to REVIEW_REQUIRED rather than blindly averaging scores.
    """
    _, session_maker = client_and_db

    AIProviderRegistry.register_provider("pass_mock", MockAIProvider(force_verdict="PASS"))
    AIProviderRegistry.register_provider("reject_mock", MockAIProvider(force_verdict="REJECT"))

    async with session_maker() as session:
        stmt = select(Question).where(Question.status.in_(["published", "draft", "ai_generated"]))
        res = await session.execute(stmt)
        q = res.scalars().first()

        result = await MultiPassValidatorService.run_multi_pass_validation(
            db=session,
            question_id=q.id,
            primary_provider_name="pass_mock",
            secondary_provider_name="reject_mock"
        )
        await session.commit()

        assert result["validator_disagreement"] is True
        assert result["all_passed"] is False
        assert result["status"] == "REVIEW_REQUIRED"

    AIProviderRegistry.register_provider("mock", MockAIProvider())

@pytest.mark.asyncio
async def test_ai_cannot_unilaterally_publish_or_bypass_human_review(client_and_db):
    """
    AI or automated systems CANNOT approve or publish questions.
    Only authenticated human reviewers can approve.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(Question).where(Question.status.in_(["published", "draft", "ai_generated"]))
        res = await session.execute(stmt)
        q = res.scalars().first()
        q.status = "MEDICAL_REVIEW"
        await session.commit()

        # Non-human attempt to approve raises AuthorizationError
        with pytest.raises(AuthorizationError):
            await QuestionLifecycleService.transition_state(
                db=session,
                question_id=q.id,
                target_status="APPROVED",
                actor_id="automated-ai-agent",
                is_human_reviewer=False
            )

@pytest.mark.asyncio
async def test_question_versioning_and_historical_immutability(client_and_db):
    """
    Editing or approving a published question creates a new immutable QuestionVersion snapshot.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(Question).options(selectinload(Question.options)).where(Question.status == "published")
        res = await session.execute(stmt)
        q = res.scalars().first()

        initial_version = q.content_version

        # Execute Doctor Approval Decision
        updated_q = await GovernanceService.execute_medical_review_decision(
            db=session,
            reviewer_id="dr-reviewer-id",
            question_id=q.id,
            verdict="APPROVE",
            clinical_notes="Verified against Katzung Pharmacology 15th Ed."
        )
        await session.commit()

        assert updated_q.status == "PUBLISHED"
        assert updated_q.trust_class == "VERIFIED_CORE_QUESTION"
        assert updated_q.content_version > initial_version

        # Verify QuestionVersion snapshot was stored in database
        stmt_v = select(QuestionVersion).where(QuestionVersion.question_id == q.id)
        res_v = await session.execute(stmt_v)
        versions = res_v.scalars().all()
        assert len(versions) >= 1
        assert versions[0].correct_explanation == q.correct_explanation

@pytest.mark.asyncio
async def test_content_coverage_matrix_and_governance_api(client_and_db):
    """
    Tests the governance dashboard and coverage analytics APIs.
    """
    client, _ = client_and_db

    admin_login = await client.post("/api/v1/auth/login", json={
        "email": "admin@neetpg.pro",
        "password": "AdminSecure123!"
    })
    headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    # 1. Governance Dashboard
    dash_res = await client.get("/api/v1/admin/governance/dashboard", headers=headers)
    assert dash_res.status_code == 200
    dash = dash_res.json()
    assert "total_questions" in dash
    assert "verified_questions" in dash
    assert "review_pending" in dash

    # 2. Coverage Analytics
    cov_res = await client.get("/api/v1/admin/governance/coverage", headers=headers)
    assert cov_res.status_code == 200
    coverage = cov_res.json()
    assert len(coverage) >= 1
    assert "subject_name" in coverage[0]
    assert "topics" in coverage[0]

    # 3. Source Registry
    src_res = await client.post("/api/v1/admin/governance/sources", json={
        "title": "Harrison's Principles of Internal Medicine",
        "source_type": "STANDARD_TEXTBOOK",
        "edition": "21st Edition",
        "publication_year": 2022,
        "publisher": "McGraw Hill"
    }, headers=headers)
    assert src_res.status_code == 201
    assert src_res.json()["title"] == "Harrison's Principles of Internal Medicine"
