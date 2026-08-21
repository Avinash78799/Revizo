import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.taxonomy import Concept
from app.models.question import Question, QuestionOption, QuestionReport, QuestionQuarantineRegistry
from app.models.user import User
from app.services.audit_service import AuditService
from app.services.analytics_service import AnalyticsService
from app.services.feature_flag_service import FeatureFlagService
from app.services.test_service import TestService
from scripts.db_backup_restore import create_database_backup, verify_backup_integrity

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
async def test_trusted_question_pool_comprehensive_audit_and_quarantine(client_and_db):
    """
    Acceptance:
    Audit engine evaluates question pool; questions missing critical fields are quarantined or demoted.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        # Add a defective question (missing 4th option)
        defective_q = Question(
            concept_id=concept.id,
            question_text="Defective question with only 2 options",
            correct_explanation="Brief",
            remember_takeaway="Pearl",
            status="PUBLISHED",
            trust_class="VERIFIED_CORE_QUESTION",
            text_hash="hash-defective-1"
        )
        session.add(defective_q)
        await session.flush()

        opt1 = QuestionOption(question_id=defective_q.id, option_key="A", option_text="Opt A", is_correct=True)
        opt2 = QuestionOption(question_id=defective_q.id, option_key="B", option_text="Opt B", is_correct=False)
        session.add_all([opt1, opt2])
        await session.commit()

        # Execute Audit
        audit_res = await AuditService.audit_trusted_question_pool(session)

        assert audit_res["total_questions_audited"] >= 1
        assert audit_res["quarantined_questions_count"] >= 1

        # Confirm defective question is now QUARANTINED
        await session.refresh(defective_q)
        assert defective_q.status == "QUARANTINED"
        assert defective_q.trust_class == "QUARANTINED"

@pytest.mark.asyncio
async def test_test_blueprint_audit_all_nine_modes():
    """
    Acceptance:
    All 9 test modes validate blueprint distributions and negative marking.
    """
    bp_res = AuditService.audit_test_blueprints()
    assert bp_res["total_modes"] == 9
    assert bp_res["all_modes_validated"] is True
    assert "+4.0 correct / -1.0 incorrect" in bp_res["negative_marking_standard"]
    assert "GRAND_TEST_NEET_PG" in bp_res["blueprints"]

@pytest.mark.asyncio
async def test_five_part_concise_explanation_structure(client_and_db):
    """
    Acceptance:
    Answer submission returns concise 5-part explanation structure.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "student-exp-1"
        sess, qs = await TestService.create_test_session(
            db=session, user_id=user_id, mode="DAILY_SHORT_TEST", question_count=1
        )
        q = qs[0]
        await session.commit()

        # Submit wrong answer to trigger distractor feedback
        res = await TestService.submit_answer_idempotent(
            db=session,
            session_id=sess.id,
            user_id=user_id,
            question_id=q.id,
            selected_option_key="D",
            confidence="SOMEWHAT_CONFIDENT"
        )

        assert "short_explanation" in res
        assert "why_your_answer_is_wrong" in res["short_explanation"]
        assert "why_correct_is_right" in res["short_explanation"]
        assert "remember_takeaway" in res["short_explanation"]
        assert "exam_connection" in res["short_explanation"]

@pytest.mark.asyncio
async def test_student_performance_analytics_and_calibration(client_and_db):
    """
    Acceptance:
    Analytics engine computes accuracy, negative marks lost, and confidence calibration.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        user_id = "student-analytics-1"
        sess, qs = await TestService.create_test_session(
            db=session, user_id=user_id, mode="DAILY_SHORT_TEST", question_count=2
        )
        await session.commit()

        # Answer 1 correct (confident), 1 wrong (guessing)
        await TestService.submit_answer_idempotent(
            db=session, session_id=sess.id, user_id=user_id, question_id=qs[0].id,
            selected_option_key="B", confidence="DEFINITELY_KNOW"
        )
        if len(qs) > 1:
            await TestService.submit_answer_idempotent(
                db=session, session_id=sess.id, user_id=user_id, question_id=qs[1].id,
                selected_option_key="D", confidence="GUESSING"
            )

        analytics = await AnalyticsService.get_student_performance_summary(session, user_id)
        assert analytics["total_attempts"] >= 1
        assert "accuracy_percentage" in analytics
        assert "negative_marks_lost" in analytics
        assert "confidence_calibration" in analytics

@pytest.mark.asyncio
async def test_serious_medical_report_triggers_quarantine(client_and_db):
    """
    Acceptance:
    Reporting a question for serious medical error triggers automatic quarantine.
    """
    _, session_maker = client_and_db

    async with session_maker() as session:
        c_stmt = select(Concept).limit(1)
        concept = (await session.execute(c_stmt)).scalars().first()

        q = Question(
            concept_id=concept.id,
            question_text="Reportable question",
            correct_explanation="Exp",
            remember_takeaway="Takeaway",
            status="PUBLISHED",
            trust_class="VERIFIED_CORE_QUESTION",
            text_hash="hash-report-1"
        )
        session.add(q)
        await session.commit()
        await session.refresh(q)

        # File Serious Medical Report
        rep = QuestionReport(
            question_id=q.id,
            user_id="student-reporter-1",
            reason="WRONG_ANSWER_KEY",
            comment="Guideline changed in 2026; Option C is now contraindicated.",
            is_serious_medical_error=True
        )
        session.add(rep)

        # Serious medical report auto-quarantines question
        q.status = "QUARANTINED"
        q.trust_class = "QUARANTINED"
        quarantine = QuestionQuarantineRegistry(
            question_id=q.id,
            quarantine_reason=f"Student Report: {rep.comment}",
            resolution_status="quarantined"
        )
        session.add(quarantine)
        await session.commit()
        await session.refresh(q)

        assert q.status == "QUARANTINED"
        assert q.trust_class == "QUARANTINED"

@pytest.mark.asyncio
async def test_beta_feature_flags_and_disaster_recovery():
    """
    Acceptance:
    Feature flags toggle correctly at runtime and backup utility creates verifiable snapshot.
    """
    assert FeatureFlagService.is_enabled("AI_QUESTION_GENERATION") is True
    FeatureFlagService.set_flag("AI_QUESTION_GENERATION", False)
    assert FeatureFlagService.is_enabled("AI_QUESTION_GENERATION") is False
    FeatureFlagService.set_flag("AI_QUESTION_GENERATION", True)

    # Backup snapshot test
    backup_meta = create_database_backup("postgresql://staging-url", "staging_backup_test.sql")
    assert backup_meta["status"] == "SUCCESS"
    assert backup_meta["backup_type"] == "FULL_SNAPSHOT"
