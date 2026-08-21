import asyncio
import httpx
import uuid

BASE_URL = "http://localhost:8000/api/v1"

async def test_cycle(mode: str, count: int, topic_id=None, subject_id=None):
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Login or register student
        email = f"student_test_{uuid.uuid4().hex[:8]}@example.com"
        reg_res = await client.post("/auth/register", json={
            "email": email,
            "password": "Password123!",
            "full_name": "Test Doctor",
            "target_exam_year": 2026
        })
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Start Test
        req_payload = {
            "mode": mode,
            "question_count": count,
            "total_questions": count,
            "topic_id": topic_id,
            "subject_id": subject_id
        }
        start_res = await client.post("/tests/generate", json=req_payload, headers=headers)
        assert start_res.status_code == 201, f"Failed start: {start_res.text}"
        data = start_res.json()
        session_id = data["session_id"]
        questions = data["questions"]
        print(f"\n[CYCLE: {mode}] Requested: {count}, Received: {len(questions)} questions (Session: {session_id})")
        assert len(questions) == count or len(questions) >= min(count, 5), f"Unexpected question count: {len(questions)}"

        # 3. Answer questions
        for idx, q in enumerate(questions):
            ans_res = await client.post(f"/tests/{session_id}/answers", json={
                "question_id": q["id"],
                "selected_option_key": "A",
                "confidence": "DEFINITELY_KNOW" if idx % 2 == 0 else "GUESSING",
                "time_spent_seconds": 25
            }, headers=headers)
            assert ans_res.status_code == 200, f"Failed submit answer: {ans_res.text}"

        # 4. Submit / Complete Test
        submit_res = await client.post(f"/tests/{session_id}/submit", headers=headers)
        assert submit_res.status_code == 200, f"Failed complete: {submit_res.text}"
        result = submit_res.json()

        # 5. Verify result payload fields
        assert "mode" in result and result["mode"] is not None, "Missing mode in result!"
        assert "scoring" in result, "Missing scoring in result!"
        assert "question_breakdowns" in result, "Missing question_breakdowns!"
        assert result["scoring"]["score"] is not None
        assert result["scoring"]["accuracy_percentage"] is not None
        assert result["scoring"]["calibration_percentage"] is not None

        print(f"  -> Result OK: Mode='{result['mode']}', Score={result['scoring']['score']}, Accuracy={result['scoring']['accuracy_percentage']}%, Calibration={result['scoring']['calibration_percentage']}%, Breakdowns={len(result['question_breakdowns'])}")

async def main():
    print("=== RUNNING 3 E2E TEST CYCLES ===")
    # Cycle 1: Quick Test (10 questions)
    await test_cycle("quick_test", 10)

    # Cycle 2: Topic Test with expansion
    await test_cycle("topic_test", 10)

    # Cycle 3: Subject Test (5 questions)
    await test_cycle("subject_test", 5)
    print("\nALL 3 TEST CYCLES COMPLETED SUCCESSFULLY WITH ZERO CRASHES!")

if __name__ == "__main__":
    asyncio.run(main())
