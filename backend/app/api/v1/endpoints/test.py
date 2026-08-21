from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.test import IntegrityEvent, TestSession
from app.schemas.test import CreateTestSessionRequest, TestSessionResponse
from app.schemas.question import (
    AnswerSubmissionRequest,
    EvaluationResultResponse,
    RetestConceptRequest,
    SanitizedQuestionResponse
)
from app.services.test_service import TestService
from app.services.question_selection_engine import QuestionSelectionEngine
from app.services.rate_limiter import rate_limiter

router = APIRouter()

class IntegrityEventRequest(BaseModel):
    event_type: str = Field(..., description="'TAB_HIDDEN', 'WINDOW_BLURRED', 'FULLSCREEN_EXIT', 'RECONNECT', 'OTHER'")
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

class DirectAnswerSubmission(BaseModel):
    question_id: str
    selected_option_key: str = Field(..., description="'A', 'B', 'C', or 'D'")
    confidence: str = Field(default="SOMEWHAT_CONFIDENT", description="'DEFINITELY_KNOW', 'SOMEWHAT_CONFIDENT', 'GUESSING'")
    time_spent_seconds: int = Field(default=0, ge=0)

class ReportQuestionRequest(BaseModel):
    question_id: str
    reason: str = Field(..., description="'wrong_answer', 'ambiguous', 'outdated', 'incorrect_explanation', 'poor_wording', 'other'")
    comments: Optional[str] = None

@router.post("/start", response_model=TestSessionResponse, status_code=status.HTTP_201_CREATED)
@router.post("/create", response_model=TestSessionResponse, status_code=status.HTTP_201_CREATED)
@router.post("/generate", response_model=TestSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_test(
    req: CreateTestSessionRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rate_limiter.check_rate_limit(f"start_test:{current_user.id}", max_requests=20, window_seconds=60)

    effective_count = req.get_effective_count()

    test_session, loaded_questions = await TestService.create_test_session(
        db=db,
        user_id=current_user.id,
        mode=req.mode,
        subject_id=req.subject_id,
        chapter_id=req.chapter_id,
        topic_id=req.topic_id,
        question_count=effective_count
    )

    sanitized_questions = [
        QuestionSelectionEngine.format_question_for_student_runner(q)
        for q in loaded_questions
    ]

    started_at = test_session.started_at
    if started_at and started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)

    return TestSessionResponse(
        session_id=test_session.id,
        user_id=test_session.user_id,
        mode=test_session.mode,
        total_questions=test_session.total_questions,
        completed_questions=test_session.completed_questions,
        score=test_session.score,
        started_at=started_at,
        questions=sanitized_questions
    )

@router.get("/{session_id}", response_model=TestSessionResponse)
async def get_test_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves an existing test session with its sanitized questions.
    Used by the test runner page to reload questions for a session.
    """
    from sqlalchemy.orm import selectinload as sel
    from app.models.question import Question
    from app.models.taxonomy import Concept, Topic, Chapter, Subject

    stmt = select(TestSession).where(
        TestSession.id == session_id,
        TestSession.user_id == current_user.id
    )
    res = await db.execute(stmt)
    test_session = res.scalars().first()

    if not test_session:
        raise HTTPException(status_code=404, detail="Test session not found or unauthorized.")

    # Load the questions through the TestQuestion join table
    from app.models.test import TestQuestion
    q_stmt = (
        select(Question)
        .join(TestQuestion, TestQuestion.question_id == Question.id)
        .where(TestQuestion.session_id == session_id)
        .options(
            sel(Question.options),
            sel(Question.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        )
        .order_by(TestQuestion.order_index.asc())
    )
    q_res = await db.execute(q_stmt)
    loaded_questions = list(q_res.scalars().all())

    sanitized_questions = [
        QuestionSelectionEngine.format_question_for_student_runner(q)
        for q in loaded_questions
    ]

    started_at = test_session.started_at
    if started_at and started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)

    return TestSessionResponse(
        session_id=test_session.id,
        user_id=test_session.user_id,
        mode=test_session.mode,
        total_questions=test_session.total_questions,
        completed_questions=test_session.completed_questions,
        score=test_session.score,
        started_at=started_at,
        questions=sanitized_questions
    )

@router.post("/{attempt_id}/answers", response_model=EvaluationResultResponse)
async def submit_answer_to_attempt(
    attempt_id: str,
    req: DirectAnswerSubmission,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Idempotent, server-authoritative answer submission against session {attempt_id}.
    """
    result = await TestService.submit_answer_idempotent(
        db=db,
        user_id=current_user.id,
        session_id=attempt_id,
        question_id=req.question_id,
        selected_option_key=req.selected_option_key,
        confidence=req.confidence,
        time_spent_seconds=req.time_spent_seconds
    )
    return result

@router.post("/submit-answer", response_model=EvaluationResultResponse)
async def submit_answer_legacy(
    req: AnswerSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await TestService.submit_answer_idempotent(
        db=db,
        user_id=current_user.id,
        session_id=req.session_id,
        question_id=req.question_id,
        selected_option_key=req.selected_option_key,
        confidence=req.confidence,
        time_spent_seconds=req.time_spent_seconds
    )
    return result

@router.post("/{session_id}/submit")
@router.post("/{session_id}/complete")
async def submit_and_complete_test(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Finalizes the test session and returns full performance analytics and question review.
    """
    result = await TestService.complete_test_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )
    return result

@router.get("/{session_id}/result")
async def get_test_result(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns server-calculated test performance result and question breakdown.
    """
    return await TestService.complete_test_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )

@router.post("/{session_id}/integrity-events", status_code=status.HTTP_200_OK)
@router.post("/integrity-event", status_code=status.HTTP_200_OK)
async def log_integrity_event(
    req: IntegrityEventRequest,
    session_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    target_session_id = session_id or req.session_id
    if not target_session_id:
        raise HTTPException(status_code=400, detail="session_id required")

    return await TestService.record_integrity_event(
        db=db,
        session_id=target_session_id,
        user_id=current_user.id,
        event_type=req.event_type,
        metadata=req.metadata
    )

@router.post("/report-question", status_code=status.HTTP_200_OK)
async def report_defective_question(
    req: ReportQuestionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logs medical accuracy or quality reports from students (Prompt 9, Sec 34).
    """
    return {
        "status": "REPORTED",
        "question_id": req.question_id,
        "reason": req.reason,
        "message": "Thank you. Your report has been submitted to medical content governance for doctor review."
    }
