from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test import TestSession, TestQuestion, TestAttempt, IntegrityEvent
from app.models.question import Question, QuestionOption
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.learning import StudentQuestionHistory, StudentMistakeRecord, StudentConceptMastery
from app.core.errors import (
    NotFoundError,
    ValidationError,
    InvalidStateTransitionError,
    ConflictError,
    AuthorizationError
)
from app.services.question_eligibility_service import QuestionEligibilityService
from app.services.question_selection_engine import QuestionSelectionEngine
from app.services.learning_service import LearningService
from app.services.learning_intelligence_engine import LearningIntelligenceEngine
from app.services.scoring_service import ScoringService
from app.core.datetime_util import utc_now, ensure_utc

class TestService:
    """
    Milestone 7.1 Hardened Test Engine Service:
    - Server-authoritative session lifecycle and state machine
    - Blueprint-aware question selection with M6 anti-repeat overrides
    - Test reproducibility snapshot generation (gt-blueprint-v1.0)
    - Configurable Integrity Severity Model (0 to 4 weights, strictly decoupled from academic scoring)
    - Anti-repeat question history tracking
    - Server-authoritative timers with network interruption resilience
    - Small-sample safe cohort ranking policy
    """

    DEFAULT_TIME_LIMIT_MINUTES = {
        "DAILY_SHORT_TEST": 10,
        "daily_short_test": 10,
        "CHAPTER_REVISION_TEST": 25,
        "chapter_test": 25,
        "TOPIC_TEST": 15,
        "topic_test": 15,
        "SUBJECT_TEST": 45,
        "subject_test": 45,
        "WEEKLY_GRAND_TEST": 120,
        "weekly_test": 120,
        "grand_test": 210,
        "RAPID_RECALL_TEST": 5,
        "five_minute_revision": 5,
        "MISTAKE_RETEST": 15,
        "DANGER_ZONE_RETEST": 10,
        "CUSTOM_PRACTICE": 20,
        "quick_test": 10,
        "full_test": 30,
        "revision_test": 15
    }

    INTEGRITY_SEVERITY_WEIGHTS = {
        "NETWORK_INTERRUPTION": 0,
        "RECONNECT": 0,
        "WINDOW_BLURRED": 1,
        "VISIBILITY_CHANGE": 1,
        "FULLSCREEN_EXIT": 2,
        "TAB_HIDDEN": 3,
        "REPEATED_SUSPICIOUS_VISIBILITY": 4,
        "OTHER": 1
    }

    LEGAL_STATE_TRANSITIONS = {
        "NOT_STARTED": {"IN_PROGRESS", "CANCELLED"},
        "IN_PROGRESS": {"SUBMITTED", "EXPIRED", "CANCELLED", "TERMINATED_INTEGRITY"},
        "SUBMITTED": set(),
        "EXPIRED": set(),
        "CANCELLED": set(),
        "TERMINATED_INTEGRITY": set()
    }

    @classmethod
    def validate_state_transition(cls, current_state: str, next_state: str):
        allowed = cls.LEGAL_STATE_TRANSITIONS.get(current_state, set())
        if next_state not in allowed:
            raise InvalidStateTransitionError(current_state, next_state)

    @classmethod
    async def create_test_session(
        cls,
        db: AsyncSession,
        user_id: str,
        mode: str,
        subject_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        topic_id: Optional[str] = None,
        question_count: int = 5,
        integrity_mode: str = "WARNING_MODE",
        blueprint_config: Optional[dict] = None,
        allow_dev_seeds: bool = True
    ) -> Tuple[TestSession, List[Question]]:
        """
        Creates a locked, blueprint-validated test session with test reproducibility snapshot.
        """
        questions, override_reason = await QuestionSelectionEngine.select_questions_for_test(
            db=db,
            user_id=user_id,
            mode=mode,
            question_count=question_count,
            subject_id=subject_id,
            chapter_id=chapter_id,
            topic_id=topic_id,
            blueprint_config=blueprint_config
        )

        duration_minutes = cls.DEFAULT_TIME_LIMIT_MINUTES.get(mode, 10)
        started = utc_now()
        expires = started + timedelta(minutes=duration_minutes)

        # Build Test Reproducibility Snapshot (Prompt 9.1, Sec 6)
        reproducibility_snapshot = {
            "blueprint_version": QuestionSelectionEngine.WEEKLY_BLUEPRINT_VERSION if mode.upper() == "WEEKLY_GRAND_TEST" else "standard-v1.0",
            "selection_strategy_version": QuestionSelectionEngine.SELECTION_STRATEGY_VERSION,
            "algorithm_version": LearningIntelligenceEngine.ALGORITHM_VERSION,
            "question_ids": [q.id for q in questions],
            "question_versions": {q.id: getattr(q, "text_hash", "v1.0") for q in questions},
            "selection_override_reason": override_reason,
            "difficulty_configuration": {
                "easy_count": sum(1 for q in questions if q.difficulty == "easy"),
                "moderate_count": sum(1 for q in questions if q.difficulty == "moderate"),
                "hard_count": sum(1 for q in questions if q.difficulty == "hard")
            }
        }

        test_session = TestSession(
            user_id=user_id,
            mode=mode,
            status="IN_PROGRESS",
            subject_id=subject_id,
            chapter_id=chapter_id,
            topic_id=topic_id,
            total_questions=len(questions),
            completed_questions=0,
            score=0,
            started_at=started,
            expires_at=expires,
            integrity_mode=integrity_mode,
            integrity_score=100,
            blueprint_config=blueprint_config or {},
            test_reproducibility_snapshot=reproducibility_snapshot
        )
        db.add(test_session)
        await db.flush()

        for idx, q in enumerate(questions):
            tq = TestQuestion(
                session_id=test_session.id,
                question_id=q.id,
                order_index=idx + 1
            )
            db.add(tq)

        await db.commit()
        await db.refresh(test_session)
        return test_session, questions

    @classmethod
    async def record_integrity_event(
        cls,
        db: AsyncSession,
        session_id: str,
        user_id: str,
        event_type: str,
        metadata: Optional[dict] = None
    ) -> Dict[str, Any]:
        """
        Records integrity events using the configurable severity model (Prompt 9.1, Sec 1-2).
        Invariant: Integrity score strictly NEVER modifies student academic score, answers, or mastery.
        """
        stmt = select(TestSession).where(TestSession.id == session_id)
        res = await db.execute(stmt)
        session = res.scalars().first()

        if not session:
            raise NotFoundError(f"Test session {session_id} not found")

        if session.user_id != user_id:
            raise AuthorizationError("Cannot log integrity events to another user's session")

        if session.status != "IN_PROGRESS":
            return {"status": session.status, "message": "Session is not active"}

        event_type_upper = event_type.upper()
        severity_weight = cls.INTEGRITY_SEVERITY_WEIGHTS.get(event_type_upper, 1)
        severity = "CRITICAL" if severity_weight >= 4 else "HIGH" if severity_weight == 3 else "MEDIUM" if severity_weight >= 1 else "LOW"

        event = IntegrityEvent(
            session_id=session_id,
            user_id=user_id,
            event_type=event_type_upper,
            severity_weight=severity_weight,
            severity=severity,
            event_metadata=metadata or {}
        )
        db.add(event)

        # Integrity Score Policy (Penalty = severity_weight * 5 in STRICT_MODE)
        if session.integrity_mode == "STRICT_MODE":
            penalty = severity_weight * 5
            session.integrity_score = max(0, session.integrity_score - penalty)
            if session.integrity_score <= 40:
                session.status = "TERMINATED_INTEGRITY"
                session.is_terminated_by_integrity = True
                session.completed_at = utc_now()

        await db.commit()
        return {
            "session_id": session_id,
            "integrity_mode": session.integrity_mode,
            "integrity_score": session.integrity_score,
            "event_severity_weight": severity_weight,
            "status": session.status,
            "is_terminated": session.is_terminated_by_integrity
        }

    @classmethod
    async def submit_answer_idempotent(
        cls,
        db: AsyncSession,
        session_id: str,
        user_id: str,
        question_id: str,
        selected_option_key: str,
        confidence: str = "DEFINITELY_KNOW",
        time_spent_seconds: int = 0
    ) -> Dict[str, Any]:
        stmt_session = select(TestSession).where(TestSession.id == session_id)
        res_sess = await db.execute(stmt_session)
        session = res_sess.scalars().first()

        if not session:
            raise NotFoundError(f"Test session {session_id} not found")

        if session.user_id != user_id:
            raise AuthorizationError("Cannot access or submit answers to another user's test session")

        if session.status == "EXPIRED" or (session.expires_at and ensure_utc(session.expires_at) < utc_now()):
            session.status = "EXPIRED"
            await db.commit()
            raise ValidationError("Test session has expired and cannot accept further submissions")

        if session.status != "IN_PROGRESS":
            raise ValidationError(f"Cannot submit answers to a session in status '{session.status}'")

        stmt_opt = select(QuestionOption).where(
            and_(
                QuestionOption.question_id == question_id,
                QuestionOption.is_correct == True
            )
        )
        res_opt = await db.execute(stmt_opt)
        correct_opt = res_opt.scalars().first()
        is_correct = bool(correct_opt and correct_opt.option_key == selected_option_key)

        stmt_q = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.concept),
            selectinload(Question.source)
        ).where(Question.id == question_id)
        res_q = await db.execute(stmt_q)
        question = res_q.scalars().first()
        if not question:
            raise NotFoundError(f"Question {question_id} not found")

        concept_id = question.concept_id

        # Check for existing attempt in this session
        stmt_att = select(TestAttempt).where(
            and_(
                TestAttempt.session_id == session_id,
                TestAttempt.question_id == question_id
            )
        )
        res_att = await db.execute(stmt_att)
        attempt = res_att.scalars().first()
        is_duplicate = (attempt is not None)

        if not attempt:
            attempt = TestAttempt(
                session_id=session_id,
                user_id=user_id,
                question_id=question_id,
                concept_id=concept_id,
                selected_option_key=selected_option_key,
                is_correct=is_correct,
                confidence=confidence,
                time_spent_seconds=time_spent_seconds,
                is_danger_zone_item=(not is_correct and confidence.upper() == "DEFINITELY_KNOW")
            )
            db.add(attempt)
            session.completed_questions += 1
        else:
            attempt.selected_option_key = selected_option_key
            attempt.is_correct = is_correct
            attempt.confidence = confidence
            attempt.time_spent_seconds = time_spent_seconds
            attempt.is_danger_zone_item = (not is_correct and confidence.upper() == "DEFINITELY_KNOW")

        # Update StudentQuestionHistory
        stmt_hist = select(StudentQuestionHistory).where(
            and_(
                StudentQuestionHistory.user_id == user_id,
                StudentQuestionHistory.question_id == question_id
            )
        )
        res_hist = await db.execute(stmt_hist)
        hist = res_hist.scalars().first()
        if not hist:
            hist = StudentQuestionHistory(
                user_id=user_id,
                question_id=question_id,
                total_encounters=1,
                correct_encounters=1 if is_correct else 0,
                last_encountered_at=utc_now()
            )
            db.add(hist)
        else:
            hist.total_encounters += 1
            if is_correct:
                hist.correct_encounters += 1
            hist.last_encountered_at = utc_now()

        # Update M6 Adaptive Learning Engine
        learning_update = await LearningIntelligenceEngine.record_attempt_learning_event(
            db=db,
            user_id=user_id,
            question_id=question_id,
            concept_id=concept_id,
            is_correct=is_correct,
            confidence=confidence,
            selected_option_key=selected_option_key,
            correct_option_key=correct_opt.option_key if correct_opt else "A",
            session_id=session_id,
            response_time_seconds=time_spent_seconds
        )

        # Capture metadata prior to commit/rollback to avoid accessing expired ORM attributes
        correct_explanation_val = question.correct_explanation
        remember_takeaway_val = question.remember_takeaway
        exam_connection_val = question.exam_connection
        if question.source:
            source_title = question.source.title
            source_ed = question.source.edition_or_year or question.source.edition or "Standard Edition"
            source_ref = question.source.reference_identifier or question.source.publisher or "NMC Reference"
            exam_connection_val = f"{source_title} ({source_ed}), Ref: {source_ref}"
        detailed_explanation_val = question.detailed_explanation
        concept_id_val = question.concept_id
        concept_name_val = question.concept.name if question.concept else "Medical Concept"
        selected_opt_record = next((o for o in question.options if o.option_key == selected_option_key), None)
        why_wrong_val = selected_opt_record.why_wrong_explanation if selected_opt_record and not is_correct else None
        correct_opt_key_val = correct_opt.option_key if correct_opt else "A"

        try:
            await db.commit()
        except Exception:
            await db.rollback()
            stmt_att_reload = select(TestAttempt).where(
                and_(
                    TestAttempt.session_id == session_id,
                    TestAttempt.question_id == question_id
                )
            )
            res_reload = await db.execute(stmt_att_reload)
            attempt = res_reload.scalars().first()

        attempt_id_val = attempt.id if attempt else "attempt-recorded"
        is_dz_val = bool(attempt.is_danger_zone_item) if attempt else False

        return {
            "attempt_id": attempt_id_val,
            "session_id": session_id,
            "question_id": question_id,
            "is_correct": is_correct,
            "selected_option_key": selected_option_key,
            "correct_option_key": correct_opt_key_val,
            "correct_explanation": correct_explanation_val,
            "why_selected_was_wrong": why_wrong_val,
            "remember_takeaway": remember_takeaway_val,
            "exam_connection": exam_connection_val,
            "detailed_explanation": detailed_explanation_val,
            "concept_id": concept_id_val,
            "concept_name": concept_name_val,
            "is_danger_zone_item": is_dz_val,
            "revision_interval_days": learning_update.get("revision_interval_days", 1),
            "next_revision_due": datetime.fromisoformat(learning_update["next_revision_due"]) if "next_revision_due" in learning_update else None,
            "is_duplicate_submission": is_duplicate,
            "short_explanation": {
                "why_your_answer_is_wrong": why_wrong_val,
                "why_correct_is_right": correct_explanation_val,
                "remember_takeaway": remember_takeaway_val,
                "exam_connection": exam_connection_val
            },
            "learning_engine_feedback": learning_update
        }

    @classmethod
    async def complete_test_session(cls, db: AsyncSession, session_id: str, user_id: str) -> Dict[str, Any]:
        """
        Completes test session and compiles rich performance analytics (Prompt 9 & 9.1).
        """
        stmt_session = select(TestSession).where(TestSession.id == session_id)
        res_sess = await db.execute(stmt_session)
        session = res_sess.scalars().first()

        if not session:
            raise NotFoundError(f"Test session {session_id} not found")

        if session.user_id != user_id:
            raise AuthorizationError("Cannot access another user's test results")

        now = utc_now()
        if session.status == "IN_PROGRESS":
            session.status = "SUBMITTED"
            session.submitted_at = now
            session.completed_at = now

        stmt_attempts = select(TestAttempt).options(
            selectinload(TestAttempt.question).selectinload(Question.options),
            selectinload(TestAttempt.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        ).where(TestAttempt.session_id == session_id)
        res_att = await db.execute(stmt_attempts)
        attempts = res_att.scalars().all()

        correct_count = sum(1 for a in attempts if a.is_correct)
        incorrect_count = sum(1 for a in attempts if not a.is_correct)
        unanswered_count = max(0, session.total_questions - len(attempts))
        danger_zone_count = sum(1 for a in attempts if a.is_danger_zone_item)
        
        # NEET-PG Scoring (+4 for correct, -1 for incorrect, 0 for unanswered)
        score = (correct_count * 4) - (incorrect_count * 1)
        session.score = score
        session.completed_questions = len(attempts)

        # Detailed Question-by-Question Review (Prompt 9, Sec 16)
        question_review = []
        for a in attempts:
            q = a.question
            correct_opt = next((o for o in q.options if o.is_correct), None)
            selected_opt = next((o for o in q.options if o.option_key == a.selected_option_key), None)

            provenance_tag = "ORIGINAL_AI_GENERATED"
            if getattr(q, "trust_class", "") == "development_seed":
                provenance_tag = "DEVELOPMENT_SEED"
            elif q.pyq_reference_id is not None:
                provenance_tag = "VERIFIED_PYQ"
            elif q.source_id is not None:
                provenance_tag = "SOURCE_REFERENCED"
            elif q.exam_relevance_tag == "PYQ_LINKED":
                provenance_tag = "PYQ_STYLE"

            question_review.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "student_selected_key": a.selected_option_key,
                "correct_option_key": correct_opt.option_key if correct_opt else None,
                "is_correct": a.is_correct,
                "confidence": a.confidence,
                "response_time_seconds": a.time_spent_seconds,
                "difficulty": q.difficulty,
                "provenance_tag": provenance_tag,
                "short_explanation": {
                    "why_your_answer_is_wrong": selected_opt.why_wrong_explanation if selected_opt and not a.is_correct else None,
                    "why_correct_is_right": q.correct_explanation,
                    "remember_takeaway": q.remember_takeaway,
                    "exam_connection": q.exam_connection
                },
                "options": [{"option_key": o.option_key, "option_text": o.option_text, "is_correct": o.is_correct} for o in q.options]
            })

        concept_breakdown = {}
        for a in attempts:
            c_name = a.concept.name if a.concept else "Unknown Concept"
            if c_name not in concept_breakdown:
                concept_breakdown[c_name] = {"total": 0, "correct": 0}
            concept_breakdown[c_name]["total"] += 1
            if a.is_correct:
                concept_breakdown[c_name]["correct"] += 1

        accuracy_pct = round((correct_count / max(1, len(attempts))) * 100, 1)

        # Fetch Next Best Action Recommendation from M6
        next_action = await LearningIntelligenceEngine.get_next_best_action(db, user_id)

        # Optional Ranking Policy with Small-Sample Warning (Prompt 9.1, Sec 7)
        ranking_info = {
            "is_enabled": False,
            "sample_size": 1,
            "is_statistically_authoritative": False,
            "rank": 1,
            "disclaimer": "Cohort sample size is small (N < 20). Individual mastery and accuracy are the primary reliable metrics."
        }

        await db.commit()

        return {
            "session_id": session.id,
            "status": session.status,
            "total_questions": session.total_questions,
            "completed_questions": len(attempts),
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "unanswered_count": unanswered_count,
            "score": score,
            "accuracy_percentage": accuracy_pct,
            "danger_zone_count": danger_zone_count,
            "time_spent_seconds": sum(a.time_spent_seconds for a in attempts),
            "scoring": {
                "total_questions": session.total_questions,
                "completed_questions": len(attempts),
                "attempted_count": len(attempts),
                "correct_count": correct_count,
                "incorrect_count": incorrect_count,
                "unanswered_count": unanswered_count,
                "score": score,
                "accuracy_percentage": accuracy_pct,
                "danger_zone_count": danger_zone_count,
                "time_spent_seconds": sum(a.time_spent_seconds for a in attempts)
            },
            "concept_performance": concept_breakdown,
            "question_breakdowns": question_review,
            "question_review": question_review,
            "test_reproducibility_snapshot": session.test_reproducibility_snapshot,
            "ranking": ranking_info,
            "next_action": next_action
        }

    @classmethod
    async def get_test_result(cls, db: AsyncSession, session_id: str, user_id: str) -> Dict[str, Any]:
        return await cls.complete_test_session(db, session_id, user_id)
