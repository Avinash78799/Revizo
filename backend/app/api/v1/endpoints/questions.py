from fastapi import APIRouter, Depends, status, Request
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.question import Question, QuestionReport, QuestionQuarantineRegistry
from app.models.audit import AuditLog
from app.schemas.question import SanitizedQuestionResponse
from app.services.question_eligibility_service import QuestionEligibilityService
from app.engines.test_engine import TestEngine
from app.services.rate_limiter import rate_limiter
from app.core.errors import NotFoundError

router = APIRouter()

class ReportQuestionRequest(BaseModel):
    reason: str = Field(..., description="'INCORRECT', 'AMBIGUOUS', 'TYPO', 'OUTDATED', 'OUT_OF_SYLLABUS', 'POOR_EXPLANATION', 'OTHER'")
    description: Optional[str] = None
    is_serious_medical_error: bool = False

@router.get("/available", response_model=List[SanitizedQuestionResponse])
async def list_available_questions(
    subject_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns available student-safe practice questions.
    Never exposes internal answers, reviews, quality scores, or AI metadata.
    """
    base_query = select(Question).options(
        selectinload(Question.options),
        selectinload(Question.concept)
    )
    eligible_query = QuestionEligibilityService.apply_eligibility_filter(base_query, allow_dev_seeds=True)
    res = await db.execute(eligible_query.limit(20))
    questions = res.scalars().all()
    return [TestEngine.sanitize_question(q) for q in questions]

@router.post("/{question_id}/report", status_code=status.HTTP_201_CREATED)
async def report_question(
    question_id: str,
    req: ReportQuestionRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rate_limiter.check_rate_limit(f"report:{current_user.id}", max_requests=10, window_seconds=60)

    stmt = select(Question).where(Question.id == question_id)
    res = await db.execute(stmt)
    question = res.scalars().first()

    if not question:
        raise NotFoundError("Question")

    report = QuestionReport(
        question_id=question.id,
        user_id=current_user.id,
        reason=req.reason.upper(),
        comment=req.description,
        is_serious_medical_error=req.is_serious_medical_error
    )
    db.add(report)

    if req.is_serious_medical_error:
        question.status = "quarantined"
        quarantine = QuestionQuarantineRegistry(
            question_id=question.id,
            quarantine_reason=f"Auto-quarantined: Serious student report ({req.reason.upper()})",
            resolution_status="quarantined",
            audit_notes=req.description
        )
        db.add(quarantine)

        audit = AuditLog(
            actor_id=current_user.id,
            action="serious_report_auto_quarantine",
            target_entity="question",
            target_id=question.id,
            details={"reason": req.reason, "description": req.description}
        )
        db.add(audit)

    await db.commit()
    return {
        "status": "reported",
        "question_id": question.id,
        "is_quarantined": req.is_serious_medical_error
    }
