from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.models.question import Question
from app.core.errors import NotFoundError, ConflictError

class TaxonomyService:
    @staticmethod
    async def get_all_subjects(db: AsyncSession) -> List[Subject]:
        stmt = select(Subject).options(
            selectinload(Subject.chapters).selectinload(Chapter.topics).selectinload(Topic.concepts)
        ).order_by(Subject.order_index.asc())
        res = await db.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def get_subject_by_id(db: AsyncSession, subject_id: str) -> Subject:
        stmt = select(Subject).options(
            selectinload(Subject.chapters).selectinload(Chapter.topics).selectinload(Topic.concepts)
        ).where(Subject.id == subject_id)
        res = await db.execute(stmt)
        subject = res.scalars().first()
        if not subject:
            raise NotFoundError("Subject")
        return subject

    @staticmethod
    async def get_chapter_by_id(db: AsyncSession, chapter_id: str) -> Chapter:
        stmt = select(Chapter).options(
            selectinload(Chapter.topics).selectinload(Topic.concepts)
        ).where(Chapter.id == chapter_id)
        res = await db.execute(stmt)
        chapter = res.scalars().first()
        if not chapter:
            raise NotFoundError("Chapter")
        return chapter

    @staticmethod
    async def get_topic_by_id(db: AsyncSession, topic_id: str) -> Topic:
        stmt = select(Topic).options(
            selectinload(Topic.concepts)
        ).where(Topic.id == topic_id)
        res = await db.execute(stmt)
        topic = res.scalars().first()
        if not topic:
            raise NotFoundError("Topic")
        return topic

    @staticmethod
    async def get_concept_by_id(db: AsyncSession, concept_id: str) -> Concept:
        stmt = select(Concept).where(Concept.id == concept_id)
        res = await db.execute(stmt)
        concept = res.scalars().first()
        if not concept:
            raise NotFoundError("Concept")
        return concept

    @staticmethod
    async def delete_concept_safe(db: AsyncSession, concept_id: str) -> bool:
        # Check for published questions to prevent orphan records
        stmt_q = select(Question).where(
            and_(
                Question.concept_id == concept_id,
                Question.status != "retired"
            )
        )
        res_q = await db.execute(stmt_q)
        if res_q.scalars().first():
            raise ConflictError("Cannot delete concept: active questions are currently linked to this concept.")

        concept = await TaxonomyService.get_concept_by_id(db, concept_id)
        await db.delete(concept)
        await db.flush()
        return True
