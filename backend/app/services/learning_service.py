from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.learning import StudentConceptMastery, StudentQuestionHistory, RevisionSchedule
from app.models.question import Question
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.services.question_eligibility_service import QuestionEligibilityService

def utc_now():
    return datetime.now(timezone.utc)

class LearningService:
    """
    Core learning intelligence service:
    1. Spaced Repetition (modified SM-2 with confidence weighting)
    2. Concept Mastery calculation
    3. Due revision retrieval and completion
    4. Five-minute focused revision session generation
    """

    MASTERY_ALGORITHM_VERSION = "v1.0"

    @classmethod
    def compute_spaced_interval(
        cls,
        consecutive_correct: int,
        ease_factor: float,
        confidence: str,
        is_correct: bool
    ) -> Dict[str, Any]:
        conf_normalized = confidence.upper()

        if not is_correct:
            # Mistake penalty: reset consecutive streak, lower ease
            ease_penalty = 0.25 if conf_normalized == "DEFINITELY_KNOW" else 0.15
            new_ease = max(1.30, ease_factor - ease_penalty)
            return {
                "interval_days": 1,
                "consecutive_correct": 0,
                "ease_factor": round(new_ease, 2),
                "next_due": utc_now() + timedelta(days=1)
            }

        # Confidence modifier for correct answers
        multiplier = 1.30 if conf_normalized == "DEFINITELY_KNOW" else (1.00 if conf_normalized == "SOMEWHAT_CONFIDENT" else 0.80)
        
        if consecutive_correct == 0:
            interval = 1
        elif consecutive_correct == 1:
            interval = 3
        elif consecutive_correct == 2:
            interval = 7
        else:
            interval = int(round(consecutive_correct * ease_factor * multiplier))
            interval = max(interval, consecutive_correct * 2)

        ease_bonus = 0.10 if conf_normalized == "DEFINITELY_KNOW" else 0.0
        new_ease = min(3.00, ease_factor + ease_bonus)

        return {
            "interval_days": interval,
            "consecutive_correct": consecutive_correct + 1,
            "ease_factor": round(new_ease, 2),
            "next_due": utc_now() + timedelta(days=interval)
        }

    @classmethod
    async def update_concept_mastery(
        cls,
        db: AsyncSession,
        user_id: str,
        concept_id: str,
        is_correct: bool,
        confidence: str
    ) -> StudentConceptMastery:
        stmt = select(StudentConceptMastery).where(
            StudentConceptMastery.user_id == user_id,
            StudentConceptMastery.concept_id == concept_id
        )
        res = await db.execute(stmt)
        record = res.scalars().first()

        conf_normalized = confidence.upper()
        is_danger_zone = (not is_correct) and (conf_normalized == "DEFINITELY_KNOW")

        if not record:
            spaced = cls.compute_spaced_interval(
                consecutive_correct=0,
                ease_factor=2.50,
                confidence=conf_normalized,
                is_correct=is_correct
            )
            record = StudentConceptMastery(
                user_id=user_id,
                concept_id=concept_id,
                total_attempts=1,
                correct_attempts=1 if is_correct else 0,
                high_confidence_wrong_count=1 if is_danger_zone else 0,
                mastery_percentage=100.0 if is_correct else 0.0,
                last_practiced_at=utc_now(),
                next_revision_due=spaced["next_due"],
                revision_interval_days=spaced["interval_days"],
                ease_factor=spaced["ease_factor"],
                consecutive_correct_count=spaced["consecutive_correct"]
            )
            db.add(record)
        else:
            record.total_attempts += 1
            if is_correct:
                record.correct_attempts += 1
            if is_danger_zone:
                record.high_confidence_wrong_count += 1

            # Mastery percentage formula with danger zone penalty
            raw_acc = (record.correct_attempts / record.total_attempts) * 100.0
            danger_penalty = min(30.0, record.high_confidence_wrong_count * 10.0)
            record.mastery_percentage = round(max(0.0, raw_acc - danger_penalty), 1)
            record.last_practiced_at = utc_now()

            spaced = cls.compute_spaced_interval(
                consecutive_correct=record.consecutive_correct_count,
                ease_factor=record.ease_factor,
                confidence=conf_normalized,
                is_correct=is_correct
            )
            record.next_revision_due = spaced["next_due"]
            record.revision_interval_days = spaced["interval_days"]
            record.ease_factor = spaced["ease_factor"]
            record.consecutive_correct_count = spaced["consecutive_correct"]

        # Also create revision schedule item
        sched = RevisionSchedule(
            user_id=user_id,
            concept_id=concept_id,
            scheduled_date=record.next_revision_due,
            is_completed=False
        )
        db.add(sched)
        await db.flush()
        return record

    @classmethod
    async def get_due_revisions(
        cls,
        db: AsyncSession,
        user_id: str,
        limit: int = 10
    ) -> List[StudentConceptMastery]:
        now = utc_now()
        stmt = select(StudentConceptMastery).options(
            selectinload(StudentConceptMastery.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        ).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.next_revision_due <= now
            )
        ).order_by(StudentConceptMastery.next_revision_due.asc()).limit(limit)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def complete_revision_item(
        cls,
        db: AsyncSession,
        user_id: str,
        concept_id: str
    ) -> bool:
        stmt = select(RevisionSchedule).where(
            and_(
                RevisionSchedule.user_id == user_id,
                RevisionSchedule.concept_id == concept_id,
                RevisionSchedule.is_completed == False
            )
        )
        res = await db.execute(stmt)
        item = res.scalars().first()
        if item:
            item.is_completed = True
            item.completed_at = utc_now()
            await db.flush()
            return True
        return False

    @classmethod
    async def select_five_minute_revision_questions(
        cls,
        db: AsyncSession,
        user_id: str,
        count: int = 5,
        allow_dev_seeds: bool = True
    ) -> List[Question]:
        """
        Selects a tightly bounded revision set (5 questions) prioritizing:
        1. Due revision concepts
        2. Danger zone concepts
        3. Weak mastery concepts (< 70%)
        """
        now = utc_now()
        
        # 1. Fetch priority concept IDs for student
        priority_concepts_stmt = select(StudentConceptMastery.concept_id).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                or_(
                    StudentConceptMastery.next_revision_due <= now,
                    StudentConceptMastery.high_confidence_wrong_count > 0,
                    StudentConceptMastery.mastery_percentage < 70.0
                )
            )
        ).limit(count * 2)
        priority_res = await db.execute(priority_concepts_stmt)
        concept_ids = list(priority_res.scalars().all())

        # 2. Query questions for these concepts
        base_query = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        )
        eligible_query = QuestionEligibilityService.apply_eligibility_filter(base_query, allow_dev_seeds=allow_dev_seeds)

        if concept_ids:
            targeted_query = eligible_query.where(Question.concept_id.in_(concept_ids)).limit(count)
            t_res = await db.execute(targeted_query)
            questions = list(t_res.scalars().all())
            if len(questions) >= count:
                return questions

        # Fallback to general eligible questions
        fallback_query = eligible_query.limit(count)
        f_res = await db.execute(fallback_query)
        return list(f_res.scalars().all())
