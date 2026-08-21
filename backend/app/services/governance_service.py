from typing import Dict, Any, List, Optional
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import (
    Question,
    QuestionOption,
    QuestionVersion,
    QuestionReview,
    QuestionQualityScorecard,
    QuestionQuarantineRegistry,
    QuestionReport
)
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.models.source import Source, EvidenceReference, PyqReference
from app.models.audit import AuditLog
from app.services.question_lifecycle_service import QuestionLifecycleService
from app.core.errors import NotFoundError, ValidationError, AuthorizationError
from app.core.datetime_util import utc_now

class GovernanceService:
    """
    Medical Content Governance & Quality Assurance Service (Prompt 6).
    Handles:
    - Immutable question versioning
    - Reviewer decision engine (Approve, Reject, Request Revision, Quarantine, Outdated)
    - Source & PYQ provenance verification
    - Content coverage analytics
    """

    @classmethod
    async def create_question_version_snapshot(
        cls,
        db: AsyncSession,
        question_id: str,
        changed_by: Optional[str] = None,
        change_reason: Optional[str] = None
    ) -> QuestionVersion:
        stmt = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.evidence_references)
        ).where(Question.id == question_id)
        res = await db.execute(stmt)
        question = res.scalars().first()

        if not question:
            raise NotFoundError("Question")

        correct_opt = next((o.option_key for o in question.options if o.is_correct), "A")
        options_dict = [
            {"option_key": o.option_key, "option_text": o.option_text, "is_correct": o.is_correct, "why_wrong": o.why_wrong_explanation}
            for o in question.options
        ]

        version = QuestionVersion(
            question_id=question.id,
            version_number=question.content_version,
            question_text=question.question_text,
            options_snapshot={"options": options_dict},
            correct_option_key=correct_opt,
            correct_explanation=question.correct_explanation,
            remember_takeaway=question.remember_takeaway,
            source_citation=question.source_citation,
            changed_by=changed_by,
            change_reason=change_reason or "Initial/updated version snapshot"
        )
        db.add(version)
        question.content_version += 1
        await db.flush()
        return version

    @classmethod
    async def execute_medical_review_decision(
        cls,
        db: AsyncSession,
        reviewer_id: str,
        question_id: str,
        verdict: str,  # 'APPROVE', 'REJECT', 'REQUEST_REVISION', 'QUARANTINE', 'MARK_OUTDATED'
        clinical_notes: Optional[str] = None,
        guideline_verified: bool = True
    ) -> Question:
        stmt = select(Question).options(selectinload(Question.options)).where(Question.id == question_id)
        res = await db.execute(stmt)
        question = res.scalars().first()

        if not question:
            raise NotFoundError("Question")

        verdict_norm = verdict.upper()
        now = utc_now()

        # Record Review
        review = QuestionReview(
            question_id=question.id,
            reviewer_id=reviewer_id,
            verdict=verdict_norm,
            clinical_notes=clinical_notes,
            guideline_verified=guideline_verified
        )
        db.add(review)

        question.reviewed_by = reviewer_id
        question.reviewed_at = now
        question.review_notes = clinical_notes

        if verdict_norm == "APPROVE":
            # Direct promotion to PUBLISHED and VERIFIED_CORE_QUESTION
            question.status = "PUBLISHED"
            question.trust_class = "VERIFIED_CORE_QUESTION"
            question.last_verified_at = now
            # Create version snapshot upon approval
            await cls.create_question_version_snapshot(db, question.id, changed_by=reviewer_id, change_reason="Doctor Review Approval")
        elif verdict_norm == "REJECT":
            question.status = "REJECTED"
        elif verdict_norm == "REQUEST_REVISION":
            question.status = "REVIEW_REQUIRED"
        elif verdict_norm == "QUARANTINE":
            question.status = "QUARANTINED"
            question.trust_class = "REVIEW_PENDING"
            quarantine = QuestionQuarantineRegistry(
                question_id=question.id,
                quarantine_reason=clinical_notes or "Reviewer Quarantine",
                resolution_status="quarantined"
            )
            db.add(quarantine)
        elif verdict_norm == "MARK_OUTDATED":
            question.status = "OUTDATED"
            question.trust_class = "REVIEW_PENDING"

        audit = AuditLog(
            actor_id=reviewer_id,
            action=f"doctor_review_{verdict_norm.lower()}",
            target_entity="question",
            target_id=question.id,
            details={"verdict": verdict_norm, "notes": clinical_notes, "new_status": question.status}
        )
        db.add(audit)
        await db.flush()
        return question

    @classmethod
    async def get_content_coverage_matrix(cls, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Calculates content coverage analytics:
        Subject -> Topic -> Verified count, Pending count, AI proposed count, Coverage gaps.
        """
        stmt = select(Subject).options(
            selectinload(Subject.chapters).selectinload(Chapter.topics).selectinload(Topic.concepts)
        ).order_by(Subject.order_index.asc())
        res = await db.execute(stmt)
        subjects = res.scalars().all()

        coverage_data = []
        for sub in subjects:
            total_verified = 0
            total_pending = 0
            total_proposed = 0
            topic_summaries = []

            for chap in sub.chapters:
                for top in chap.topics:
                    concept_ids = [c.id for c in top.concepts]
                    if not concept_ids:
                        continue

                    # Query questions under this topic's concepts
                    stmt_q = select(Question).where(Question.concept_id.in_(concept_ids))
                    res_q = await db.execute(stmt_q)
                    q_list = res_q.scalars().all()

                    verified_count = sum(1 for q in q_list if q.status == "PUBLISHED" and q.trust_class == "VERIFIED_CORE_QUESTION")
                    pending_count = sum(1 for q in q_list if q.status in ("REVIEW_REQUIRED", "AI_VALIDATED", "MEDICAL_REVIEW"))
                    proposed_count = sum(1 for q in q_list if q.status == "PROPOSED")

                    total_verified += verified_count
                    total_pending += pending_count
                    total_proposed += proposed_count

                    topic_summaries.append({
                        "topic_id": top.id,
                        "topic_name": top.name,
                        "chapter_name": chap.name,
                        "verified_questions": verified_count,
                        "review_pending": pending_count,
                        "ai_proposed": proposed_count,
                        "is_coverage_gap": verified_count < 3  # Target min 3 verified questions per topic
                    })

            coverage_data.append({
                "subject_id": sub.id,
                "subject_name": sub.name,
                "subject_code": sub.code,
                "total_verified": total_verified,
                "total_pending": total_pending,
                "total_proposed": total_proposed,
                "topics": topic_summaries
            })

        return coverage_data
