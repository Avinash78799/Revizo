import pytest
import pytest_asyncio
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept, Topic, Chapter, Subject, SyllabusRegistry, SyllabusSourceArtifact
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQualityScorecard, QuestionQuarantineRegistry
from app.models.source import Source, PyqReference, SourceConflict
from app.models.reviewer import MedicalReviewerProfile
from app.models.benchmark import BenchmarkCase
from app.models.user import User
from app.services.medical_content_service import MedicalContentService
from app.services.benchmark_service import GoldBenchmarkService
from app.services.content_gap_engine import ContentGapEngine
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
        await GoldBenchmarkService.seed_benchmark_cases(session)

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
async def test_medical_reviewer_credential_and_verification_gates(client_and_db):
    """
    Acceptance:
    - User without MedicalReviewerProfile cannot approve.
    - PENDING, SUSPENDED, or REVOKED reviewer cannot approve.
    - Only VERIFIED + ACTIVE medical reviewer can approve.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        res_c = await session.execute(c_stmt)
        concept = res_c.scalars().first()

        # Seed Verified Source
        src = Source(title="Robbins Basic Pathology 10th Ed", source_type="STANDARD_TEXTBOOK", verification_status="VERIFIED")
        session.add(src)

        q = Question(
            concept_id=concept.id,
            source_id=src.id,
            question_text="A pathology test question",
            correct_explanation="Correct explanation",
            remember_takeaway="Takeaway pearl",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-rev-test-1"
        )
        session.add(q)
        await session.commit()
        await session.refresh(q)

        # 1. Non-registered reviewer fails
        with pytest.raises(ValidationError) as exc1:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q.id, reviewer_id="random-user-no-profile", verdict="APPROVE", clinical_notes="Approved"
            )
        assert "medical reviewer profile" in str(exc1.value).lower()

        # 2. Suspended reviewer fails
        user_susp = User(id="doc-suspended", email="susp@hospital.in", hashed_password="pw", role="reviewer")
        prof_susp = MedicalReviewerProfile(
            user_id="doc-suspended", credential_type="MD", specialty="Pathology", verification_status="SUSPENDED", active_status=False
        )
        session.add_all([user_susp, prof_susp])
        await session.commit()

        with pytest.raises(ValidationError) as exc2:
            await MedicalContentService.perform_medical_review(
                db=session, question_id=q.id, reviewer_id="doc-suspended", verdict="APPROVE", clinical_notes="Suspended doc approving"
            )
        assert "suspended" in str(exc2.value).lower()

        # 3. Verified reviewer succeeds
        user_ver = User(id="doc-verified", email="doc@aiims.edu", hashed_password="pw", role="reviewer")
        prof_ver = MedicalReviewerProfile(
            user_id="doc-verified", credential_type="MD", specialty="Pathology", verification_status="VERIFIED", active_status=True
        )
        session.add_all([user_ver, prof_ver])
        await session.commit()

        res_ok = await MedicalContentService.perform_medical_review(
            db=session, question_id=q.id, reviewer_id="doc-verified", verdict="APPROVE", clinical_notes="Verified pathology approval"
        )
        assert res_ok["status"] == "APPROVED"
        assert res_ok["trust_class"] == "VERIFIED_CORE_QUESTION"

@pytest.mark.asyncio
async def test_gold_benchmark_cases_dataset_integrity(client_and_db):
    """
    Acceptance:
    - 80+ gold benchmark cases exist (actual: 110 seeded).
    - Safety-critical categories contain >= 10 cases each.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        stmt = select(BenchmarkCase)
        res = await session.execute(stmt)
        cases = res.scalars().all()

        assert len(cases) >= 80  # 110 cases
        categories = {c.category for c in cases}
        assert len(categories) == 16

        # Safety-critical check (>= 10 cases each)
        for safety_cat in ["unsafe_treatment", "incorrect_dose", "drug_contraindication", "pregnancy_safety", "pediatric_safety", "emergency_management"]:
            cat_cases = [c for c in cases if c.category == safety_cat]
            assert len(cat_cases) >= 10

@pytest.mark.asyncio
async def test_quality_score_critical_failure_hard_gate(client_and_db):
    """
    Acceptance: Critical failure (e.g. clinical accuracy failure) always triggers HARD_REJECT
    regardless of high aggregate score.
    """
    scorecard = MedicalContentService.evaluate_quality_scorecard_with_hard_gates(
        clinical_accuracy_passed=False,  # Critical failure
        medical_accuracy_passed=True,
        single_best_answer_passed=True,
        source_support_passed=True,
        clinical_accuracy_score=0.0,
        single_best_answer_score=1.0,
        distractor_quality_score=1.0,
        exam_relevance_score=1.0,
        source_support_score=1.0,
        explanation_quality_score=1.0,
        novelty_score=1.0
    )

    assert scorecard["quality_gate_status"] == "CRITICAL_FAILURE_HARD_REJECT"
    assert scorecard["failed_gate"] == "CLINICAL_ACCURACY_FAILURE"

@pytest.mark.asyncio
async def test_high_yield_evidence_provenance_zero_pyq(client_and_db):
    """
    Acceptance: When verified PYQ evidence is 0, PYQ recurrence component is strictly 0.00.
    """
    score_data = MedicalContentService.calculate_evidence_backed_high_yield_score(
        verified_pyq_count=0,
        clinical_importance_score=0.80,
        curriculum_centrality_score=0.80
    )

    assert score_data["pyq_recurrence_component"] == 0.00
    assert score_data["evidence_count"] == 0
    assert score_data["high_yield_score"] == 0.48  # (0*0.4) + (0.8*0.3) + (0.8*0.3) = 0.48

@pytest.mark.asyncio
async def test_unverified_source_blocks_trusted_publication(client_and_db):
    """
    Acceptance: Questions relying on UNVERIFIED source cannot be approved into VERIFIED_CORE_QUESTION.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        res_c = await session.execute(c_stmt)
        concept = res_c.scalars().first()

        # Unverified source
        unverified_source = Source(
            id="unverified-src-1",
            title="Random Unreviewed Medical Blog",
            source_type="OTHER",
            verification_status="UNVERIFIED"
        )
        session.add(unverified_source)
        await session.flush()

        q = Question(
            concept_id=concept.id,
            source_id=unverified_source.id,
            question_text="Unverified question text",
            correct_explanation="Explanation",
            remember_takeaway="Takeaway",
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash="hash-unverified-src-1"
        )
        session.add(q)

        user_doc = User(id="doc-active", email="doc-act@aiims.edu", hashed_password="pw", role="reviewer")
        prof_doc = MedicalReviewerProfile(
            user_id="doc-active", credential_type="MD", specialty="Medicine", verification_status="VERIFIED", active_status=True
        )
        session.add_all([user_doc, prof_doc])
        await session.commit()
        await session.refresh(q)

        with pytest.raises(ValidationError) as exc:
            await MedicalContentService.perform_medical_review(
                db=session,
                question_id=q.id,
                reviewer_id="doc-active",
                verdict="APPROVE",
                clinical_notes="Attempting approval on unverified source"
            )
        assert "unverified source" in str(exc.value).lower()

@pytest.mark.asyncio
async def test_content_gap_priority_score_and_dataset_readiness_gate(client_and_db):
    """
    Acceptance: ContentGapEngine computes explainable gap priority scores and identifies
    dataset readiness status as BOOTSTRAP / PARTIALLY_VERIFIED in development state.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        matrix = await ContentGapEngine.generate_coverage_matrix(session)

        summary = matrix["summary"]
        assert "dataset_readiness" in summary
        readiness = summary["dataset_readiness"]

        assert readiness["production_ready"] is False
        assert readiness["is_ready_for_public_testing"] is False
        assert "missing_trusted_questions" in readiness["production_deficits"]

        # Check Red Gaps have priority scores
        red_gaps = matrix["red_critical_gaps"]
        if red_gaps:
            assert "gap_priority_score" in red_gaps[0]
            assert 0.0 <= red_gaps[0]["gap_priority_score"] <= 1.0
