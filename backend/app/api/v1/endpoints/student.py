from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.test import TestAttempt
from app.models.learning import StudentConceptMastery, StudentMistakeRecord
from app.models.question import Question
from app.models.taxonomy import Concept
from app.schemas.student import DashboardResponse, DangerZoneItem
from app.engines.analytics_engine import AnalyticsEngine
from app.services.learning_intelligence_engine import LearningIntelligenceEngine
from app.core.errors import NotFoundError

router = APIRouter()

class MistakeItemResponse(BaseModel):
    attempt_id: str
    question_id: str
    question_text: str
    concept_id: str
    concept_name: str
    selected_option_key: Optional[str] = None
    correct_explanation: str
    remember_takeaway: str
    confidence: str
    is_danger_zone: bool
    answered_at: datetime

class ConceptMasterySummary(BaseModel):
    concept_id: str
    concept_name: str
    topic_name: str
    subject_name: str
    total_attempts: int
    correct_attempts: int
    mastery_percentage: float
    smoothed_mastery_score: float
    mastery_state: str
    danger_zone_active: bool
    is_cold_start: bool
    high_confidence_wrong_count: int
    revision_interval_days: int
    next_revision_due: datetime

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns student diagnostic dashboard metrics.
    """
    return await AnalyticsEngine.get_dashboard_analytics(db, current_user.id)

@router.get("/learning-plan")
async def get_daily_learning_plan(
    target_questions: int = Query(default=20, ge=5, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns personalized, prioritized daily study plan (Prompt 8, Sec 12).
    """
    return await LearningIntelligenceEngine.generate_daily_study_plan(
        db=db,
        user_id=current_user.id,
        target_questions=target_questions
    )

@router.get("/next-action")
async def get_next_best_action(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns the single highest-impact clinical study action (Prompt 8, Sec 13).
    """
    return await LearningIntelligenceEngine.get_next_best_action(db, current_user.id)

@router.get("/five-minute-revision")
async def get_five_minute_revision_slice(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns 5 targeted questions combining Danger Zone misconceptions + due spaced revisions (Prompt 8, Sec 11).
    """
    return await LearningIntelligenceEngine.get_five_minute_revision_slice(db, current_user.id)

@router.get("/confidence")
async def get_confidence_calibration(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns confidence calibration metrics (expressed confidence vs accuracy) (Prompt 8, Sec 17).
    """
    return await LearningIntelligenceEngine.get_confidence_calibration(db, current_user.id)

@router.get("/danger-zone")
async def get_danger_zone(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns active Danger Zone misconceptions (WRONG + DEFINITELY_KNOW >= 2) (Prompt 8, Sec 2 & 16).
    """
    return await LearningIntelligenceEngine.get_danger_zone_concepts(db, current_user.id)

@router.get("/mistakes")
async def get_mistakes(
    danger_zone_only: bool = Query(default=False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns categorized student mistake records with error taxonomy (Prompt 8, Sec 18).
    """
    stmt = select(StudentMistakeRecord).options(
        selectinload(StudentMistakeRecord.concept),
        selectinload(StudentMistakeRecord.question)
    ).where(StudentMistakeRecord.user_id == current_user.id)

    if danger_zone_only:
        stmt = stmt.where(StudentMistakeRecord.confidence_level == "DEFINITELY_KNOW")

    stmt = stmt.order_by(StudentMistakeRecord.last_occurred_at.desc())
    res = await db.execute(stmt)
    mistakes = res.scalars().all()

    # Load attempts for response time trap signal
    results = []
    for m in mistakes:
        stmt_att = select(TestAttempt).where(
            and_(TestAttempt.user_id == current_user.id, TestAttempt.question_id == m.question_id)
        ).order_by(TestAttempt.created_at.desc()).limit(1)
        res_att = await db.execute(stmt_att)
        latest_att = res_att.scalars().first()
        time_spent = latest_att.time_spent_seconds if latest_att else 20

        # Time-trap classification: Knowledge Gap (<15s) vs Overthinking Trap (>45s) vs Misconception
        if time_spent <= 15:
            trap_tag = "Knowledge Gap (Quick Guess)"
            trap_type = "quick_gap"
        elif time_spent >= 45:
            trap_tag = "Overthinking Trap (>45s)"
            trap_type = "overthinking"
        else:
            trap_tag = "Misconception / Reasoning"
            trap_type = "reasoning"

        results.append({
            "id": m.id,
            "attempt_id": latest_att.id if latest_att else m.id,
            "question_id": m.question_id,
            "concept_id": m.concept_id,
            "concept_name": m.concept.name if m.concept else "Concept",
            "question_text": m.question.question_text if m.question else "Question Text",
            "correct_explanation": m.question.correct_explanation if m.question else "",
            "remember_takeaway": m.question.remember_takeaway if m.question else "",
            "selected_option_key": m.selected_option_key,
            "correct_option_key": m.correct_option_key,
            "confidence": m.confidence_level,
            "confidence_level": m.confidence_level,
            "is_danger_zone": m.confidence_level == "DEFINITELY_KNOW",
            "error_type": m.error_type,
            "status": m.status,
            "occurrence_count": m.occurrence_count,
            "time_spent_seconds": time_spent,
            "time_trap_tag": trap_tag,
            "time_trap_type": trap_type,
            "answered_at": m.last_occurred_at.isoformat(),
            "last_occurred_at": m.last_occurred_at.isoformat()
        })

    return results


@router.get("/mastery", response_model=List[ConceptMasterySummary])
async def get_mastery(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns concept-level mastery records with interpretable states and statistical indicators.
    """
    stmt = select(StudentConceptMastery).options(
        selectinload(StudentConceptMastery.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
    ).where(
        StudentConceptMastery.user_id == current_user.id
    ).order_by(StudentConceptMastery.smoothed_mastery_score.asc())
    result = await db.execute(stmt)
    records = result.scalars().all()

    summaries: list[ConceptMasterySummary] = []
    for r in records:
        if r.concept:
            topic_name = r.concept.topic.name if r.concept.topic else "Topic"
            subject_name = r.concept.topic.chapter.subject.name if (r.concept.topic and r.concept.topic.chapter and r.concept.topic.chapter.subject) else "Subject"
            summaries.append(ConceptMasterySummary(
                concept_id=r.concept_id,
                concept_name=r.concept.name,
                topic_name=topic_name,
                subject_name=subject_name,
                total_attempts=r.total_attempts,
                correct_attempts=r.correct_attempts,
                mastery_percentage=r.mastery_percentage,
                smoothed_mastery_score=r.smoothed_mastery_score,
                mastery_state=r.mastery_state,
                danger_zone_active=r.danger_zone_active,
                is_cold_start=r.is_cold_start,
                high_confidence_wrong_count=r.high_confidence_wrong_count,
                revision_interval_days=r.revision_interval_days,
                next_revision_due=r.next_revision_due
            ))
    return summaries

@router.post("/concepts/{concept_id}/retest")
async def create_misconception_retest(
    concept_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generates a targeted retest question for a specific misconception concept (Prompt 8, Sec 16).
    """
    stmt_q = select(Question).options(selectinload(Question.options)).where(
        and_(
            Question.concept_id == concept_id,
            Question.status == "PUBLISHED"
        )
    ).limit(1)
    res_q = await db.execute(stmt_q)
    q = res_q.scalars().first()

    if not q:
        raise NotFoundError("Retest Question for this Concept")

    return {
        "concept_id": concept_id,
        "question_id": q.id,
        "question_text": q.question_text,
        "difficulty": q.difficulty,
        "options": [{"option_key": o.option_key, "option_text": o.option_text} for o in q.options]
    }
