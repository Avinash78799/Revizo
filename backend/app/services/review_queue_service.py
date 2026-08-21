import uuid
from typing import Dict, List, Any, Optional
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question, QuestionOption, QuestionReview
from app.models.taxonomy import Subject, Chapter, Topic, Concept
from app.models.source import Source
from app.models.reviewer import MedicalReviewerProfile
from app.core.datetime_util import utc_now

class ReviewQueueService:
    """
    Milestone 12.6: Human Medical Review Queue Management Service.
    
    Routes candidate questions to human medical doctors based on risk profile:
    1. Standard-Risk Queue -> 1 Verified Doctor Approval.
    2. High-Risk Queue -> 2 Independent Distinct Verified Doctor Approvals.
    3. Quarantine Queue -> Critical Failures, Disputed Guidelines, or Contradictions.
    """

    @classmethod
    async def get_standard_risk_queue(
        cls,
        db: AsyncSession,
        subject_code: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Question]:
        """
        Retrieves standard-risk candidate questions awaiting single-doctor review.
        """
        query = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.source),
            selectinload(Question.concept)
        ).where(
            and_(
                Question.status == "PROPOSED",
                Question.trust_class == "AI_GENERATED_REVIEW_PENDING",
                Question.is_high_risk.is_(False)
            )
        )

        if subject_code:
            query = query.join(Concept, Question.concept_id == Concept.id)\
                         .join(Topic, Concept.topic_id == Topic.id)\
                         .join(Chapter, Topic.chapter_id == Chapter.id)\
                         .join(Subject, Chapter.subject_id == Subject.id)\
                         .where(Subject.code == subject_code)

        query = query.order_by(Question.created_at.asc()).offset(offset).limit(limit)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_high_risk_two_doctor_queue(
        cls,
        db: AsyncSession,
        subject_code: Optional[str] = None,
        reviewer_id: Optional[str] = None,
        stage: Optional[str] = None,  # 'STAGE_1_PENDING' or 'STAGE_2_PENDING'
        limit: int = 50,
        offset: int = 0
    ) -> List[Question]:
        """
        Retrieves high-risk candidate questions awaiting first or second doctor review.
        If reviewer_id is supplied, excludes questions where this reviewer has already performed the 1st review.
        """
        query = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.source),
            selectinload(Question.concept)
        ).where(
            and_(
                Question.is_high_risk.is_(True),
                Question.status.in_(["PROPOSED", "REVIEW_PENDING", "proposed", "review_pending"])
            )
        )

        if stage == "STAGE_1_PENDING":
            query = query.where(Question.first_reviewer_id.is_(None))
        elif stage == "STAGE_2_PENDING":
            query = query.where(Question.first_reviewer_id.isnot(None))

        # Filter out questions this reviewer already approved in stage 1
        if reviewer_id:
            query = query.where(
                or_(
                    Question.first_reviewer_id.is_(None),
                    Question.first_reviewer_id != reviewer_id
                )
            )

        if subject_code:
            query = query.join(Concept, Question.concept_id == Concept.id)\
                         .join(Topic, Concept.topic_id == Topic.id)\
                         .join(Chapter, Topic.chapter_id == Chapter.id)\
                         .join(Subject, Chapter.subject_id == Subject.id)\
                         .where(Subject.code == subject_code)

        query = query.order_by(Question.created_at.asc()).offset(offset).limit(limit)
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_quarantine_queue(
        cls,
        db: AsyncSession,
        limit: int = 50,
        offset: int = 0
    ) -> List[Question]:
        """
        Retrieves quarantined or rejected questions requiring Medical Director review.
        """
        query = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.source)
        ).where(
            Question.status.in_(["QUARANTINED", "REJECTED", "WITHDRAWN"])
        ).order_by(Question.updated_at.desc()).offset(offset).limit(limit)

        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_review_queue_summary(cls, db: AsyncSession) -> Dict[str, Any]:
        """
        Returns real-time queue counts across all stages.
        """
        # Standard Risk Pending
        stmt_std = select(func.count(Question.id)).where(
            and_(
                Question.status == "PROPOSED",
                Question.trust_class == "AI_GENERATED_REVIEW_PENDING",
                Question.is_high_risk.is_(False)
            )
        )
        std_pending = (await db.execute(stmt_std)).scalar_one()

        # High Risk Stage 1 Pending (0 reviews)
        stmt_hr1 = select(func.count(Question.id)).where(
            and_(
                Question.is_high_risk.is_(True),
                Question.status == "PROPOSED",
                Question.first_reviewer_id.is_(None)
            )
        )
        hr_stage1_pending = (await db.execute(stmt_hr1)).scalar_one()

        # High Risk Stage 2 Pending (1 review recorded, needs second distinct doctor)
        stmt_hr2 = select(func.count(Question.id)).where(
            and_(
                Question.is_high_risk.is_(True),
                Question.status == "REVIEW_PENDING",
                Question.first_reviewer_id.isnot(None),
                Question.second_reviewer_id.is_(None)
            )
        )
        hr_stage2_pending = (await db.execute(stmt_hr2)).scalar_one()

        # Doctor Verified / Approved
        stmt_app = select(func.count(Question.id)).where(
            Question.trust_class.in_(["VERIFIED_CORE_QUESTION", "VERIFIED_PYQ", "verified_core_question", "verified_pyq"])
        )
        approved_count = (await db.execute(stmt_app)).scalar_one()

        # Quarantined / Rejected
        stmt_quar = select(func.count(Question.id)).where(
            Question.status.in_(["QUARANTINED", "REJECTED", "WITHDRAWN"])
        )
        quarantine_count = (await db.execute(stmt_quar)).scalar_one()

        return {
            "standard_risk_pending": std_pending,
            "high_risk_stage1_pending": hr_stage1_pending,
            "high_risk_stage2_pending": hr_stage2_pending,
            "total_pending_review": std_pending + hr_stage1_pending + hr_stage2_pending,
            "doctor_approved": approved_count,
            "quarantined": quarantine_count
        }

    @classmethod
    async def get_doctor_queue_dashboard(
        cls,
        db: AsyncSession,
        reviewer_user_id: str
    ) -> Dict[str, Any]:
        """
        Retrieves doctor dashboard with specialty-aware queue routing and performance metrics.
        """
        from app.services.reviewer_service import ReviewerService
        from app.core.errors import AuthorizationError, NotFoundError

        profile = await ReviewerService.get_profile_by_user_id(db, reviewer_user_id)
        if not profile:
            raise NotFoundError(f"Medical reviewer profile not found for user {reviewer_user_id}")
        if profile.verification_status != "VERIFIED":
            raise AuthorizationError(f"Reviewer status is '{profile.verification_status}'. Only VERIFIED doctors can access review queue.")

        global_summary = await cls.get_review_queue_summary(db)

        # Count reviews performed by this reviewer
        stmt_rev_count = select(func.count(QuestionReview.id)).where(QuestionReview.reviewer_id == reviewer_user_id)
        my_reviews_count = (await db.execute(stmt_rev_count)).scalar_one()

        # Available high-risk questions for this doctor (excluding questions they reviewed in stage 1)
        hr_available = await cls.get_high_risk_two_doctor_queue(db, reviewer_id=reviewer_user_id, limit=50)

        return {
            "reviewer": {
                "user_id": reviewer_user_id,
                "qualification": profile.credential_type,
                "specialty": profile.specialty,
                "registration_number": profile.registration_number,
                "medical_council": profile.medical_council,
                "verification_status": profile.verification_status
            },
            "metrics": {
                "my_completed_reviews": my_reviews_count,
                "global_standard_pending": global_summary["standard_risk_pending"],
                "global_high_risk_pending": global_summary["high_risk_stage1_pending"] + global_summary["high_risk_stage2_pending"],
                "global_doctor_approved": global_summary["doctor_approved"],
                "global_quarantined": global_summary["quarantined"]
            },
            "high_risk_queue_available_count": len(hr_available)
        }

    @classmethod
    async def get_review_interface_payload(
        cls,
        db: AsyncSession,
        question_id: str,
        reviewer_user_id: str
    ) -> Dict[str, Any]:
        """
        Constructs the comprehensive review interface data payload for an assigned question.
        """
        from app.services.reviewer_service import ReviewerService
        from app.core.errors import AuthorizationError, NotFoundError

        profile = await ReviewerService.get_profile_by_user_id(db, reviewer_user_id)
        if not profile or profile.verification_status != "VERIFIED":
            raise AuthorizationError("Only VERIFIED medical doctors can access the review interface.")

        stmt = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.source),
            selectinload(Question.concept),
            selectinload(Question.evidence_references),
            selectinload(Question.reviews)
        ).where(Question.id == question_id)

        q = (await db.execute(stmt)).scalars().first()
        if not q:
            raise NotFoundError(f"Question {question_id} not found.")

        # If high risk and this reviewer already reviewed in stage 1 -> block self-re-review
        if q.is_high_risk and q.first_reviewer_id == reviewer_user_id:
            raise AuthorizationError("Doctor A cannot act as Doctor B for the same high-risk question.")

        options_payload = [
            {
                "key": opt.option_key,
                "text": opt.option_text,
                "is_correct": opt.is_correct,
                "why_wrong_explanation": opt.why_wrong_explanation
            }
            for opt in sorted(q.options, key=lambda x: x.option_key)
        ]

        source_payload = None
        if q.source:
            source_payload = {
                "id": q.source.id,
                "title": q.source.title,
                "edition": q.source.edition,
                "publisher": q.source.publisher,
                "reference_identifier": q.source.reference_identifier,
                "verification_status": q.source.verification_status
            }

        evidence_payload = [
            {
                "claim_snippet": ev.claim_snippet,
                "page_or_section": ev.page_or_section,
                "fact_type": ev.fact_type
            }
            for ev in q.evidence_references
        ]

        # Blind review history for Doctor B during High-Risk Stage 2 review to ensure independent evaluation
        is_blinded_stage2 = q.is_high_risk and q.first_reviewer_id and not q.second_reviewer_id
        review_history = []
        if not is_blinded_stage2:
            review_history = [
                {
                    "reviewer_id": rev.reviewer_id,
                    "credential_status": rev.reviewer_credential_status,
                    "verdict": rev.verdict,
                    "clinical_notes": rev.clinical_notes,
                    "reviewed_at": rev.created_at.isoformat() if rev.created_at else None
                }
                for rev in q.reviews
            ]

        return {
            "question_id": q.id,
            "status": q.status,
            "trust_class": q.trust_class,
            "question_text": q.question_text,
            "options": options_payload,
            "correct_explanation": q.correct_explanation,
            "remember_takeaway": q.remember_takeaway,
            "is_high_risk": q.is_high_risk,
            "high_risk_category": q.high_risk_category,
            "source": source_payload,
            "evidence": evidence_payload,
            "review_history": review_history,
            "required_review_stage": "STAGE_2" if (q.is_high_risk and q.first_reviewer_id) else "STAGE_1"
        }
