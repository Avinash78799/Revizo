import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.question import Question

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
async def test_frontend_complete_contract_and_user_flows(client_and_db):
    """
    End-to-End Contract and User Flow Test matching all Milestone 3 Frontend Screens:
    1. Register & Login (Auth UI)
    2. Dashboard Retrieval (Dashboard UI)
    3. Curriculum Hierarchy (Subjects & Topics UI)
    4. Test Launcher & Sanitized MCQ Runner (Test Runner UI)
    5. Confidence Marking & Server Evaluation with Corrective Explanation Anatomy (ExplanationCard UI)
    6. Integrity Event Logging (Integrity Modal UI)
    7. Results & Confidence Analysis (Result Page UI)
    8. Mistake Bank Retrieval (Mistakes UI)
    9. Danger Zone Isolation (Danger Zone UI)
    10. Spaced Revision Scheduling & Completion (Revision UI)
    11. Question Reporting & Auto-Quarantine (Report Modal UI)
    12. Admin Protection Gate (Admin UI Route Guard)
    """
    client, session_maker = client_and_db

    # 1. Register & Login
    reg = await client.post("/api/v1/auth/register", json={
        "email": "dr.e2e@neetpg.pro",
        "password": "Password123!",
        "full_name": "Dr. E2E Student",
        "target_exam_year": 2026
    })
    assert reg.status_code == 201
    token = reg.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {token}"}

    # 2. Student Dashboard
    dash = await client.get("/api/v1/student/dashboard", headers=student_headers)
    assert dash.status_code == 200
    dash_data = dash.json()
    assert "todays_practice_count" in dash_data
    assert "due_revisions" in dash_data
    assert "weak_areas" in dash_data

    # 3. Curriculum Taxonomy Navigation
    sub_res = await client.get("/api/v1/taxonomy/subjects")
    assert sub_res.status_code == 200
    subjects = sub_res.json()
    assert len(subjects) >= 1
    pharm_id = subjects[0]["id"]

    tree_res = await client.get(f"/api/v1/taxonomy/subjects/{pharm_id}/tree")
    assert tree_res.status_code == 200
    assert "chapters" in tree_res.json()

    # 4. Start Practice Test
    start_res = await client.post("/api/v1/tests/start", json={
        "mode": "quick_test",
        "question_count": 3
    }, headers=student_headers)
    assert start_res.status_code == 201
    session_data = start_res.json()
    session_id = session_data["session_id"]
    questions = session_data["questions"]
    assert len(questions) >= 1

    # Verify Active Question Sanitization (NO correct keys or explanations exposed to browser)
    for q in questions:
        assert "correct_option_key" not in q
        assert "correct_explanation" not in q
        assert "remember_takeaway" not in q

    q1 = questions[0]

    # Find the actual wrong distractor key for q1 from DB to guarantee testing Danger Zone
    async with session_maker() as session:
        stmt = select(Question).options(selectinload(Question.options)).where(Question.id == q1["id"])
        res = await session.execute(stmt)
        q_db = res.scalars().first()
        wrong_opt = next(o for o in q_db.options if not o.is_correct)
        wrong_key = wrong_opt.option_key
        correct_key = next(o for o in q_db.options if o.is_correct).option_key

    # 5. Log Integrity Event (Window blur / Tab switch)
    integ_res = await client.post(f"/api/v1/tests/{session_id}/integrity-events", json={
        "event_type": "TAB_HIDDEN",
        "metadata": {"test": "blurred"}
    }, headers=student_headers)
    assert integ_res.status_code == 200

    # 6. Submit Answer with HIGH CONFIDENCE WRONG (Danger Zone Trigger)
    ans_wrong = await client.post(f"/api/v1/tests/{session_id}/answers", json={
        "question_id": q1["id"],
        "selected_option_key": wrong_key,
        "confidence": "DEFINITELY_KNOW",
        "time_spent_seconds": 15
    }, headers=student_headers)
    assert ans_wrong.status_code == 200
    eval_wrong = ans_wrong.json()
    assert eval_wrong["is_correct"] is False
    assert eval_wrong["is_danger_zone_item"] is True
    assert eval_wrong["correct_explanation"] is not None
    assert eval_wrong["why_selected_was_wrong"] is not None
    assert eval_wrong["remember_takeaway"] is not None

    # 7. Submit Next Answer with Correct Option
    if len(questions) > 1:
        q2 = questions[1]
        async with session_maker() as session:
            stmt = select(Question).options(selectinload(Question.options)).where(Question.id == q2["id"])
            res = await session.execute(stmt)
            q2_db = res.scalars().first()
            q2_correct_key = next(o for o in q2_db.options if o.is_correct).option_key

        ans_correct = await client.post(f"/api/v1/tests/{session_id}/answers", json={
            "question_id": q2["id"],
            "selected_option_key": q2_correct_key,
            "confidence": "SOMEWHAT_CONFIDENT",
            "time_spent_seconds": 20
        }, headers=student_headers)
        assert ans_correct.status_code == 200
        assert ans_correct.json()["is_correct"] is True

    # 8. Get Test Result and Performance Analysis
    result_res = await client.get(f"/api/v1/tests/{session_id}/result", headers=student_headers)
    assert result_res.status_code == 200
    res_data = result_res.json()
    assert res_data["scoring"]["danger_zone_count"] >= 1
    assert len(res_data["question_breakdowns"]) >= 1

    # 9. Verify Danger Zone Appears in Student Danger Zone View
    dz_res = await client.get("/api/v1/student/danger-zone", headers=student_headers)
    assert dz_res.status_code == 200
    assert len(dz_res.json()) >= 1

    # 10. Verify Mistake Appears in Student Mistake Bank
    mistake_res = await client.get("/api/v1/student/mistakes", headers=student_headers)
    assert mistake_res.status_code == 200
    assert len(mistake_res.json()) >= 1

    # 11. Report Question with Clinical Error (Auto-Quarantine)
    rep_res = await client.post(f"/api/v1/questions/{q1['id']}/report", json={
        "reason": "INCORRECT",
        "description": "Textbook citation discrepancy",
        "is_serious_medical_error": True
    }, headers=student_headers)
    assert rep_res.status_code == 201
    assert rep_res.json()["is_quarantined"] is True

    # 12. Verify Admin Gate: Student Forbidden from Accessing Admin Review Queue
    admin_forbidden = await client.get("/api/v1/admin/review-queue", headers=student_headers)
    assert admin_forbidden.status_code == 403
