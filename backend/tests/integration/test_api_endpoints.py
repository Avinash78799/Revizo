import pytest
import pytest_asyncio
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import Base, get_db
from app.db.seed import seed_database
from app.models.test import TestSession
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
async def test_health_and_readiness(client_and_db):
    client, _ = client_and_db
    
    # Health probe
    h_res = await client.get("/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "healthy"

    # Readiness probe
    r_res = await client.get("/ready")
    assert r_res.status_code == 200
    assert r_res.json()["status"] == "ready"

@pytest.mark.asyncio
async def test_complete_student_flow(client_and_db):
    client, _ = client_and_db

    # 1. Register & Login
    reg_resp = await client.post("/api/v1/auth/register", json={
        "email": "dr.aspirant.full@neetpg.pro",
        "password": "StrongPassword123!",
        "full_name": "Dr. Aspirant",
        "target_exam_year": 2026
    })
    assert reg_resp.status_code == 201
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Browse Taxonomy
    tax_resp = await client.get("/api/v1/taxonomy/subjects")
    assert tax_resp.status_code == 200
    subjects = tax_resp.json()
    assert len(subjects) >= 1
    pharm_id = subjects[0]["id"]

    tree_resp = await client.get(f"/api/v1/taxonomy/subjects/{pharm_id}/tree")
    assert tree_resp.status_code == 200

    # 3. Start Test
    test_resp = await client.post("/api/v1/tests/start", json={
        "mode": "quick_test",
        "question_count": 3
    }, headers=headers)
    assert test_resp.status_code == 201
    test_data = test_resp.json()
    session_id = test_data["session_id"]
    questions = test_data["questions"]
    assert len(questions) >= 1

    first_q = questions[0]
    
    # 4. Submit Answer
    ans_resp = await client.post(f"/api/v1/tests/{session_id}/answers", json={
        "question_id": first_q["id"],
        "selected_option_key": "B",
        "confidence": "DEFINITELY_KNOW",
        "time_spent_seconds": 22
    }, headers=headers)
    assert ans_resp.status_code == 200
    eval_res = ans_resp.json()
    assert isinstance(eval_res["is_correct"], bool)
    assert eval_res["correct_explanation"] is not None
    assert eval_res["remember_takeaway"] is not None

    # 5. Get Test Result
    result_resp = await client.get(f"/api/v1/tests/{session_id}/result", headers=headers)
    assert result_resp.status_code == 200
    res_payload = result_resp.json()
    assert "scoring" in res_payload
    assert res_payload["scoring"]["attempted_count"] >= 1

    # 6. Spaced Revision Due Check & Complete
    due_resp = await client.get("/api/v1/revision/due", headers=headers)
    assert due_resp.status_code == 200

    # 7. Start 5-Minute Revision Session
    five_min_resp = await client.post("/api/v1/revision/five-minute-session", headers=headers)
    assert five_min_resp.status_code == 201
    assert len(five_min_resp.json()["questions"]) >= 1

    # 8. Report Question
    rep_resp = await client.post(f"/api/v1/questions/{first_q['id']}/report", json={
        "reason": "TYPO",
        "description": "Minor punctuation correction"
    }, headers=headers)
    assert rep_resp.status_code == 201

@pytest.mark.asyncio
async def test_attack_idor_submission_to_another_users_attempt(client_and_db):
    client, _ = client_and_db

    # Register Student A
    res_a = await client.post("/api/v1/auth/register", json={
        "email": "student_a@neetpg.pro",
        "password": "Password123!"
    })
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Register Student B
    res_b = await client.post("/api/v1/auth/register", json={
        "email": "student_b@neetpg.pro",
        "password": "Password123!"
    })
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Student A starts test
    start_a = await client.post("/api/v1/tests/start", json={"mode": "quick_test", "question_count": 2}, headers=headers_a)
    session_a_id = start_a.json()["session_id"]
    question_a_id = start_a.json()["questions"][0]["id"]

    # Student B attempts IDOR attack: submit answer to Student A's test
    attack_submit = await client.post(f"/api/v1/tests/{session_a_id}/answers", json={
        "question_id": question_a_id,
        "selected_option_key": "A",
        "confidence": "GUESSING"
    }, headers=headers_b)
    assert attack_submit.status_code == 403

    # Student B attempts IDOR attack: view Student A's test results
    attack_view = await client.get(f"/api/v1/tests/{session_a_id}/result", headers=headers_b)
    assert attack_view.status_code == 403

@pytest.mark.asyncio
async def test_idempotency_double_click_submission(client_and_db):
    client, _ = client_and_db

    res_user = await client.post("/api/v1/auth/register", json={
        "email": "idempotent_user@neetpg.pro",
        "password": "Password123!"
    })
    headers = {"Authorization": f"Bearer {res_user.json()['access_token']}"}

    start = await client.post("/api/v1/tests/start", json={"mode": "quick_test", "question_count": 2}, headers=headers)
    session_id = start.json()["session_id"]
    q_id = start.json()["questions"][0]["id"]

    # First Submission
    sub1 = await client.post(f"/api/v1/tests/{session_id}/answers", json={
        "question_id": q_id,
        "selected_option_key": "B",
        "confidence": "DEFINITELY_KNOW"
    }, headers=headers)
    assert sub1.status_code == 200
    assert sub1.json()["is_duplicate_submission"] is False

    # Second Duplicate Submission (double click / network retry)
    sub2 = await client.post(f"/api/v1/tests/{session_id}/answers", json={
        "question_id": q_id,
        "selected_option_key": "B",
        "confidence": "DEFINITELY_KNOW"
    }, headers=headers)
    assert sub2.status_code == 200
    assert sub2.json()["is_duplicate_submission"] is True

    # Verify score count is exactly 1, not double-counted
    result = await client.get(f"/api/v1/tests/{session_id}/result", headers=headers)
    assert result.json()["scoring"]["attempted_count"] == 1

@pytest.mark.asyncio
async def test_attack_submitting_after_expiration(client_and_db):
    client, session_maker = client_and_db

    res_user = await client.post("/api/v1/auth/register", json={
        "email": "timer_test_user@neetpg.pro",
        "password": "Password123!"
    })
    headers = {"Authorization": f"Bearer {res_user.json()['access_token']}"}

    start = await client.post("/api/v1/tests/start", json={"mode": "quick_test", "question_count": 2}, headers=headers)
    session_id = start.json()["session_id"]
    q_id = start.json()["questions"][0]["id"]

    # Manually expire the session in the database
    async with session_maker() as session:
        stmt = select(TestSession).where(TestSession.id == session_id)
        res = await session.execute(stmt)
        s_obj = res.scalars().first()
        s_obj.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)
        await session.commit()

    # Attempt submission to expired session
    late_submit = await client.post(f"/api/v1/tests/{session_id}/answers", json={
        "question_id": q_id,
        "selected_option_key": "B",
        "confidence": "SOMEWHAT_CONFIDENT"
    }, headers=headers)
    assert late_submit.status_code == 422
    assert "expired" in late_submit.json()["error"]["message"].lower()

@pytest.mark.asyncio
async def test_admin_taxonomy_safe_deletion(client_and_db):
    client, _ = client_and_db

    admin_login = await client.post("/api/v1/auth/login", json={
        "email": "admin@neetpg.pro",
        "password": "AdminSecure123!"
    })
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    # 1. Create a subject, chapter, topic, concept
    sub_res = await client.post("/api/v1/taxonomy/subjects", json={
        "name": "Biochemistry",
        "code": "BIOCHEM",
        "description": "Medical Biochemistry"
    }, headers=admin_headers)
    assert sub_res.status_code == 201
    sub_id = sub_res.json()["id"]

    chap_res = await client.post("/api/v1/taxonomy/chapters", json={
        "subject_id": sub_id,
        "name": "Enzymes"
    }, headers=admin_headers)
    assert chap_res.status_code == 201
    chap_id = chap_res.json()["id"]

    top_res = await client.post("/api/v1/taxonomy/topics", json={
        "chapter_id": chap_id,
        "name": "Enzyme Kinetics"
    }, headers=admin_headers)
    assert top_res.status_code == 201
    top_id = top_res.json()["id"]

    con_res = await client.post("/api/v1/taxonomy/concepts", json={
        "topic_id": top_id,
        "name": "Michaelis-Menten Kinetics"
    }, headers=admin_headers)
    assert con_res.status_code == 201
    con_id = con_res.json()["id"]

    # Delete unlinked concept -> success
    del_res = await client.delete(f"/api/v1/taxonomy/concepts/{con_id}", headers=admin_headers)
    assert del_res.status_code == 200

@pytest.mark.asyncio
async def test_admin_question_lifecycle_transitions(client_and_db):
    client, session_maker = client_and_db

    admin_login = await client.post("/api/v1/auth/login", json={
        "email": "admin@neetpg.pro",
        "password": "AdminSecure123!"
    })
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    # Fetch a question
    async with session_maker() as session:
        stmt = select(Question).where(Question.status == "published")
        res = await session.execute(stmt)
        q = res.scalars().first()
        q_id = q.id

    # Quarantine question
    quar_res = await client.post(f"/api/v1/admin/questions/{q_id}/quarantine", json={
        "reason": "Expert review dispute",
        "audit_notes": "Temporarily quarantined for guideline revision"
    }, headers=admin_headers)
    assert quar_res.status_code == 200
    assert quar_res.json()["status"] == "quarantined"
