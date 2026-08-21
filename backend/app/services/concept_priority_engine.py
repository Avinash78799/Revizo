from typing import Dict, Any, List, Optional
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.question import Question
from app.models.source import PyqReference
from app.models.learning import StudentConceptMastery

class ConceptPriorityEngine:
    """
    Concept Priority & High-Yield Ranking Engine (Prompt 7, Sec 8, 9, 31).
    Produces transparent, multi-component priority scores to direct question generation.
    Never claims to 'predict the next exam'; provides objective curriculum and diagnostic priority.
    """

    WEIGHTS = {
        "curriculum_importance": 0.30,
        "pyq_recurrence": 0.25,
        "student_misconceptions": 0.25,
        "content_coverage_gap": 0.20,
    }

    @classmethod
    async def calculate_concept_priority(
        cls,
        db: AsyncSession,
        concept_id: str
    ) -> Dict[str, Any]:
        stmt_c = select(Concept).options(
            selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject),
            selectinload(Concept.questions),
            selectinload(Concept.mastery_records)
        ).where(Concept.id == concept_id)
        res_c = await db.execute(stmt_c)
        concept = res_c.scalars().first()

        if not concept:
            return {"error": "Concept not found"}

        # 1. Curriculum Importance (0.0 to 1.0)
        curriculum_score = float(concept.exam_relevance_score)

        # 2. PYQ Recurrence & Frequency
        stmt_pyq = select(func.count(PyqReference.id)).where(PyqReference.concept_id == concept_id)
        pyq_count = (await db.execute(stmt_pyq)).scalar() or 0
        pyq_score = min(1.0, pyq_count * 0.35)

        # 3. Student Misconceptions (Aggregate high-confidence error frequency)
        total_attempts = sum(m.total_attempts for m in concept.mastery_records)
        high_conf_wrong = sum(m.high_confidence_wrong_count for m in concept.mastery_records)
        
        if total_attempts > 0:
            misconception_rate = float(high_conf_wrong) / float(total_attempts)
            misconception_score = min(1.0, misconception_rate * 2.0)
        else:
            misconception_score = 0.50  # Baseline neutral prior

        # 4. Content Coverage Gap (Inverse of verified questions)
        verified_count = sum(1 for q in concept.questions if q.status == "PUBLISHED" and q.trust_class == "VERIFIED_CORE_QUESTION")
        if verified_count == 0:
            gap_score = 1.0
        elif verified_count <= 2:
            gap_score = 0.60
        else:
            gap_score = 0.15

        # Weighted Aggregate Priority Score
        total_priority = (
            curriculum_score * cls.WEIGHTS["curriculum_importance"] +
            pyq_score * cls.WEIGHTS["pyq_recurrence"] +
            misconception_score * cls.WEIGHTS["student_misconceptions"] +
            gap_score * cls.WEIGHTS["content_coverage_gap"]
        )

        reasons = []
        if pyq_count > 0:
            reasons.append(f"Linked to {pyq_count} historical verified exam appearance(s).")
        if high_conf_wrong > 0:
            reasons.append(f"Triggered {high_conf_wrong} Danger Zone student misconception(s).")
        if verified_count < 2:
            reasons.append(f"Current verified pool has only {verified_count} question(s) (coverage gap).")
        if curriculum_score >= 0.85:
            reasons.append("Marked high-yield core curriculum concept.")

        return {
            "concept_id": concept.id,
            "concept_name": concept.name,
            "topic_name": concept.topic.name if concept.topic else "Topic",
            "subject_name": concept.topic.chapter.subject.name if (concept.topic and concept.topic.chapter and concept.topic.chapter.subject) else "Subject",
            "overall_priority_score": round(total_priority, 3),
            "priority_level": "CRITICAL" if total_priority >= 0.75 else "HIGH" if total_priority >= 0.55 else "MODERATE",
            "breakdown": {
                "curriculum_importance": round(curriculum_score, 2),
                "pyq_recurrence": round(pyq_score, 2),
                "student_misconceptions": round(misconception_score, 2),
                "content_coverage_gap": round(gap_score, 2)
            },
            "why_priority": reasons
        }
