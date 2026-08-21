from typing import Dict, Any, List
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test import TestAttempt, TestSession
from app.models.learning import StudentConceptMastery, LearningEvidenceRecord
from app.models.taxonomy import Concept, Subject, Chapter, Topic
from app.core.datetime_util import utc_now, ensure_utc

class AnalyticsService:
    """
    Milestone 10 Performance Analytics Engine (Prompt 14, Sec 6).
    Actionable student-facing analytics to guide 'WHAT TO STUDY NEXT'.
    """

    @classmethod
    async def get_student_performance_summary(cls, db: AsyncSession, user_id: str) -> Dict[str, Any]:
        # 1. Total Attempts & Accuracy
        stmt_att = select(TestAttempt).where(TestAttempt.user_id == user_id)
        res_att = await db.execute(stmt_att)
        attempts = res_att.scalars().all()

        total_attempts = len(attempts)
        correct_count = sum(1 for a in attempts if a.is_correct)
        incorrect_count = total_attempts - correct_count
        accuracy = round((correct_count / total_attempts * 100), 1) if total_attempts > 0 else 0.0
        negative_marks_lost = incorrect_count * 1.0  # -1 mark per wrong MCQ

        # 2. Confidence vs Correctness Calibration
        def_know_attempts = [a for a in attempts if a.confidence and a.confidence.upper() == "DEFINITELY_KNOW"]
        guessing_attempts = [a for a in attempts if a.confidence and a.confidence.upper() == "GUESSING"]

        def_know_accuracy = round(sum(1 for a in def_know_attempts if a.is_correct) / len(def_know_attempts) * 100, 1) if def_know_attempts else 0.0
        guessing_accuracy = round(sum(1 for a in guessing_attempts if a.is_correct) / len(guessing_attempts) * 100, 1) if guessing_attempts else 0.0

        # 3. Weak & Strong Concepts
        stmt_m = (
            select(StudentConceptMastery)
            .options(selectinload(StudentConceptMastery.concept))
            .where(StudentConceptMastery.user_id == user_id)
        )
        res_m = await db.execute(stmt_m)
        mastery_records = res_m.scalars().all()

        weak_concepts = [
            {
                "concept_id": m.concept_id,
                "concept_name": m.concept.name if m.concept else "Medical Concept",
                "mastery_percentage": m.mastery_percentage,
                "misconception_state": m.misconception_state,
                "danger_zone_active": m.danger_zone_active
            }
            for m in mastery_records if m.mastery_percentage < 60.0 or m.danger_zone_active
        ]

        strong_concepts = [
            {
                "concept_id": m.concept_id,
                "concept_name": m.concept.name if m.concept else "Medical Concept",
                "mastery_percentage": m.mastery_percentage
            }
            for m in mastery_records if m.mastery_percentage >= 80.0 and not m.danger_zone_active
        ]

        # 4. Revision Items Due
        now = utc_now()
        revision_due_count = sum(1 for m in mastery_records if m.next_revision_due and ensure_utc(m.next_revision_due) <= now)

        return {
            "user_id": user_id,
            "total_attempts": total_attempts,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "accuracy_percentage": accuracy,
            "negative_marks_lost": negative_marks_lost,
            "confidence_calibration": {
                "high_confidence_accuracy": def_know_accuracy,
                "guessing_accuracy": guessing_accuracy,
                "high_confidence_errors_count": sum(1 for a in def_know_attempts if not a.is_correct)
            },
            "weak_concepts_count": len(weak_concepts),
            "weak_concepts": weak_concepts[:5],
            "strong_concepts_count": len(strong_concepts),
            "revision_items_due": revision_due_count,
            "recommended_next_action": "REVISE_DANGER_ZONE" if any(w["danger_zone_active"] for w in weak_concepts) else "DAILY_SHORT_TEST"
        }
