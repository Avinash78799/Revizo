from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.learning import StudentConceptMastery, StudentQuestionHistory

def utc_now():
    return datetime.now(timezone.utc)

class LearningEngine:
    @staticmethod
    def calculate_spaced_interval(
        consecutive_correct: int,
        ease_factor: float,
        confidence: str,
        is_correct: bool
    ) -> dict:
        """
        Adaptive concept-level spaced repetition algorithm (modified SM-2 / FSRS).
        Adapts interval based on correctness AND student confidence.
        """
        if not is_correct:
            # Mistake resets the consecutive streak and lowers ease factor slightly
            return {
                "interval_days": 1,
                "consecutive_correct": 0,
                "ease_factor": max(1.3, ease_factor - 0.20),
                "next_due": utc_now() + timedelta(days=1)
            }
        
        # Confidence multiplier
        conf_multiplier = 1.25 if confidence == "definitely_know" else (1.0 if confidence == "somewhat_confident" else 0.8)
        
        if consecutive_correct == 0:
            interval = 1
        elif consecutive_correct == 1:
            interval = 3
        elif consecutive_correct == 2:
            interval = 7
        else:
            interval = int(interval * ease_factor * conf_multiplier)
            interval = max(interval, consecutive_correct * 3)
            
        new_ease = min(3.0, ease_factor + (0.1 if confidence == "definitely_know" else 0.0))
        next_due = utc_now() + timedelta(days=interval)
        
        return {
            "interval_days": interval,
            "consecutive_correct": consecutive_correct + 1,
            "ease_factor": new_ease,
            "next_due": next_due
        }

    @staticmethod
    async def update_student_concept_mastery(
        session: AsyncSession,
        user_id: str,
        concept_id: str,
        is_correct: bool,
        confidence: str
    ) -> StudentConceptMastery:
        """
        Updates concept-level mastery records and flags high-confidence misconceptions (Danger Zone).
        """
        stmt = select(StudentConceptMastery).where(
            StudentConceptMastery.user_id == user_id,
            StudentConceptMastery.concept_id == concept_id
        )
        result = await session.execute(stmt)
        record = result.scalars().first()

        is_danger_zone = (not is_correct) and (confidence == "definitely_know")

        if not record:
            spaced = LearningEngine.calculate_spaced_interval(
                consecutive_correct=0,
                ease_factor=2.50,
                confidence=confidence,
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
            session.add(record)
        else:
            record.total_attempts += 1
            if is_correct:
                record.correct_attempts += 1
            if is_danger_zone:
                record.high_confidence_wrong_count += 1

            record.mastery_percentage = round((record.correct_attempts / record.total_attempts) * 100.0, 1)
            record.last_practiced_at = utc_now()

            spaced = LearningEngine.calculate_spaced_interval(
                consecutive_correct=record.consecutive_correct_count,
                ease_factor=record.ease_factor,
                confidence=confidence,
                is_correct=is_correct
            )
            record.next_revision_due = spaced["next_due"]
            record.revision_interval_days = spaced["interval_days"]
            record.ease_factor = spaced["ease_factor"]
            record.consecutive_correct_count = spaced["consecutive_correct"]

        # Also track question-level encounter history
        await session.flush()
        return record

    @staticmethod
    async def record_question_history(
        session: AsyncSession,
        user_id: str,
        question_id: str,
        is_correct: bool
    ) -> StudentQuestionHistory:
        stmt = select(StudentQuestionHistory).where(
            StudentQuestionHistory.user_id == user_id,
            StudentQuestionHistory.question_id == question_id
        )
        result = await session.execute(stmt)
        history = result.scalars().first()

        if not history:
            history = StudentQuestionHistory(
                user_id=user_id,
                question_id=question_id,
                total_encounters=1,
                correct_encounters=1 if is_correct else 0,
                last_encountered_at=utc_now()
            )
            session.add(history)
        else:
            history.total_encounters += 1
            if is_correct:
                history.correct_encounters += 1
            history.last_encountered_at = utc_now()

        await session.flush()
        return history
