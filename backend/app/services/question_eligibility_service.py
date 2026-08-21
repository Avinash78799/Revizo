from sqlalchemy import select, and_, not_
from sqlalchemy.sql import Select
from app.models.question import Question

class QuestionEligibilityService:
    """
    Single authoritative question eligibility service.
    Guarantees that only verified, published, non-quarantined questions
    reach students during active test selection.
    """

    ALLOWED_TRUST_CLASSES = {
        "verified_core_question",
        "ai_assisted_question",
        "dynamic_practice_question"
    }

    @classmethod
    def apply_eligibility_filter(cls, query: Select, allow_dev_seeds: bool = False) -> Select:
        """
        Applies standard eligibility criteria to any SQLAlchemy query selecting Question entities.
        """
        trust_filter = (
            Question.trust_class.in_(cls.ALLOWED_TRUST_CLASSES | {"development_seed"})
            if allow_dev_seeds
            else Question.trust_class.in_(cls.ALLOWED_TRUST_CLASSES)
        )

        return query.where(
            and_(
                Question.status == "published",
                trust_filter,
                Question.status != "quarantined",
                Question.status != "retired"
            )
        )

    @classmethod
    def is_question_eligible(cls, question: Question, allow_dev_seeds: bool = False) -> bool:
        """
        In-memory validation check for a specific Question instance.
        """
        if question.status != "published":
            return False
        if question.status in ("quarantined", "retired"):
            return False
        
        valid_classes = cls.ALLOWED_TRUST_CLASSES | ({"development_seed"} if allow_dev_seeds else set())
        return question.trust_class in valid_classes
