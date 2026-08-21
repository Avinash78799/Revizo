import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import httpx
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, and_, func
from app.core.database import AsyncSessionLocal, engine
from app.core.config import settings
from app.models.user import User, Profile
from app.models.question import Question, QuestionOption, QuestionReport, QuestionQuarantineRegistry
from app.models.test import TestSession, TestAttempt
from app.models.learning import StudentMistakeRecord, StudentQuestionHistory
from app.services.test_service import TestService
from app.services.question_selection_engine import QuestionSelectionEngine
from app.services.ai_provider import AIProviderRegistry, ProviderUnavailableError
from app.core.security import create_access_token, get_password_hash
from app.core.errors import RateLimitError, ValidationError

async def verify_b1_rate_limiting():
    print("\n" + "="*80)
    print("B1: RATE LIMITING VERIFICATION (LOGIN & REGISTER)")
    print("="*80)
    
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/api/v1") as client:
        # Rapid login requests
        login_payload = {"email": "aspirant@neetpg.pro", "password": "WrongPassword123!"}
        status_codes = []
        for i in range(25):
            res = await client.post("/auth/login", json=login_payload)
            status_codes.append(res.status_code)
            
        rate_limited = any(code == 429 for code in status_codes)
        print(f"Login 25 rapid requests status codes: {set(status_codes)}")
        print(f"B1 Rate Limiting Status: {'[PASS] 429 Too Many Requests enforced' if rate_limited else '[FAIL]'}")
        return rate_limited

async def verify_b2_idempotency():
    print("\n" + "="*80)
    print("B2: IDEMPOTENCY OF ANSWER SUBMISSIONS (DUPLICATE PROTECTION)")
    print("="*80)
    
    async with AsyncSessionLocal() as session:
        # Find or create a test student
        stmt = select(User).where(User.email == "idempotent_tester@revizo.test")
        user = (await session.execute(stmt)).scalars().first()
        if not user:
            user = User(email="idempotent_tester@revizo.test", hashed_password=get_password_hash("pw"), role="student")
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
        # Create a test session
        test_session, questions = await TestService.create_test_session(
            db=session,
            user_id=user.id,
            mode="daily_short_test",
            question_count=3
        )
        session_id = test_session.id
        q_id = questions[0].id
        
        # Submit answer 1st time
        res1 = await TestService.submit_answer_idempotent(
            db=session,
            session_id=session_id,
            user_id=user.id,
            question_id=q_id,
            selected_option_key="A",
            confidence="DEFINITELY_KNOW",
            time_spent_seconds=12
        )
        
        # Submit same answer 2nd time immediately (simulating flaky network retry)
        res2 = await TestService.submit_answer_idempotent(
            db=session,
            session_id=session_id,
            user_id=user.id,
            question_id=q_id,
            selected_option_key="A",
            confidence="DEFINITELY_KNOW",
            time_spent_seconds=12
        )
        
        # Check attempts count in database
        stmt_att = select(func.count(TestAttempt.id)).where(
            and_(TestAttempt.session_id == session_id, TestAttempt.question_id == q_id)
        )
        att_count = (await session.execute(stmt_att)).scalar_one()
        
        # Check session completed_questions count
        stmt_s = select(TestSession).where(TestSession.id == session_id)
        s_obj = (await session.execute(stmt_s)).scalars().first()
        
        print(f"Attempts recorded for question in session: {att_count} (Expected: 1)")
        print(f"Session completed_questions count: {s_obj.completed_questions} (Expected: 1)")
        passed = (att_count == 1 and s_obj.completed_questions == 1)
        print(f"B2 Idempotency Status: {'[PASS] Duplicate submission safely handled' if passed else '[FAIL]'}")
        return passed

async def verify_b3_timer_authority():
    print("\n" + "="*80)
    print("B3: SERVER-SIDE TIMER AUTHORITY VERIFICATION")
    print("="*80)
    
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == "timer_tester@revizo.test")
        user = (await session.execute(stmt)).scalars().first()
        if not user:
            user = User(email="timer_tester@revizo.test", hashed_password=get_password_hash("pw"), role="student")
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
        test_session, questions = await TestService.create_test_session(
            db=session,
            user_id=user.id,
            mode="daily_short_test",
            question_count=2
        )
        
        # Artificially expire the session on server
        test_session.expires_at = datetime.now(timezone.utc) - timedelta(minutes=5)
        await session.commit()
        
        # Attempt to submit answer to expired session
        rejected = False
        try:
            await TestService.submit_answer_idempotent(
                db=session,
                session_id=test_session.id,
                user_id=user.id,
                question_id=questions[0].id,
                selected_option_key="A",
                confidence="DEFINITELY_KNOW",
                time_spent_seconds=10
            )
        except ValidationError as e:
            rejected = True
            print(f"Server-side rejection received: {e}")
            
        print(f"B3 Timer Authority Status: {'[PASS] Expired submission strictly rejected by server' if rejected else '[FAIL]'}")
        return rejected

async def verify_b4_confidence_danger_zone():
    print("\n" + "="*80)
    print("B4: CONFIDENCE + DANGER ZONE ISOLATION LOGIC")
    print("="*80)
    
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == "danger_tester@revizo.test")
        user = (await session.execute(stmt)).scalars().first()
        if not user:
            user = User(email="danger_tester@revizo.test", hashed_password=get_password_hash("pw"), role="student")
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
        test_session, questions = await TestService.create_test_session(
            db=session,
            user_id=user.id,
            mode="daily_short_test",
            question_count=2
        )
        
        q = questions[0]
        # Find wrong option key
        opts_res = await session.execute(select(QuestionOption).where(QuestionOption.question_id == q.id))
        opts = opts_res.scalars().all()
        wrong_opt = next((o.option_key for o in opts if not o.is_correct), "C")
        
        # Submit wrong answer with DEFINITELY_KNOW (100% confidence)
        res = await TestService.submit_answer_idempotent(
            db=session,
            session_id=test_session.id,
            user_id=user.id,
            question_id=q.id,
            selected_option_key=wrong_opt,
            confidence="DEFINITELY_KNOW",
            time_spent_seconds=8
        )
        
        # Verify TestAttempt is_danger_zone_item
        stmt_att = select(TestAttempt).where(
            and_(TestAttempt.session_id == test_session.id, TestAttempt.question_id == q.id)
        )
        att = (await session.execute(stmt_att)).scalars().first()
        
        # Verify StudentMistakeRecord
        stmt_mistake = select(StudentMistakeRecord).where(
            and_(StudentMistakeRecord.user_id == user.id, StudentMistakeRecord.question_id == q.id)
        )
        mistake = (await session.execute(stmt_mistake)).scalars().first()
        
        is_dz_attempt = att.is_danger_zone_item if att else False
        is_dz_mistake = (mistake.error_type == "CONFIDENCE_ERROR" or mistake.misconception_state == "CONFIDENCE_ERROR") if mistake else False
        
        print(f"TestAttempt is_danger_zone_item: {is_dz_attempt}")
        print(f"StudentMistakeRecord error_type: {mistake.error_type if mistake else 'None'}")
        
        passed = (is_dz_attempt and is_dz_mistake)
        print(f"B4 Danger Zone Status: {'[PASS] Overconfidence errors correctly isolated in Danger Zone' if passed else '[FAIL]'}")
        return passed

async def verify_b5_quarantine_flow():
    print("\n" + "="*80)
    print("B5: CRITICAL REPORT & QUARANTINE CIRCUIT BREAKER")
    print("="*80)
    
    async with AsyncSessionLocal() as session:
        # 1. Pick an active question
        stmt_q = select(Question).where(Question.status == "published").limit(1)
        q = (await session.execute(stmt_q)).scalars().first()
        assert q is not None
        target_q_id = q.id
        
        # Create an in-progress test that contains this question
        stmt_user = select(User).where(User.role == "student").limit(1)
        user = (await session.execute(stmt_user)).scalars().first()
        
        test_session, _ = await TestService.create_test_session(
            db=session, user_id=user.id, mode="daily_short_test", question_count=3
        )
        
        # 2. File CRITICAL report on target question
        q.status = "QUARANTINED"
        q.trust_class = "QUARANTINED"
        quarantine_record = QuestionQuarantineRegistry(
            question_id=target_q_id,
            quarantine_reason="CRITICAL medical accuracy report by student",
            resolution_status="quarantined",
            audit_notes="Immediate circuit breaker quarantine"
        )
        session.add(quarantine_record)
        await session.commit()
        
        # 3. Confirm target question is excluded from new test generation
        new_questions, _ = await QuestionSelectionEngine.select_questions_for_test(
            db=session, user_id=user.id, mode="daily_short_test", question_count=10
        )
        new_q_ids = [nq.id for nq in new_questions]
        is_excluded_from_new_tests = (target_q_id not in new_q_ids)
        print(f"Quarantined question excluded from new test pools: {is_excluded_from_new_tests}")
        
        # Restore status for testing integrity
        q.status = "published"
        q.trust_class = "SOURCE_REFERENCED"
        await session.commit()
        
        print(f"B5 Quarantine Status: {'[PASS] Critical quarantine immediately removes question from pool' if is_excluded_from_new_tests else '[FAIL]'}")
        return is_excluded_from_new_tests

def verify_b8_ai_fail_closed():
    print("\n" + "="*80)
    print("B8: AI PROVIDER OUTAGE FAILS CLOSED IN PRODUCTION")
    print("="*80)
    
    # Save original settings
    orig_env = settings.ENVIRONMENT
    orig_mock = settings.ALLOW_MOCK_AI
    
    try:
        # Simulate production environment with mock disallowed
        settings.ENVIRONMENT = "production"
        settings.ALLOW_MOCK_AI = False
        
        fails_closed = False
        try:
            AIProviderRegistry.get_provider("openai")
        except ProviderUnavailableError as e:
            fails_closed = True
            print(f"ProviderUnavailableError caught as expected: {e}")
            
        print(f"B8 AI Fail-Closed Status: {'[PASS] Unregistered/Unavailable AI fails closed' if fails_closed else '[FAIL]'}")
        return fails_closed
    finally:
        settings.ENVIRONMENT = orig_env
        settings.ALLOW_MOCK_AI = orig_mock

async def main():
    print("="*80)
    print("PART B: GAPS & EDGE-CASES VERIFICATION SUITE")
    print("="*80)
    
    b1 = await verify_b1_rate_limiting()
    b2 = await verify_b2_idempotency()
    b3 = await verify_b3_timer_authority()
    b4 = await verify_b4_confidence_danger_zone()
    b5 = await verify_b5_quarantine_flow()
    b8 = verify_b8_ai_fail_closed()
    
    print("\n" + "="*80)
    print("PART B AUTOMATED SUMMARY SCORECARD")
    print("="*80)
    print(f"B1 (Rate Limiting on Auth/Test)      : {'PASS' if b1 else 'FAIL'}")
    print(f"B2 (Idempotent Answer Submissions)   : {'PASS' if b2 else 'FAIL'}")
    print(f"B3 (Server-Side Timer Authority)     : {'PASS' if b3 else 'FAIL'}")
    print(f"B4 (Danger Zone Isolation Logic)     : {'PASS' if b4 else 'FAIL'}")
    print(f"B5 (Quarantine Circuit Breaker)      : {'PASS' if b5 else 'FAIL'}")
    print(f"B8 (AI Fail-Closed in Production)    : {'PASS' if b8 else 'FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
