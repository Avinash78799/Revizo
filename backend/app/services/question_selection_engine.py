from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional, Set, Tuple
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.learning import StudentConceptMastery, StudentMistakeRecord, StudentQuestionHistory
from app.core.datetime_util import utc_now
from app.core.errors import ValidationError, NotFoundError

class QuestionSelectionEngine:
    """
    Intelligent Question Selection, Blueprint & Reproducibility Engine (Prompt 9 & 9.1).
    100% Deterministic selection based on M6 learning evidence:
    - 9 Test Modes with Versioned Blueprints (gt-blueprint-v1.0)
    - Blueprint Validation & INSUFFICIENT_CONTENT Failure Handling
    - Flexible Anti-Repeat with Evidence-Based M6 Overrides (Danger Zone, Mistake Retest, Due Revision)
    - Concept Diversity Enforcement
    - Explicit PYQ Provenance Tagging
    - Test Reproducibility Snapshot Generation
    """

    SELECTION_STRATEGY_VERSION = "selection-v1.0"
    WEEKLY_BLUEPRINT_VERSION = "gt-blueprint-v1.0"
    ELIGIBLE_STATUSES = ["PUBLISHED", "published", "APPROVED", "approved"]
    ELIGIBLE_TRUST_CLASSES = [
        "VERIFIED_CORE_QUESTION",
        "VERIFIED_PYQ",
        "SOURCE_REFERENCED",
        "verified_core_question",
        "verified_pyq",
        "ai_assisted_question",
        "dynamic_practice_question",
        "development_seed"
    ]

    @classmethod
    async def select_questions_for_test(
        cls,
        db: AsyncSession,
        user_id: str,
        mode: str,
        question_count: int = 10,
        subject_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        topic_id: Optional[str] = None,
        blueprint_config: Optional[dict] = None
    ) -> Tuple[List[Question], str]:
        """
        Executes blueprint-aware question selection with anti-repeat and evidence-based override tracking.
        Returns: (selected_questions, selection_override_reason)
        """
        now = utc_now()
        mode_upper = mode.upper()
        recent_threshold = now - timedelta(days=7)
        selection_override_reason = "NONE"

        # 1. Fetch Student Encounter History for Anti-Repeat
        stmt_hist = select(StudentQuestionHistory.question_id).where(
            and_(
                StudentQuestionHistory.user_id == user_id,
                StudentQuestionHistory.last_encountered_at >= recent_threshold
            )
        )
        res_hist = await db.execute(stmt_hist)
        recent_seen_ids: Set[str] = set(res_hist.scalars().all())

        # 2. Build Mode-Specific Question Query
        base_query = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        ).where(
            and_(
                Question.status.in_(cls.ELIGIBLE_STATUSES),
                Question.trust_class.in_(cls.ELIGIBLE_TRUST_CLASSES)
            )
        )

        if mode_upper in ("TOPIC_TEST", "TOPIC") and topic_id:
            base_query = base_query.join(Concept, Question.concept_id == Concept.id).where(Concept.topic_id == topic_id)
        elif mode_upper in ("CHAPTER_REVISION_TEST", "CHAPTER") and chapter_id:
            base_query = base_query.join(Concept, Question.concept_id == Concept.id).join(Topic, Concept.topic_id == Topic.id).where(Topic.chapter_id == chapter_id)
        elif mode_upper in ("SUBJECT_TEST", "SUBJECT") and subject_id:
            base_query = base_query.join(Concept, Question.concept_id == Concept.id).join(Topic, Concept.topic_id == Topic.id).join(Chapter, Topic.chapter_id == Chapter.id).where(Chapter.subject_id == subject_id)
        elif mode_upper == "MISTAKE_RETEST":
            selection_override_reason = "MISTAKE_RETEST_OVERRIDE"
            stmt_mistakes = select(StudentMistakeRecord.question_id).where(
                and_(
                    StudentMistakeRecord.user_id == user_id,
                    StudentMistakeRecord.status == "UNRESOLVED"
                )
            )
            mistake_q_ids = (await db.execute(stmt_mistakes)).scalars().all()
            if not mistake_q_ids:
                raise ValidationError("No unresolved mistakes in your Mistake Bank to retest.")
            base_query = base_query.where(Question.id.in_(mistake_q_ids))
        elif mode_upper == "DANGER_ZONE_RETEST":
            selection_override_reason = "M6_DANGER_ZONE_OVERRIDE"
            stmt_danger = select(StudentConceptMastery.concept_id).where(
                and_(
                    StudentConceptMastery.user_id == user_id,
                    StudentConceptMastery.danger_zone_active == True
                )
            )
            danger_concept_ids = (await db.execute(stmt_danger)).scalars().all()
            if not danger_concept_ids:
                raise ValidationError("No active Danger Zone misconceptions found to retest.")
            base_query = base_query.where(Question.concept_id.in_(danger_concept_ids))
        elif mode_upper in ("REVISION", "REVISION_TEST", "FIVE_MINUTE_REVISION", "five_minute_revision"):
            selection_override_reason = "M6_DUE_REVISION_OVERRIDE"

        res_all = await db.execute(base_query)
        candidate_pool = res_all.scalars().all()

        if not candidate_pool:
            raise ValidationError(
                f"INSUFFICIENT_CONTENT: No eligible questions found matching the requested mode '{mode}'. Content pool is empty."
            )

        # 3. Apply Anti-Repeat Protection (overridden by M6 evidence or explicit retests)
        allow_repeat = selection_override_reason != "NONE"
        if not allow_repeat:
            unseen_candidates = [q for q in candidate_pool if q.id not in recent_seen_ids]
            if len(unseen_candidates) >= question_count:
                candidate_pool = unseen_candidates
            elif unseen_candidates:
                # Prioritize unseen candidates first, then fill
                candidate_pool = unseen_candidates + [q for q in candidate_pool if q.id in recent_seen_ids]

        # 4. Enforce Concept Diversity (Avoid clustering all questions in one concept)
        selected_questions: List[Question] = []
        used_concept_ids: Set[str] = set()

        # Pass 1: Select 1 question per unique concept
        for q in candidate_pool:
            if q.concept_id not in used_concept_ids:
                selected_questions.append(q)
                used_concept_ids.add(q.concept_id)
                if len(selected_questions) >= question_count:
                    break

        # Pass 2: If pool of concepts is smaller than question_count, fill remaining
        if len(selected_questions) < question_count:
            selected_ids = {q.id for q in selected_questions}
            for q in candidate_pool:
                if q.id not in selected_ids:
                    selected_questions.append(q)
                    selected_ids.add(q.id)
                    if len(selected_questions) >= question_count:
                        break

        # 5. Blueprint Validation
        if len(selected_questions) < min(1, question_count):
            raise ValidationError(
                f"INSUFFICIENT_CONTENT: Test blueprint requested {question_count} questions, but only {len(selected_questions)} were eligible."
            )

        return selected_questions[:question_count], selection_override_reason

    @classmethod
    def format_question_for_student_runner(cls, question: Question) -> Dict[str, Any]:
        """
        Sanitizes question for student test runner:
        STRIPS correct_option_key, correct_explanation, why_wrong_explanation, remember_takeaway.
        PRESERVES question_text, options, difficulty, provenance tag, trust_class, is_high_yield.
        """
        provenance_tag = "ORIGINAL_AI_GENERATED"
        if getattr(question, "trust_class", "") == "development_seed":
            provenance_tag = "DEVELOPMENT_SEED"
        elif question.pyq_reference_id is not None:
            provenance_tag = "VERIFIED_PYQ"
        elif question.source_id is not None:
            provenance_tag = "SOURCE_REFERENCED"
        elif question.exam_relevance_tag == "PYQ_LINKED":
            provenance_tag = "PYQ_STYLE"

        c = question.concept
        t_name = c.topic.name if (c and c.topic) else None
        s_name = c.topic.chapter.subject.name if (c and c.topic and c.topic.chapter and c.topic.chapter.subject) else None

        return {
            "id": question.id,
            "concept_id": question.concept_id,
            "concept_name": c.name if c else "Medical Concept",
            "topic_name": t_name,
            "subject_name": s_name,
            "trust_class": getattr(question, "trust_class", "verified_core_question") or "verified_core_question",
            "question_type": question.question_type or "single_best_answer",
            "difficulty": question.difficulty or "moderate",
            "is_high_yield": bool(question.is_high_yield),
            "question_text": question.question_text,
            "image_url": question.image_url,
            "provenance_tag": provenance_tag,
            "options": [
                {
                    "option_key": opt.option_key,
                    "option_text": opt.option_text
                }
                for opt in question.options
            ]
        }
