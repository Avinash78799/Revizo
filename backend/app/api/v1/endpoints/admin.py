from fastapi import APIRouter, Depends, status
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_reviewer_user, get_current_admin_user
from app.models.user import User
from app.models.question import Question, QuestionReport
from app.schemas.question import QuestionDetailResponse
from app.services.admin_service import AdminService
from app.core.errors import NotFoundError

router = APIRouter()

class ReviewQuestionRequest(BaseModel):
    verdict: str = Field(..., description="'approved', 'needs_revision', 'rejected'")
    notes: Optional[str] = None
    is_high_yield: bool = False

class QuarantineRequest(BaseModel):
    reason: str
    audit_notes: Optional[str] = None

class ResolveReportRequest(BaseModel):
    action_taken: str = Field(..., description="'question_fixed', 'question_quarantined', 'dismissed_valid'")

@router.get("/review-queue", response_model=List[QuestionDetailResponse])
async def get_review_queue(
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Question).options(
        selectinload(Question.options),
        selectinload(Question.concept)
    ).where(
        Question.status.in_(["draft", "review_required", "ai_generated", "reported"])
    ).limit(50)
    result = await db.execute(stmt)
    return list(result.scalars().all())

@router.post("/questions/{question_id}/publish", status_code=status.HTTP_200_OK)
@router.post("/approve-question", status_code=status.HTTP_200_OK)
async def publish_question(
    question_id: Optional[str] = None,
    req: Optional[ReviewQuestionRequest] = None,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    q_id = question_id
    notes = req.notes if req else None
    high_yield = req.is_high_yield if req else False
    
    question = await AdminService.review_and_publish_question(
        db=db,
        reviewer_id=current_user.id,
        question_id=q_id,
        is_high_yield=high_yield,
        notes=notes
    )
    await db.commit()
    return {"status": "published", "question_id": question.id, "trust_class": question.trust_class}

@router.post("/questions/{question_id}/quarantine", status_code=status.HTTP_200_OK)
@router.post("/quarantine-question", status_code=status.HTTP_200_OK)
async def quarantine_question(
    req: QuarantineRequest,
    question_id: Optional[str] = None,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    q_id = question_id
    question = await AdminService.quarantine_question(
        db=db,
        actor_id=current_user.id,
        question_id=q_id,
        reason=req.reason,
        audit_notes=req.audit_notes
    )
    await db.commit()
    return {"status": "quarantined", "question_id": question.id, "reason": req.reason}

@router.post("/reports/{report_id}/resolve", status_code=status.HTTP_200_OK)
async def resolve_report(
    report_id: str,
    req: ResolveReportRequest,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    report = await AdminService.resolve_question_report(
        db=db,
        resolver_id=current_user.id,
        report_id=report_id,
        action_taken=req.action_taken
    )
    await db.commit()
    return {"status": "resolved", "report_id": report.id, "action_taken": req.action_taken}
