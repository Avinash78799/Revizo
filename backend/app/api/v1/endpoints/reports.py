from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.question import Question, QuestionReport, QuestionQuarantineRegistry
from app.models.audit import AuditLog

router = APIRouter()

class CreateReportRequest(BaseModel):
    question_id: str
    reason: str = Field(..., description="'incorrect_answer', 'ambiguous', 'outdated', 'typo', 'poor_explanation', 'other'")
    comment: Optional[str] = None
    is_serious_medical_error: bool = False

@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def report_question(
    req: CreateReportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Submits a student report on a question.
    If flagged as a serious medical error, automatically quarantines the question.
    """
    stmt = select(Question).where(Question.id == req.question_id)
    result = await db.execute(stmt)
    question = result.scalars().first()

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")

    report = QuestionReport(
        question_id=question.id,
        user_id=current_user.id,
        reason=req.reason,
        comment=req.comment,
        is_serious_medical_error=req.is_serious_medical_error
    )
    db.add(report)

    # Automatic safety trigger: serious medical reports isolate question immediately
    if req.is_serious_medical_error:
        question.status = "quarantined"
        quarantine = QuestionQuarantineRegistry(
            question_id=question.id,
            quarantine_reason=f"Auto-quarantined: Serious medical error report ({req.reason})",
            resolution_status="quarantined",
            audit_notes=req.comment
        )
        db.add(quarantine)

        audit = AuditLog(
            actor_id=current_user.id,
            action="serious_report_auto_quarantine",
            target_entity="question",
            target_id=question.id,
            details={"reason": req.reason, "comment": req.comment}
        )
        db.add(audit)

    await db.commit()
    return {
        "status": "reported",
        "question_id": question.id,
        "is_quarantined": req.is_serious_medical_error
    }
