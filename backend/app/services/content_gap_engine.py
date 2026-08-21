from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.taxonomy import Subject, Chapter, Topic, Concept, SyllabusRegistry
from app.models.question import Question
from app.models.source import Source, PyqReference, SourceConflict

class ContentGapEngine:
    """
    NEET-PG Syllabus Content Coverage Matrix, Priority Gap & Dataset Readiness Engine (Prompt 11, Sec 15-18).
    - Distinguishes RAW Draft Count from TRUSTED Question Count (Level 1-3 only)
    - Computes Explainable CONTENT_GAP_PRIORITY_SCORE
    - Enforces CONTENT_DATASET_STATUS Readiness Gates (BOOTSTRAP to PRODUCTION_READY)
    """

    TRUSTED_TRUST_CLASSES = {"VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "SOURCE_REFERENCED"}

    # Dataset Readiness Thresholds (Prompt 11, Sec 17 & 18)
    READINESS_THRESHOLDS = {
        "PILOT": {
            "min_trusted_questions": 50,
            "min_verified_pyqs": 10,
            "min_subjects_covered": 5,
            "min_concepts_covered": 20
        },
        "PUBLIC_TESTING": {
            "min_trusted_questions": 500,
            "min_verified_pyqs": 100,
            "min_subjects_covered": 19,
            "min_concepts_covered": 150
        },
        "PRODUCTION_READY": {
            "min_trusted_questions": 3000,
            "min_verified_pyqs": 500,
            "min_subjects_covered": 19,
            "min_concepts_covered": 400
        }
    }

    @classmethod
    def calculate_gap_priority_score(
        cls,
        exam_relevance_score: float,
        pyq_frequency: int,
        trusted_question_count: int,
        clinical_importance: float = 0.80
    ) -> Dict[str, Any]:
        """
        Calculates explainable Content Gap Priority Score (0.0 to 1.0).
        Higher score = higher priority for doctor authoring / review.
        """
        deficit_factor = 1.0 if trusted_question_count == 0 else 0.5 if trusted_question_count == 1 else 0.1
        pyq_factor = min(1.0, pyq_frequency * 0.20)

        score = round(
            (exam_relevance_score * 0.35) +
            (pyq_factor * 0.25) +
            (clinical_importance * 0.20) +
            (deficit_factor * 0.20),
            2
        )

        return {
            "gap_priority_score": score,
            "deficit_factor": deficit_factor,
            "pyq_factor": pyq_factor,
            "exam_relevance_score": exam_relevance_score,
            "clinical_importance": clinical_importance
        }

    @classmethod
    def determine_dataset_readiness_status(
        cls,
        total_trusted_questions: int,
        total_verified_pyqs: int,
        subjects_covered: int,
        concepts_covered: int
    ) -> Dict[str, Any]:
        """
        Determines medical content dataset readiness status with measurable blockers.
        """
        prod_t = cls.READINESS_THRESHOLDS["PRODUCTION_READY"]
        pub_t = cls.READINESS_THRESHOLDS["PUBLIC_TESTING"]
        pilot_t = cls.READINESS_THRESHOLDS["PILOT"]

        if (total_trusted_questions >= prod_t["min_trusted_questions"] and
            total_verified_pyqs >= prod_t["min_verified_pyqs"] and
            subjects_covered >= prod_t["min_subjects_covered"]):
            status = "PRODUCTION_READY"
            is_ready_for_public = True
        elif (total_trusted_questions >= pub_t["min_trusted_questions"] and
              total_verified_pyqs >= pub_t["min_verified_pyqs"] and
              subjects_covered >= pub_t["min_subjects_covered"]):
            status = "SUFFICIENT_FOR_PUBLIC_TESTING"
            is_ready_for_public = True
        elif (total_trusted_questions >= pilot_t["min_trusted_questions"] and
              total_verified_pyqs >= pilot_t["min_verified_pyqs"] and
              subjects_covered >= pilot_t["min_subjects_covered"]):
            status = "SUFFICIENT_FOR_PILOT"
            is_ready_for_public = False
        elif total_trusted_questions > 0:
            status = "PARTIALLY_VERIFIED"
            is_ready_for_public = False
        else:
            status = "BOOTSTRAP"
            is_ready_for_public = False

        return {
            "content_dataset_status": status,
            "is_ready_for_public_testing": is_ready_for_public,
            "production_ready": status == "PRODUCTION_READY",
            "pilot_gate_passed": status in ("SUFFICIENT_FOR_PILOT", "SUFFICIENT_FOR_PUBLIC_TESTING", "PRODUCTION_READY"),
            "current_metrics": {
                "trusted_questions": total_trusted_questions,
                "verified_pyqs": total_verified_pyqs,
                "subjects_covered": subjects_covered,
                "concepts_covered": concepts_covered
            },
            "production_deficits": {
                "missing_trusted_questions": max(0, prod_t["min_trusted_questions"] - total_trusted_questions),
                "missing_verified_pyqs": max(0, prod_t["min_verified_pyqs"] - total_verified_pyqs),
                "missing_subjects": max(0, prod_t["min_subjects_covered"] - subjects_covered)
            }
        }

    @classmethod
    async def generate_coverage_matrix(cls, db: AsyncSession) -> Dict[str, Any]:
        stmt_concepts = select(Concept).options(
            selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject),
            selectinload(Concept.questions)
        )
        res_c = await db.execute(stmt_concepts)
        concepts = res_c.scalars().all()

        red_gaps = []
        yellow_gaps = []
        green_healthy = []

        total_all_questions = 0
        total_trusted_questions = 0
        total_verified_pyqs = 0
        total_ai_pending = 0
        total_quarantined = 0
        total_withdrawn = 0

        subjects_with_trusted = set()
        concepts_with_trusted = set()

        for c in concepts:
            all_qs = c.questions
            trusted_qs = [q for q in all_qs if q.trust_class in cls.TRUSTED_TRUST_CLASSES and q.status in ("PUBLISHED", "APPROVED")]
            ai_pending_qs = [q for q in all_qs if q.trust_class == "AI_GENERATED_REVIEW_PENDING" or q.status == "PROPOSED"]
            quarantined_qs = [q for q in all_qs if q.status == "QUARANTINED" or q.trust_class == "QUARANTINED"]
            withdrawn_qs = [q for q in all_qs if q.status == "WITHDRAWN" or q.trust_class == "WITHDRAWN"]
            verified_pyqs = [q for q in trusted_qs if q.trust_class == "VERIFIED_PYQ"]

            total_all_questions += len(all_qs)
            total_trusted_questions += len(trusted_qs)
            total_verified_pyqs += len(verified_pyqs)
            total_ai_pending += len(ai_pending_qs)
            total_quarantined += len(quarantined_qs)
            total_withdrawn += len(withdrawn_qs)

            if len(trusted_qs) > 0:
                concepts_with_trusted.add(c.id)
                if c.topic and c.topic.chapter and c.topic.chapter.subject:
                    subjects_with_trusted.add(c.topic.chapter.subject.id)

            subject_name = c.topic.chapter.subject.name if (c.topic and c.topic.chapter and c.topic.chapter.subject) else "Subject"
            topic_name = c.topic.name if c.topic else "Topic"

            gap_calc = cls.calculate_gap_priority_score(
                exam_relevance_score=c.exam_relevance_score,
                pyq_frequency=c.pyq_frequency,
                trusted_question_count=len(trusted_qs)
            )

            item = {
                "concept_id": c.id,
                "concept_name": c.name,
                "subject_name": subject_name,
                "topic_name": topic_name,
                "exam_relevance_score": c.exam_relevance_score,
                "total_draft_questions": len(all_qs),
                "trusted_question_count": len(trusted_qs),
                "verified_pyq_count": len(verified_pyqs),
                "ai_pending_count": len(ai_pending_qs),
                "quarantined_count": len(quarantined_qs),
                "gap_priority_score": gap_calc["gap_priority_score"]
            }

            if len(trusted_qs) == 0:
                item["gap_status"] = "RED"
                item["reason"] = "Zero TRUSTED questions for high-yield concept"
                red_gaps.append(item)
            elif len(trusted_qs) == 1:
                item["gap_status"] = "YELLOW"
                item["reason"] = "Single trusted question; insufficient difficulty coverage"
                yellow_gaps.append(item)
            else:
                item["gap_status"] = "GREEN"
                green_healthy.append(item)

        # Sort gaps by priority score descending
        red_gaps.sort(key=lambda x: x["gap_priority_score"], reverse=True)
        yellow_gaps.sort(key=lambda x: x["gap_priority_score"], reverse=True)

        readiness = cls.determine_dataset_readiness_status(
            total_trusted_questions=total_trusted_questions,
            total_verified_pyqs=total_verified_pyqs,
            subjects_covered=len(subjects_with_trusted),
            concepts_covered=len(concepts_with_trusted)
        )

        return {
            "summary": {
                "total_concepts": len(concepts),
                "healthy_concepts_green": len(green_healthy),
                "limited_concepts_yellow": len(yellow_gaps),
                "missing_concepts_red": len(red_gaps),
                "total_draft_questions": total_all_questions,
                "total_trusted_questions": total_trusted_questions,
                "total_verified_pyqs": total_verified_pyqs,
                "total_ai_pending": total_ai_pending,
                "total_quarantined": total_quarantined,
                "total_withdrawn": total_withdrawn,
                "syllabus_version": "neet-pg-nmc-2026-v1.0",
                "dataset_readiness": readiness
            },
            "red_critical_gaps": red_gaps,
            "yellow_limited_gaps": yellow_gaps,
            "green_coverage": green_healthy
        }
