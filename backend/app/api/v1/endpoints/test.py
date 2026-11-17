from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.test import IntegrityEvent, TestSession, TestTemplate, TestAttempt
from app.models.question import QuestionReport, QuestionQuarantineRegistry
from app.models.taxonomy import Subject
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

@router.get("/series")
@router.get("/templates")
async def get_test_series(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns available test series across all specialized categories:
    NEET-PG Pro, Medicine Prep, INI-CET, FMGE/NExT, Image-Based, Subject-Wise, and Rapid Drills.
    """
    stmt = select(TestTemplate).order_by(TestTemplate.created_at.desc())
    res = await db.execute(stmt)
    templates = res.scalars().all()

    # Query all 19 NMC subjects to ensure complete Subject-Wise Test coverage
    subj_stmt = select(Subject).order_by(Subject.order_index.asc())
    subj_res = await db.execute(subj_stmt)
    all_subjects = subj_res.scalars().all()

    neet_pg_pro_series = []
    medicine_prep_series = []
    inicet_series = []
    fmge_next_series = []
    image_based_series = []
    live_tests = []
    subject_tests = []
    quick_drills = []

    for t in templates:
        cfg = t.config or {}
        series_cat = cfg.get("series_category")
        item = {
            "id": t.id,
            "title": t.title,
            "mode": t.mode,
            "series_category": series_cat,
            "test_type": cfg.get("test_type", "CLINICAL VIGNETTE"),
            "badge": cfg.get("badge"),
            "clinical_focus": cfg.get("clinical_focus"),
            "target_audience": cfg.get("target_audience"),
            "question_count": cfg.get("question_count", 20),
            "time_limit_minutes": cfg.get("time_limit_minutes", 25),
            "is_live": cfg.get("is_live", False),
            "live_window_start": cfg.get("live_window_start"),
            "live_window_end": cfg.get("live_window_end"),
            "syllabus_tag": cfg.get("syllabus_tag", "High-Yield Curriculum"),
            "total_registered": cfg.get("total_registered", 1840),
            "subject_id": cfg.get("subject_id"),
            "subject_ids": cfg.get("subject_ids"),
            "subject_name": cfg.get("subject_name"),
            "subject_code": cfg.get("subject_code"),
            "difficulty": cfg.get("difficulty", "all")
        }

        # Categorize by series
        if series_cat == "neet_pg_pro":
            neet_pg_pro_series.append(item)
        elif series_cat == "medicine_prep":
            medicine_prep_series.append(item)
        elif series_cat == "inicet":
            inicet_series.append(item)
        elif series_cat == "fmge_next":
            fmge_next_series.append(item)
        elif series_cat == "image_based":
            image_based_series.append(item)
        elif series_cat == "subject_wise" or t.mode in ("subject_test", "subject"):
            subject_tests.append(item)
        elif series_cat == "quick_drills" or t.mode in ("quick_drill", "rapid_recall"):
            quick_drills.append(item)
        else:
            quick_drills.append(item)

        # Retain backward-compatible live_grand_tests bucket
        if item["is_live"] or series_cat == "neet_pg_pro" or t.mode in ("weekly_grand_test", "live_grand_test", "grand_test"):
            live_tests.append(item)

    # If no subject templates exist yet in DB, dynamically generate them from subjects table
    if not subject_tests:
        for s in all_subjects:
            subject_tests.append({
                "id": f"swt-{s.id}",
                "title": f"{s.name} Subject Test",
                "mode": "subject_test",
                "series_category": "subject_wise",
                "test_type": "SUBJECT MASTERY",
                "badge": f"{s.code} CORE",
                "subject_id": s.id,
                "subject_name": s.name,
                "subject_code": s.code,
                "question_count": 20,
                "time_limit_minutes": 25,
                "is_live": False,
                "syllabus_tag": f"All High-Yield {s.name} Topics",
                "total_registered": 950,
                "difficulty": "all"
            })

    return {
        "neet_pg_pro_series": neet_pg_pro_series,
        "medicine_prep_series": medicine_prep_series,
        "inicet_series": inicet_series,
        "fmge_next_series": fmge_next_series,
        "image_based_series": image_based_series,
        "live_grand_tests": live_tests,
        "subject_wise_tests": subject_tests,
        "quick_drills": quick_drills
    }

@router.get("/history")
async def get_test_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns student's historical test sessions with scores, accuracy, and status.
    """
    stmt = select(TestSession).where(
        TestSession.user_id == current_user.id
    ).order_by(TestSession.started_at.desc()).limit(50)
    res = await db.execute(stmt)
    sessions = res.scalars().all()

    history = []
    for s in sessions:
        max_score = (s.total_questions or 10) * 4
        accuracy = round((s.score / max_score) * 100.0, 1) if max_score > 0 and s.score > 0 else 0.0
        
        display_title = (s.mode or "Practice Test").replace("_", " ").title()
        if s.template and s.template.title:
            display_title = s.template.title

        history.append({
            "session_id": s.id,
            "mode": s.mode,
            "title": display_title,
            "status": s.status,
            "total_questions": s.total_questions,
            "completed_questions": s.completed_questions,
            "score": s.score,
            "max_score": max_score,
            "accuracy_percentage": accuracy,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "submitted_at": s.submitted_at.isoformat() if s.submitted_at else None,
        })

    return history

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

    effective_mode = req.mode
    effective_count = req.get_effective_count()
    effective_duration = req.duration_minutes
    effective_subject_id = req.subject_id
    effective_subject_ids = req.subject_ids
    effective_difficulty = req.difficulty

    # If launching from a test template, populate missing or default configuration from template
    if req.template_id:
        tmpl = await db.get(TestTemplate, req.template_id)
        if tmpl:
            cfg = tmpl.config or {}
            if (not effective_mode or effective_mode == "quick_test") and tmpl.mode:
                effective_mode = tmpl.mode
            if (req.total_questions is None and req.question_count == 10) and cfg.get("question_count"):
                effective_count = cfg.get("question_count")
            if not effective_duration and cfg.get("time_limit_minutes"):
                effective_duration = cfg.get("time_limit_minutes")
            if not effective_subject_ids and cfg.get("subject_ids"):
                effective_subject_ids = cfg.get("subject_ids")
            if not effective_subject_id and cfg.get("subject_id"):
                effective_subject_id = cfg.get("subject_id")
            if (not effective_difficulty or effective_difficulty == "all") and cfg.get("difficulty"):
                effective_difficulty = cfg.get("difficulty")

    test_session, loaded_questions = await TestService.create_test_session(
        db=db,
        user_id=current_user.id,
        mode=effective_mode,
        subject_id=effective_subject_id,
        chapter_id=req.chapter_id,
        topic_id=req.topic_id,
        subject_ids=effective_subject_ids,
        difficulty=effective_difficulty,
        unattempted_only=req.unattempted_only,
        is_high_yield_only=req.is_high_yield_only,
        template_id=req.template_id,
        duration_minutes=effective_duration,
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
    Logs medical accuracy or quality reports from students into the QuestionReport registry.
    """
    from app.models.question import Question
    stmt = select(Question).where(Question.id == req.question_id)
    res = await db.execute(stmt)
    q = res.scalars().first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    report = QuestionReport(
        question_id=req.question_id,
        user_id=current_user.id,
        reason=req.reason,
        comment=req.comments,
        is_serious_medical_error=(req.reason in ("wrong_answer", "incorrect_explanation"))
    )
    db.add(report)

    if req.reason in ("wrong_answer", "incorrect_explanation"):
        # Auto-quarantine serious medical error reports for senior clinician review
        quarantine = QuestionQuarantineRegistry(
            question_id=req.question_id,
            quarantine_reason=f"Student report: {req.reason}",
            resolution_status="quarantined",
            audit_notes=req.comments
        )
        db.add(quarantine)

    await db.commit()

    return {
        "status": "REPORTED",
        "question_id": req.question_id,
        "reason": req.reason,
        "message": "Thank you. Your report has been submitted to medical content governance for doctor review."
    }
