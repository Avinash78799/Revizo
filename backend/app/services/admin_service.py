from typing import Optional, Dict, Any, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQuarantineRegistry, QuestionReport
from app.models.audit import AuditLog
from app.core.errors import NotFoundError, InvalidStateTransitionError

class AdminService:
    """
    Administrative and medical review service.
    Enforces question lifecycle transitions and audit logging.
    """

    ALLOWED_TRANSITIONS = {
        "draft": {"ai_generated", "validating", "review_required", "retired"},
        "ai_generated": {"validating", "review_required", "quarantined", "retired"},
        "validating": {"review_required", "quarantined", "retired"},
        "review_required": {"published", "quarantined", "retired", "draft"},
        "published": {"quarantined", "retired"},
        "quarantined": {"review_required", "retired", "published"},
        "retired": set()
    }

    @classmethod
    def validate_transition(cls, from_status: str, to_status: str):
        allowed = cls.ALLOWED_TRANSITIONS.get(from_status, set())
        if to_status not in allowed:
            raise InvalidStateTransitionError(from_status, to_status)

    @classmethod
    async def log_audit_event(
        cls,
        db: AsyncSession,
        actor_id: Optional[str],
        action: str,
        target_entity: str,
        target_id: str,
        details: Dict[str, Any]
    ):
        # Ensure no sensitive tokens/passwords are captured in audit logs
        safe_details = {k: v for k, v in details.items() if k not in ("password", "token", "hashed_password")}
        log = AuditLog(
            actor_id=actor_id,
            action=action,
            target_entity=target_entity,
            target_id=target_id,
            details=safe_details
        )
        db.add(log)
        await db.flush()

    @classmethod
    async def review_and_publish_question(
        cls,
        db: AsyncSession,
        reviewer_id: str,
        question_id: str,
        is_high_yield: bool = False,
        notes: Optional[str] = None
    ) -> Question:
        stmt = select(Question).options(selectinload(Question.options)).where(Question.id == question_id)
        res = await db.execute(stmt)
        question = res.scalars().first()

        if not question:
            raise NotFoundError("Question")

        cls.validate_transition(question.status, "published")

        question.status = "published"
        question.trust_class = "verified_core_question"
        question.is_high_yield = is_high_yield
        question.reviewed_by = reviewer_id
        question.review_notes = notes

        review = QuestionReview(
            question_id=question.id,
            reviewer_id=reviewer_id,
            verdict="approved",
            notes=notes
        )
        db.add(review)

        await cls.log_audit_event(
            db=db,
            actor_id=reviewer_id,
            action="question_published",
            target_entity="question",
            target_id=question.id,
            details={"verdict": "approved", "is_high_yield": is_high_yield, "notes": notes}
        )

        await db.flush()
        return question

    @classmethod
    async def quarantine_question(
        cls,
        db: AsyncSession,
        actor_id: str,
        question_id: str,
        reason: str,
        audit_notes: Optional[str] = None
    ) -> Question:
        stmt = select(Question).where(Question.id == question_id)
        res = await db.execute(stmt)
        question = res.scalars().first()

        if not question:
            raise NotFoundError("Question")

        cls.validate_transition(question.status, "quarantined")
        question.status = "quarantined"

        quarantine = QuestionQuarantineRegistry(
            question_id=question.id,
            quarantine_reason=reason,
            resolution_status="quarantined",
            audit_notes=audit_notes
        )
        db.add(quarantine)

        await cls.log_audit_event(
            db=db,
            actor_id=actor_id,
            action="question_quarantined",
            target_entity="question",
            target_id=question.id,
            details={"reason": reason, "notes": audit_notes}
        )

        await db.flush()
        return question

    @classmethod
    async def resolve_question_report(
        cls,
        db: AsyncSession,
        resolver_id: str,
        report_id: str,
        action_taken: str
    ) -> QuestionReport:
        stmt = select(QuestionReport).where(QuestionReport.id == report_id)
        res = await db.execute(stmt)
        report = res.scalars().first()

        if not report:
            raise NotFoundError("Question report")

        report.resolved = True
        report.resolved_by = resolver_id

        await cls.log_audit_event(
            db=db,
            actor_id=resolver_id,
            action="report_resolved",
            target_entity="question_report",
            target_id=report.id,
            details={"action_taken": action_taken}
        )

        await db.flush()
        return report
