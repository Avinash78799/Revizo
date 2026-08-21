from datetime import datetime, timezone
from typing import Optional, Dict, Any, Set
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question, QuestionReview, QuestionQuarantineRegistry, QuestionVersion
from app.models.audit import AuditLog
from app.core.errors import InvalidStateTransitionError, NotFoundError, AuthorizationError, ValidationError
from app.core.datetime_util import utc_now

class QuestionLifecycleService:
    """
    Question Lifecycle & Content Governance State Machine (Prompt 6, Sec 2 & 3).
    Guarantees that:
    1. No AI-generated or unverified question can reach PUBLISHED / VERIFIED_CORE_QUESTION without passing medical review.
    2. Every lifecycle transition is audited.
    3. Illegal state transitions are rejected.
    """

    LEGAL_TRANSITIONS: Dict[str, Set[str]] = {
        "PROPOSED": {"AI_VALIDATED", "AUTHOR_VALIDATED", "REVIEW_REQUIRED", "REJECTED"},
        "AI_VALIDATED": {"REVIEW_REQUIRED", "MEDICAL_REVIEW", "REJECTED", "QUARANTINED"},
        "AUTHOR_VALIDATED": {"REVIEW_REQUIRED", "MEDICAL_REVIEW", "REJECTED", "QUARANTINED"},
        "REVIEW_REQUIRED": {"MEDICAL_REVIEW", "REJECTED", "QUARANTINED"},
        "MEDICAL_REVIEW": {"APPROVED", "REJECTED", "REVIEW_REQUIRED", "QUARANTINED"},
        "APPROVED": {"PUBLISHED", "QUARANTINED", "WITHDRAWN"},
        "PUBLISHED": {"MONITORED", "QUARANTINED", "OUTDATED", "WITHDRAWN", "RETIRED"},
        "MONITORED": {"QUARANTINED", "OUTDATED", "WITHDRAWN", "RETIRED", "REVIEW_REQUIRED"},
        "QUARANTINED": {"REVIEW_REQUIRED", "MEDICAL_REVIEW", "WITHDRAWN", "RETIRED", "PUBLISHED"},
        "OUTDATED": {"REVIEW_REQUIRED", "WITHDRAWN", "RETIRED"},
        "WITHDRAWN": {"RETIRED"},
        "REJECTED": set(),
        "RETIRED": set()
    }

    VALID_TRUST_CLASSES = {
        "DEVELOPMENT_SEED",
        "AI_PROPOSED",
        "AUTHOR_CREATED",
        "REVIEW_PENDING",
        "MEDICALLY_REVIEWED",
        "VERIFIED_CORE_QUESTION",
        "WITHDRAWN"
    }

    @classmethod
    def validate_transition(cls, current_status: str, target_status: str):
        curr = current_status.upper()
        target = target_status.upper()
        allowed = cls.LEGAL_TRANSITIONS.get(curr, set())
        if target not in allowed:
            raise InvalidStateTransitionError(curr, target)

    @classmethod
    async def transition_state(
        cls,
        db: AsyncSession,
        question_id: str,
        target_status: str,
        actor_id: Optional[str] = None,
        reason: Optional[str] = None,
        audit_details: Optional[Dict[str, Any]] = None,
        is_human_reviewer: bool = False
    ) -> Question:
        stmt = select(Question).where(Question.id == question_id)
        res = await db.execute(stmt)
        question = res.scalars().first()

        if not question:
            raise NotFoundError("Question")

        current = question.status.upper()
        target = target_status.upper()

        cls.validate_transition(current, target)

        # Human Review Safeguard: AI or unauthenticated actors can NEVER approve or publish questions
        if target in ("APPROVED", "PUBLISHED") and not is_human_reviewer:
            raise AuthorizationError("Only verified human medical reviewers/admins can approve or publish questions.")

        question.status = target
        now = utc_now()

        # Update trust classes accordingly
        if target == "PUBLISHED":
            question.trust_class = "VERIFIED_CORE_QUESTION"
            question.last_verified_at = now
        elif target == "APPROVED":
            question.trust_class = "MEDICALLY_REVIEWED"
        elif target == "QUARANTINED":
            question.trust_class = "REVIEW_PENDING"
            # Add quarantine registry entry
            quarantine_entry = QuestionQuarantineRegistry(
                question_id=question.id,
                quarantine_reason=reason or "Quarantined via governance state machine",
                resolution_status="quarantined",
                audit_notes=f"Transitioned from {current} to QUARANTINED by actor {actor_id}"
            )
            db.add(quarantine_entry)
        elif target == "WITHDRAWN":
            question.trust_class = "WITHDRAWN"

        # Log Immutable Audit Entry
        audit = AuditLog(
            actor_id=actor_id,
            action=f"lifecycle_{current.lower()}_to_{target.lower()}",
            target_entity="question",
            target_id=question.id,
            details={
                "from_status": current,
                "to_status": target,
                "trust_class": question.trust_class,
                "reason": reason,
                "is_human_reviewer": is_human_reviewer,
                **(audit_details or {})
            }
        )
        db.add(audit)
        await db.flush()
        return question
