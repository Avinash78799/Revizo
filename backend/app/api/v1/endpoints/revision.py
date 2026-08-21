from fastapi import APIRouter, Depends, status
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.student import DueConceptItem
from app.schemas.test import TestSessionResponse
from app.services.learning_service import LearningService
from app.services.test_service import TestService
from app.engines.test_engine import TestEngine

router = APIRouter()

class CompleteRevisionRequest(BaseModel):
    concept_id: str

@router.get("/due", response_model=List[DueConceptItem])
async def get_due_revisions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns student concepts currently due for spaced repetition review.
    """
    records = await LearningService.get_due_revisions(db, current_user.id)
    items: list[DueConceptItem] = []
    for r in records:
        if r.concept:
            topic_name = r.concept.topic.name if r.concept.topic else "Topic"
            subject_name = r.concept.topic.chapter.subject.name if (r.concept.topic and r.concept.topic.chapter and r.concept.topic.chapter.subject) else "Subject"
            items.append(DueConceptItem(
                concept_id=r.concept_id,
                concept_name=r.concept.name,
                topic_name=topic_name,
                subject_name=subject_name,
                revision_interval_days=r.revision_interval_days,
                next_revision_due=r.next_revision_due
            ))
    return items

@router.post("/complete", status_code=status.HTTP_200_OK)
async def complete_revision(
    req: CompleteRevisionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    success = await LearningService.complete_revision_item(db, current_user.id, req.concept_id)
    await db.commit()
    return {"status": "completed" if success else "no_pending_schedule", "concept_id": req.concept_id}

@router.post("/five-minute-session", response_model=TestSessionResponse, status_code=status.HTTP_201_CREATED)
async def start_five_minute_revision_session(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Starts a quick 5-minute revision session selecting 5 questions from
    due concepts, weak areas, and mistake history.
    """
    test_session, questions = await TestService.create_test_session(
        db=db,
        user_id=current_user.id,
        mode="five_minute_revision",
        question_count=10
    )
    await db.commit()

    sanitized = [TestEngine.sanitize_question(q) for q in questions]
    return TestSessionResponse(
        session_id=test_session.id,
        user_id=test_session.user_id,
        mode=test_session.mode,
        total_questions=test_session.total_questions,
        completed_questions=test_session.completed_questions,
        score=test_session.score,
        started_at=test_session.started_at,
        questions=sanitized
    )
