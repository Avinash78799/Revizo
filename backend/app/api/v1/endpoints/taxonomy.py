from fastapi import APIRouter, Depends, status
from typing import List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_admin_user
from app.models.user import User
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.schemas.taxonomy import (
    SubjectResponse,
    SubjectItemResponse,
    ChapterResponse,
    ChapterItemResponse,
    TopicResponse,
    TopicItemResponse,
    ConceptResponse
)
from app.services.taxonomy_service import TaxonomyService

router = APIRouter()

class CreateSubjectRequest(BaseModel):
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=20)
    description: Optional[str] = None
    order_index: int = 0

class CreateChapterRequest(BaseModel):
    subject_id: str
    name: str = Field(..., max_length=150)
    order_index: int = 0

class CreateTopicRequest(BaseModel):
    chapter_id: str
    name: str = Field(..., max_length=150)
    order_index: int = 0

class CreateConceptRequest(BaseModel):
    topic_id: str
    name: str = Field(..., max_length=200)
    high_yield_notes: Optional[str] = None
    clinical_pearl: Optional[str] = None
    exam_relevance_score: float = Field(default=0.80, ge=0.0, le=1.0)

@router.get("/subjects", response_model=List[SubjectResponse])
async def list_subjects(db: AsyncSession = Depends(get_db)):
    return await TaxonomyService.get_all_subjects(db)

@router.get("/tree", response_model=List[SubjectResponse])
async def get_full_taxonomy_tree(db: AsyncSession = Depends(get_db)):
    """Returns all subjects with their full chapter/topic/concept tree."""
    return await TaxonomyService.get_all_subjects(db)

@router.get("/subjects/{subject_id}/tree", response_model=SubjectResponse)
async def get_subject_tree(subject_id: str, db: AsyncSession = Depends(get_db)):
    return await TaxonomyService.get_subject_by_id(db, subject_id)

@router.get("/chapters", response_model=List[ChapterResponse])
async def list_chapters(subject_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Chapter)
    if subject_id:
        query = query.where(Chapter.subject_id == subject_id)
    query = query.order_by(Chapter.order_index.asc())
    result = await db.execute(query)
    return list(result.scalars().all())

@router.get("/topics", response_model=List[TopicResponse])
async def list_topics(chapter_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Topic)
    if chapter_id:
        query = query.where(Topic.chapter_id == chapter_id)
    query = query.order_by(Topic.order_index.asc())
    result = await db.execute(query)
    return list(result.scalars().all())

@router.get("/concepts", response_model=List[ConceptResponse])
async def list_concepts(topic_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Concept)
    if topic_id:
        query = query.where(Concept.topic_id == topic_id)
    result = await db.execute(query)
    return list(result.scalars().all())

# --- Admin Taxonomy Mutation Endpoints ---

@router.post("/subjects", response_model=SubjectItemResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    req: CreateSubjectRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    sub = Subject(
        name=req.name,
        code=req.code.upper(),
        description=req.description,
        order_index=req.order_index
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub

@router.post("/chapters", response_model=ChapterItemResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter(
    req: CreateChapterRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    chap = Chapter(
        subject_id=req.subject_id,
        name=req.name,
        order_index=req.order_index
    )
    db.add(chap)
    await db.commit()
    await db.refresh(chap)
    return chap

@router.post("/topics", response_model=TopicItemResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    req: CreateTopicRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    top = Topic(
        chapter_id=req.chapter_id,
        name=req.name,
        order_index=req.order_index
    )
    db.add(top)
    await db.commit()
    await db.refresh(top)
    return top

@router.post("/concepts", response_model=ConceptResponse, status_code=status.HTTP_201_CREATED)
async def create_concept(
    req: CreateConceptRequest,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    con = Concept(
        topic_id=req.topic_id,
        name=req.name,
        high_yield_notes=req.high_yield_notes,
        clinical_pearl=req.clinical_pearl,
        exam_relevance_score=req.exam_relevance_score
    )
    db.add(con)
    await db.commit()
    await db.refresh(con)
    return con

@router.delete("/concepts/{concept_id}", status_code=status.HTTP_200_OK)
async def delete_concept(
    concept_id: str,
    current_admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    await TaxonomyService.delete_concept_safe(db, concept_id)
    await db.commit()
    return {"status": "deleted", "concept_id": concept_id}
