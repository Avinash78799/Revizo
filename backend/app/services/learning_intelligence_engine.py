import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.learning import StudentConceptMastery, StudentMistakeRecord, DailyStudyPlan, RevisionSchedule, LearningEvidenceRecord
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.question import Question
from app.models.test import TestAttempt, TestSession
from app.core.datetime_util import utc_now, ensure_utc
from app.core.errors import NotFoundError

class LearningIntelligenceEngine:
    """
    Adaptive Learning, Spaced Revision & Student Intelligence Engine (Prompt 8 & 8.1).
    100% Deterministic Backend Intelligence:
    - Bayesian-smoothed concept mastery & statistical confidence intervals
    - Configurable Interpretable Mastery States (UNSEEN, INTRODUCED, WEAK, FRAGILE, DEVELOPING, STABLE, STRONG, MASTERED)
    - Misconception State Progression (CONFIDENCE_ERROR -> SUSPECTED_MISCONCEPTION -> CONFIRMED_MISCONCEPTION -> DANGER_ZONE)
    - Clinical-Confidence-Modified SM-2 Spaced Repetition
    - Idempotency & Invalidation Protection (Quarantined questions do not poison mastery)
    - Top-Bottom Quartile Discrimination ($D = P_{top} - P_{bottom}$) & Observed Error Rate
    - Dynamic 5-Minute Micro-Revision Slices with Explainable Selection Reasons
    - Configurable Daily Study Plan Allocations
    - Transparent Next-Best-Action Clinical Prioritization
    """

    ALGORITHM_VERSION = "adaptive-v1.0"
    ALLOCATION_STRATEGY_VERSION = "daily-alloc-v1.0"

    # Configurable Mastery Thresholds (Prompt 8, Sec 4)
    MASTERY_THRESHOLDS = {
        "WEAK_CEILING": 0.40,
        "DEVELOPING_CEILING": 0.65,
        "STABLE_CEILING": 0.85,
        "STRONG_CEILING": 0.95,
        "MASTERED_MIN_ATTEMPTS": 5
    }

    # Configurable Default Daily Plan Distribution Weights (Prompt 8.1, Sec 5)
    DEFAULT_DAILY_ALLOCATION_WEIGHTS = {
        "danger_zone": 0.30,
        "due_revisions": 0.30,
        "weak_concepts": 0.25,
        "discovery": 0.15
    }

    @classmethod
    def compute_mastery_state(
        cls,
        total_attempts: int,
        smoothed_score: float,
        high_conf_wrong: int,
        lucky_guesses: int,
        danger_zone_active: bool
    ) -> str:
        if total_attempts == 0:
            return "UNSEEN"
        if total_attempts == 1:
            return "INTRODUCED"
        if danger_zone_active or high_conf_wrong >= 2:
            return "FRAGILE"
        if smoothed_score < cls.MASTERY_THRESHOLDS["WEAK_CEILING"]:
            return "WEAK"
        if smoothed_score >= 0.70 and lucky_guesses >= int(total_attempts * 0.4) and lucky_guesses > 0:
            return "FRAGILE"
        if total_attempts >= cls.MASTERY_THRESHOLDS["MASTERED_MIN_ATTEMPTS"] and smoothed_score >= 0.80 and not danger_zone_active:
            return "MASTERED"
        if smoothed_score >= cls.MASTERY_THRESHOLDS["STABLE_CEILING"]:
            return "STRONG"
        if smoothed_score >= cls.MASTERY_THRESHOLDS["DEVELOPING_CEILING"]:
            return "STABLE"
        return "DEVELOPING"

    @classmethod
    def compute_misconception_state(cls, high_conf_wrong_count: int) -> str:
        """
        Misconception State Progression (Prompt 8.1, Sec 1):
        0 confident mistakes -> NONE
        1 confident mistake  -> SUSPECTED_MISCONCEPTION (Confidence Error recorded, NOT confirmed)
        >= 2 confident mistakes -> CONFIRMED_MISCONCEPTION / DANGER_ZONE
        """
        if high_conf_wrong_count == 0:
            return "NONE"
        if high_conf_wrong_count == 1:
            return "SUSPECTED_MISCONCEPTION"
        return "CONFIRMED_MISCONCEPTION"

    @classmethod
    async def record_attempt_learning_event(
        cls,
        db: AsyncSession,
        user_id: str,
        question_id: str,
        concept_id: str,
        is_correct: bool,
        confidence: str,  # 'DEFINITELY_KNOW', 'SOMEWHAT_CONFIDENT', 'GUESSING'
        selected_option_key: str,
        correct_option_key: str,
        session_id: Optional[str] = None,
        response_time_seconds: int = 0
    ) -> Dict[str, Any]:
        """
        Idempotent Learning Event Processor.
        Prevents double-counting on network retries and updates statistical mastery models.
        """
        now = utc_now()
        conf_norm = confidence.upper()
        idempotency_key = f"{user_id}:{session_id or 'direct'}:{question_id}:{selected_option_key}"

        # 1. Idempotency Check: Verify if event was already recorded
        stmt_dup = select(LearningEvidenceRecord).where(LearningEvidenceRecord.idempotency_key == idempotency_key)
        res_dup = await db.execute(stmt_dup)
        existing_event = res_dup.scalars().first()

        if existing_event:
            stmt_m = select(StudentConceptMastery).where(
                and_(
                    StudentConceptMastery.user_id == user_id,
                    StudentConceptMastery.concept_id == concept_id
                )
            )
            mastery = (await db.execute(stmt_m)).scalars().first()
            return {
                "idempotent_replay": True,
                "concept_id": concept_id,
                "mastery_percentage": mastery.mastery_percentage if mastery else 0.0,
                "mastery_state": mastery.mastery_state if mastery else "UNSEEN",
                "misconception_state": mastery.misconception_state if mastery else "NONE",
                "danger_zone_active": mastery.danger_zone_active if mastery else False
            }

        # 2. Fetch or Initialize StudentConceptMastery
        stmt_m = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.concept_id == concept_id
            )
        )
        res_m = await db.execute(stmt_m)
        mastery = res_m.scalars().first()

        if not mastery:
            mastery = StudentConceptMastery(
                user_id=user_id,
                concept_id=concept_id,
                total_attempts=0,
                correct_attempts=0,
                wrong_count=0,
                high_confidence_wrong_count=0,
                lucky_guess_count=0,
                ease_factor=2.50,
                revision_interval_days=1,
                consecutive_correct_count=0,
                algorithm_version=cls.ALGORITHM_VERSION
            )
            db.add(mastery)



        mastery.total_attempts += 1
        if is_correct:
            mastery.correct_attempts += 1
            if conf_norm == "GUESSING":
                mastery.lucky_guess_count += 1
        else:
            mastery.wrong_count += 1
            if conf_norm == "DEFINITELY_KNOW":
                mastery.high_confidence_wrong_count += 1

        # Misconception State Progression & Danger Zone Activation Rule (>= 2 confident errors)
        mastery.misconception_state = cls.compute_misconception_state(mastery.high_confidence_wrong_count)
        if mastery.high_confidence_wrong_count >= 2:
            mastery.danger_zone_active = True
        elif is_correct and mastery.danger_zone_active and conf_norm == "DEFINITELY_KNOW":
            if mastery.high_confidence_wrong_count > 0:
                mastery.high_confidence_wrong_count -= 1
            mastery.misconception_state = cls.compute_misconception_state(mastery.high_confidence_wrong_count)
            if mastery.high_confidence_wrong_count < 2:
                mastery.danger_zone_active = False

        # Statistical Calculations: Bayesian Beta Prior & Uncertainty
        mastery.mastery_percentage = round((float(mastery.correct_attempts) / float(mastery.total_attempts) * 100), 1)
        mastery.smoothed_mastery_score = round(float(mastery.correct_attempts + 1) / float(mastery.total_attempts + 2), 3)
        mastery.confidence_interval_width = round(1.0 / math.sqrt(mastery.total_attempts + 1), 3)
        mastery.is_cold_start = (mastery.total_attempts < 3)
        mastery.mastery_state = cls.compute_mastery_state(
            total_attempts=mastery.total_attempts,
            smoothed_score=mastery.smoothed_mastery_score,
            high_conf_wrong=mastery.high_confidence_wrong_count,
            lucky_guesses=mastery.lucky_guess_count,
            danger_zone_active=mastery.danger_zone_active
        )

        # 4. Spaced Repetition (Modified SM-2 with Clinical Confidence)
        if not is_correct:
            if conf_norm == "DEFINITELY_KNOW":
                mastery.ease_factor = max(1.30, mastery.ease_factor - 0.30)
                mastery.revision_interval_days = 1
                mastery.consecutive_correct_count = 0
            else:
                mastery.ease_factor = max(1.30, mastery.ease_factor - 0.15)
                mastery.revision_interval_days = 1
                mastery.consecutive_correct_count = 0
        else:
            if conf_norm == "GUESSING":
                mastery.revision_interval_days = 1
                mastery.consecutive_correct_count = 1
            elif conf_norm == "SOMEWHAT_CONFIDENT":
                mastery.consecutive_correct_count += 1
                if mastery.consecutive_correct_count == 1:
                    mastery.revision_interval_days = 2
                else:
                    mastery.revision_interval_days = min(30, max(2, int(round(mastery.revision_interval_days * 1.5))))
            else:  # DEFINITELY_KNOW
                mastery.consecutive_correct_count += 1
                mastery.ease_factor = min(3.0, mastery.ease_factor + 0.10)
                if mastery.consecutive_correct_count == 1:
                    mastery.revision_interval_days = 1
                elif mastery.consecutive_correct_count == 2:
                    mastery.revision_interval_days = 6
                else:
                    mastery.revision_interval_days = min(180, max(6, int(round(mastery.revision_interval_days * mastery.ease_factor))))

        mastery.last_practiced_at = now
        mastery.next_revision_due = now + timedelta(days=mastery.revision_interval_days)

        # 5. Mistake Record & Error Taxonomy
        if not is_correct:
            stmt_mistake = select(StudentMistakeRecord).where(
                and_(
                    StudentMistakeRecord.user_id == user_id,
                    StudentMistakeRecord.question_id == question_id
                )
            )
            res_mistake = await db.execute(stmt_mistake)
            mistake = res_mistake.scalars().first()

            if mastery.smoothed_mastery_score >= 0.75 and response_time_seconds > 0 and response_time_seconds < 15 and conf_norm != "DEFINITELY_KNOW":
                error_type = "SPEED_SILLY_MISTAKE"
            elif conf_norm == "DEFINITELY_KNOW":
                error_type = "CONFIDENCE_ERROR"
            else:
                error_type = "FACTUAL_KNOWLEDGE_GAP"

            misconception_st = "CONFIRMED_MISCONCEPTION" if mastery.high_confidence_wrong_count >= 2 else ("SUSPECTED_MISCONCEPTION" if conf_norm == "DEFINITELY_KNOW" else "NOT_APPLICABLE")

            if not mistake:
                mistake = StudentMistakeRecord(
                    user_id=user_id,
                    question_id=question_id,
                    concept_id=concept_id,
                    session_id=session_id,
                    selected_option_key=selected_option_key,
                    correct_option_key=correct_option_key,
                    confidence_level=conf_norm,
                    error_type=error_type,
                    misconception_state=misconception_st,
                    status="UNRESOLVED",
                    occurrence_count=1
                )
                db.add(mistake)
            else:
                mistake.occurrence_count += 1
                mistake.last_occurred_at = now
                mistake.confidence_level = conf_norm
                mistake.selected_option_key = selected_option_key
                mistake.misconception_state = misconception_st
                mistake.status = "UNRESOLVED"
        else:
            stmt_mistake = select(StudentMistakeRecord).where(
                and_(
                    StudentMistakeRecord.user_id == user_id,
                    StudentMistakeRecord.question_id == question_id,
                    StudentMistakeRecord.status == "UNRESOLVED"
                )
            )
            res_mistake = await db.execute(stmt_mistake)
            mistake = res_mistake.scalars().first()
            if mistake and conf_norm == "DEFINITELY_KNOW":
                mistake.status = "RESOLVED_ON_RETEST"
                mistake.resolved_at = now

        # 6. Question Empirical Calibration (Observed Error Rate)
        stmt_q = select(Question).where(Question.id == question_id)
        res_q = await db.execute(stmt_q)
        question = res_q.scalars().first()
        if question:
            question.total_attempts_count = (question.total_attempts_count or 0) + 1
            if is_correct:
                question.correct_attempts_count = (question.correct_attempts_count or 0) + 1
            if question.total_attempts_count >= 5:
                # Raw observed error rate (Prompt 8.1, Sec 3)
                question.observed_difficulty_score = round(1.0 - (float(question.correct_attempts_count) / float(question.total_attempts_count)), 2)

        # Record Immutable Learning Evidence
        evidence = LearningEvidenceRecord(
            idempotency_key=idempotency_key,
            user_id=user_id,
            question_id=question_id,
            concept_id=concept_id,
            attempt_id=session_id,
            is_correct=is_correct,
            confidence=conf_norm,
            response_time_seconds=response_time_seconds,
            algorithm_version=cls.ALGORITHM_VERSION
        )
        db.add(evidence)

        return {
            "idempotent_replay": False,
            "concept_id": concept_id,
            "mastery_percentage": mastery.mastery_percentage,
            "smoothed_mastery_score": mastery.smoothed_mastery_score,
            "mastery_state": mastery.mastery_state,
            "misconception_state": mastery.misconception_state,
            "danger_zone_active": mastery.danger_zone_active,
            "is_cold_start": mastery.is_cold_start,
            "next_revision_due": mastery.next_revision_due.isoformat(),
            "revision_interval_days": mastery.revision_interval_days,
            "ease_factor": round(mastery.ease_factor, 2)
        }

    @classmethod
    async def invalidate_question_evidence_and_recalculate_mastery(
        cls,
        db: AsyncSession,
        question_id: str
    ) -> int:
        """
        Question Quality Protection (Prompt 8 & 8.1).
        Marks all learning evidence for an invalidated question as is_invalidated=True
        and recomputes affected student mastery scores without the corrupted evidence.
        """
        stmt_ev = select(LearningEvidenceRecord).where(LearningEvidenceRecord.question_id == question_id)
        res_ev = await db.execute(stmt_ev)
        records = res_ev.scalars().all()

        affected_user_concepts = set()
        for r in records:
            r.is_invalidated = True
            affected_user_concepts.add((r.user_id, r.concept_id))

        for u_id, c_id in affected_user_concepts:
            stmt_valid = select(LearningEvidenceRecord).where(
                and_(
                    LearningEvidenceRecord.user_id == u_id,
                    LearningEvidenceRecord.concept_id == c_id,
                    LearningEvidenceRecord.is_invalidated == False
                )
            )
            res_valid = await db.execute(stmt_valid)
            valid_evidence = res_valid.scalars().all()

            stmt_m = select(StudentConceptMastery).where(
                and_(
                    StudentConceptMastery.user_id == u_id,
                    StudentConceptMastery.concept_id == c_id
                )
            )
            res_m = await db.execute(stmt_m)
            mastery = res_m.scalars().first()

            if mastery:
                valid_total = len(valid_evidence)
                valid_correct = sum(1 for e in valid_evidence if e.is_correct)
                valid_high_conf_wrong = sum(1 for e in valid_evidence if not e.is_correct and e.confidence == "DEFINITELY_KNOW")
                valid_lucky = sum(1 for e in valid_evidence if e.is_correct and e.confidence == "GUESSING")

                mastery.total_attempts = valid_total
                mastery.correct_attempts = valid_correct
                mastery.wrong_count = valid_total - valid_correct
                mastery.high_confidence_wrong_count = valid_high_conf_wrong
                mastery.lucky_guess_count = valid_lucky
                mastery.misconception_state = cls.compute_misconception_state(valid_high_conf_wrong)
                mastery.danger_zone_active = (valid_high_conf_wrong >= 2)

                mastery.mastery_percentage = round((float(valid_correct) / float(valid_total) * 100), 1) if valid_total > 0 else 0.0
                mastery.smoothed_mastery_score = round(float(valid_correct + 1) / float(valid_total + 2), 3)
                mastery.is_cold_start = (valid_total < 3)
                mastery.mastery_state = cls.compute_mastery_state(
                    total_attempts=valid_total,
                    smoothed_score=mastery.smoothed_mastery_score,
                    high_conf_wrong=valid_high_conf_wrong,
                    lucky_guesses=valid_lucky,
                    danger_zone_active=mastery.danger_zone_active
                )

        await db.flush()
        return len(records)

    @classmethod
    async def calculate_question_discrimination(
        cls,
        db: AsyncSession,
        question_id: str
    ) -> Dict[str, Any]:
        """
        Calculates empirical Top-Bottom Quartile Discrimination (Prompt 8.1, Sec 2).
        D = P(correct | Top Quartile) - P(correct | Bottom Quartile).
        """
        stmt_q = select(Question).where(Question.id == question_id)
        res_q = await db.execute(stmt_q)
        q = res_q.scalars().first()

        if not q or (q.total_attempts_count or 0) < 10:
            return {
                "question_id": question_id,
                "status": "INSUFFICIENT_SAMPLE_SIZE",
                "sample_size": q.total_attempts_count if q else 0,
                "message": "Minimum 10 student attempts required to compute top-bottom quartile discrimination."
            }

        stmt_att = select(TestAttempt).options(selectinload(TestAttempt.session)).where(TestAttempt.question_id == question_id)
        res_att = await db.execute(stmt_att)
        attempts = res_att.scalars().all()

        if len(attempts) < 10:
            return {"question_id": question_id, "status": "INSUFFICIENT_SAMPLE_SIZE", "sample_size": len(attempts)}

        sorted_attempts = sorted(attempts, key=lambda a: a.session.score if a.session else 0, reverse=True)
        quartile_size = max(1, len(sorted_attempts) // 4)

        top_quartile = sorted_attempts[:quartile_size]
        bottom_quartile = sorted_attempts[-quartile_size:]

        top_correct_rate = float(sum(1 for a in top_quartile if a.is_correct)) / float(len(top_quartile))
        bottom_correct_rate = float(sum(1 for a in bottom_quartile if a.is_correct)) / float(len(bottom_quartile))

        quartile_discrimination = round(top_correct_rate - bottom_correct_rate, 2)
        q.discrimination_index = quartile_discrimination
        await db.flush()

        return {
            "question_id": question_id,
            "status": "CALCULATED",
            "metric_name": "TOP_BOTTOM_QUARTILE_DISCRIMINATION",
            "sample_size": len(attempts),
            "observed_error_rate": q.observed_difficulty_score,
            "top_bottom_quartile_discrimination": quartile_discrimination,
            "quality_rating": "EXCELLENT" if quartile_discrimination >= 0.40 else "GOOD" if quartile_discrimination >= 0.20 else "WEAK_OR_AMBIGUOUS"
        }

    @classmethod
    async def get_confidence_calibration(cls, db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """
        Calculates student confidence calibration metrics (Prompt 8, Sec 17).
        """
        stmt = select(LearningEvidenceRecord).where(
            and_(
                LearningEvidenceRecord.user_id == user_id,
                LearningEvidenceRecord.is_invalidated == False
            )
        )
        res = await db.execute(stmt)
        records = res.scalars().all()

        if len(records) < 5:
            return {
                "status": "INSUFFICIENT_DATA",
                "sample_size": len(records),
                "message": "Complete at least 5 questions to view confidence calibration."
            }

        high_conf = [r for r in records if r.confidence == "DEFINITELY_KNOW"]
        mod_conf = [r for r in records if r.confidence == "SOMEWHAT_CONFIDENT"]
        low_conf = [r for r in records if r.confidence == "GUESSING"]

        high_acc = round(float(sum(1 for r in high_conf if r.is_correct)) / float(len(high_conf)) * 100, 1) if high_conf else 0.0
        mod_acc = round(float(sum(1 for r in mod_conf if r.is_correct)) / float(len(mod_conf)) * 100, 1) if mod_conf else 0.0
        low_acc = round(float(sum(1 for r in low_conf if r.is_correct)) / float(len(low_conf)) * 100, 1) if low_conf else 0.0

        calibration_gap = round(100.0 - high_acc, 1) if high_conf else 0.0

        if high_acc >= 90.0:
            feedback = "Excellent clinical confidence calibration. Your high-confidence answers are highly reliable."
        elif high_acc >= 75.0:
            feedback = "Good calibration, with occasional misconceptions in specific subtopics."
        else:
            feedback = f"Overconfidence alert: When marking 'Definitely Know', accuracy was {high_acc}%. Review your Danger Zone misconceptions."

        return {
            "status": "CALIBRATED",
            "sample_size": len(records),
            "breakdown": {
                "definitely_know": {"count": len(high_conf), "accuracy_percentage": high_acc},
                "somewhat_confident": {"count": len(mod_conf), "accuracy_percentage": mod_acc},
                "guessing": {"count": len(low_conf), "accuracy_percentage": low_acc}
            },
            "calibration_gap_percentage": calibration_gap,
            "feedback": feedback
        }

    @classmethod
    async def get_danger_zone_concepts(cls, db: AsyncSession, user_id: str) -> List[Dict[str, Any]]:
        stmt = select(StudentConceptMastery).options(
            selectinload(StudentConceptMastery.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        ).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.high_confidence_wrong_count >= 1
            )
        ).order_by(desc(StudentConceptMastery.high_confidence_wrong_count))
        
        res = await db.execute(stmt)
        records = res.scalars().all()

        results = []
        for r in records:
            c = r.concept
            subject_name = c.topic.chapter.subject.name if (c and c.topic and c.topic.chapter and c.topic.chapter.subject) else "Subject"
            topic_name = c.topic.name if (c and c.topic) else "Topic"

            results.append({
                "concept_id": r.concept_id,
                "concept_name": c.name if c else "Concept",
                "subject_name": subject_name,
                "topic_name": topic_name,
                "high_confidence_wrong_count": r.high_confidence_wrong_count,
                "total_attempts": r.total_attempts,
                "mastery_percentage": r.mastery_percentage,
                "mastery_state": r.mastery_state,
                "misconception_state": r.misconception_state,
                "danger_zone_active": r.danger_zone_active,
                "clinical_pearl": c.clinical_pearl if c else None,
                "last_practiced_at": r.last_practiced_at.isoformat() if r.last_practiced_at else None,
                "why_danger_zone": f"Answered incorrectly with definite clinical confidence ({r.high_confidence_wrong_count} time(s))."
            })
        return results

    @classmethod
    async def get_due_spaced_revisions(cls, db: AsyncSession, user_id: str) -> List[Dict[str, Any]]:
        now = utc_now()
        stmt = select(StudentConceptMastery).options(
            selectinload(StudentConceptMastery.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        ).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.next_revision_due <= now
            )
        ).order_by(StudentConceptMastery.next_revision_due.asc())

        res = await db.execute(stmt)
        records = res.scalars().all()

        results = []
        for r in records:
            c = r.concept
            subject_name = c.topic.chapter.subject.name if (c and c.topic and c.topic.chapter and c.topic.chapter.subject) else "Subject"
            topic_name = c.topic.name if (c and c.topic) else "Topic"
            days_overdue = (now - ensure_utc(r.next_revision_due)).days

            results.append({
                "concept_id": r.concept_id,
                "concept_name": c.name if c else "Concept",
                "subject_name": subject_name,
                "topic_name": topic_name,
                "next_revision_due": r.next_revision_due.isoformat(),
                "days_overdue": max(0, days_overdue),
                "interval_days": r.revision_interval_days,
                "mastery_percentage": r.mastery_percentage,
                "mastery_state": r.mastery_state,
                "misconception_state": r.misconception_state,
                "danger_zone_active": r.danger_zone_active
            })
        return results

    @classmethod
    async def generate_daily_study_plan(
        cls,
        db: AsyncSession,
        user_id: str,
        target_questions: int = 20
    ) -> Dict[str, Any]:
        now = utc_now()
        target_date_str = now.strftime("%Y-%m-%d")

        stmt_p = select(DailyStudyPlan).where(
            and_(
                DailyStudyPlan.user_id == user_id,
                DailyStudyPlan.target_date == target_date_str
            )
        )
        res_p = await db.execute(stmt_p)
        plan = res_p.scalars().first()

        danger_zone_items = await cls.get_danger_zone_concepts(db, user_id)
        due_revision_items = await cls.get_due_spaced_revisions(db, user_id)

        stmt_weak = select(StudentConceptMastery).options(
            selectinload(StudentConceptMastery.concept)
        ).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.smoothed_mastery_score < 0.60,
                StudentConceptMastery.danger_zone_active == False
            )
        ).limit(5)
        res_weak = await db.execute(stmt_weak)
        weak_records = res_weak.scalars().all()
        weak_items = [{"concept_id": w.concept_id, "concept_name": w.concept.name if w.concept else "Concept", "smoothed_mastery": w.smoothed_mastery_score} for w in weak_records]

        stmt_attempted = select(StudentConceptMastery.concept_id).where(StudentConceptMastery.user_id == user_id)
        attempted_ids = (await db.execute(stmt_attempted)).scalars().all()

        stmt_disc = select(Concept).where(
            and_(
                Concept.exam_relevance_score >= 0.70,
                ~Concept.id.in_(attempted_ids) if attempted_ids else True
            )
        ).limit(5)
        res_disc = await db.execute(stmt_disc)
        disc_records = res_disc.scalars().all()
        disc_items = [{"concept_id": d.id, "concept_name": d.name, "exam_relevance_score": d.exam_relevance_score} for d in disc_records]

        if not plan:
            plan = DailyStudyPlan(
                user_id=user_id,
                target_date=target_date_str,
                total_target_questions=target_questions,
                danger_zone_slice={"items": danger_zone_items[:5]},
                due_revision_slice={"items": due_revision_items[:6]},
                weak_subject_slice={"items": weak_items[:5]},
                discovery_slice={"items": disc_items[:4]},
                status="GENERATED",
                algorithm_version=cls.ALGORITHM_VERSION,
                allocation_strategy_version=cls.ALLOCATION_STRATEGY_VERSION
            )
            db.add(plan)
            await db.commit()
            await db.refresh(plan)

        return {
            "plan_id": plan.id,
            "target_date": plan.target_date,
            "total_target_questions": plan.total_target_questions,
            "completed_questions": plan.completed_questions_count,
            "status": plan.status,
            "algorithm_version": plan.algorithm_version,
            "allocation_strategy_version": plan.allocation_strategy_version,
            "slices": {
                "danger_zone": danger_zone_items[:5],
                "due_revisions": due_revision_items[:6],
                "weak_concepts": weak_items[:5],
                "discovery_concepts": disc_items[:4]
            },
            "summary": {
                "danger_zone_count": len(danger_zone_items),
                "due_revisions_count": len(due_revision_items),
                "weak_concepts_count": len(weak_items),
                "discovery_count": len(disc_items)
            }
        }

    @classmethod
    async def get_five_minute_revision_slice(cls, db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """
        Dynamic 5-Minute Micro-Revision Session (Prompt 8.1, Sec 4).
        Dynamically adjusts to available data: does NOT manufacture false Danger Zone questions.
        Pulls from Danger Zone -> Due Spaced Revisions -> Weak Concepts -> High-Yield Diagnostic.
        """
        danger = await cls.get_danger_zone_concepts(db, user_id)
        due = await cls.get_due_spaced_revisions(db, user_id)

        target_items = []
        # Dynamic allocation: take available Danger Zone concepts
        for item in danger[:3]:
            target_items.append({
                "concept_id": item["concept_id"],
                "reason": "Resolve High-Priority Misconception",
                "priority": "CRITICAL"
            })
        # Take available Due Spaced Revisions
        for item in due[:3]:
            if not any(t["concept_id"] == item["concept_id"] for t in target_items):
                target_items.append({
                    "concept_id": item["concept_id"],
                    "reason": f"Spaced Revision Due ({item['days_overdue']} days overdue)",
                    "priority": "HIGH"
                })

        # Fetch questions under targeted concepts
        selected_questions = []
        for target in target_items:
            stmt_q = select(Question).options(selectinload(Question.options), selectinload(Question.concept)).where(
                and_(
                    Question.concept_id == target["concept_id"],
                    Question.status.in_(["PUBLISHED", "published", "APPROVED", "approved"])
                )
            ).limit(1)
            q = (await db.execute(stmt_q)).scalars().first()
            if q and not any(sq["question_id"] == q.id for sq in selected_questions):
                selected_questions.append({
                    "question_id": q.id,
                    "concept_id": q.concept_id,
                    "concept_name": q.concept.name if q.concept else "Medical Concept",
                    "question_text": q.question_text,
                    "difficulty": q.difficulty,
                    "selection_reason": target["reason"],
                    "priority": target["priority"],
                    "estimated_time_minutes": 1,
                    "options": [{"option_key": o.option_key, "option_text": o.option_text} for o in q.options]
                })
            if len(selected_questions) >= 5:
                break

        # If pool still has capacity, backfill with high-yield core questions
        if len(selected_questions) < 5:
            existing_ids = [sq["question_id"] for sq in selected_questions]
            stmt_fill = select(Question).options(selectinload(Question.options), selectinload(Question.concept)).where(
                and_(
                    Question.status.in_(["PUBLISHED", "published", "APPROVED", "approved"]),
                    ~Question.id.in_(existing_ids) if existing_ids else True
                )
            ).limit(5 - len(selected_questions))
            fill_qs = (await db.execute(stmt_fill)).scalars().all()
            for q in fill_qs:
                selected_questions.append({
                    "question_id": q.id,
                    "concept_id": q.concept_id,
                    "concept_name": q.concept.name if q.concept else "Medical Concept",
                    "question_text": q.question_text,
                    "difficulty": q.difficulty,
                    "selection_reason": "High-Yield Core Diagnostic Review",
                    "priority": "STANDARD",
                    "estimated_time_minutes": 1,
                    "options": [{"option_key": o.option_key, "option_text": o.option_text} for o in q.options]
                })

        return {
            "session_type": "FIVE_MINUTE_RAPID_REVISION",
            "total_questions": len(selected_questions),
            "estimated_duration_minutes": max(1, len(selected_questions)),
            "algorithm_version": cls.ALGORITHM_VERSION,
            "target_misconceptions_included": sum(1 for q in selected_questions if q["priority"] == "CRITICAL"),
            "questions": selected_questions
        }

    @classmethod
    async def get_next_best_action(cls, db: AsyncSession, user_id: str) -> Dict[str, Any]:
        """
        Explainable Next-Best-Action Engine (Prompt 8 & 8.1).
        Exposes transparent, auditable educational reasons.
        """
        danger = await cls.get_danger_zone_concepts(db, user_id)
        # Check for confirmed Danger Zone misconceptions (>= 2 errors)
        confirmed_danger = [d for d in danger if d.get("danger_zone_active", False) or d.get("high_confidence_wrong_count", 0) >= 2]
        if confirmed_danger:
            top_danger = confirmed_danger[0]
            return {
                "action_type": "RESOLVE_DANGER_ZONE_MISCONCEPTION",
                "priority": "CRITICAL",
                "title": f"Resolve Misconception: {top_danger['concept_name']}",
                "description": f"Prioritized because:\n- {top_danger['high_confidence_wrong_count']} repeated incorrect answers despite high confidence\n- Concept is in active Danger Zone\n- Crucial to clarify before exam day.",
                "concept_id": top_danger["concept_id"],
                "subject_name": top_danger["subject_name"],
                "recommended_mode": "TARGETED_PRACTICE",
                "estimated_time_minutes": 5,
                "algorithm_version": cls.ALGORITHM_VERSION
            }

        due = await cls.get_due_spaced_revisions(db, user_id)
        if due:
            top_due = due[0]
            return {
                "action_type": "DUE_SPACED_REVISION",
                "priority": "HIGH",
                "title": f"Spaced Revision Due: {top_due['concept_name']}",
                "description": f"Prioritized because:\n- Scheduled spaced repetition is due today\n- {top_due['days_overdue']} day(s) overdue\n- Spacing interval: {top_due['interval_days']} day(s).",
                "concept_id": top_due["concept_id"],
                "subject_name": top_due["subject_name"],
                "recommended_mode": "SPACED_REVISION",
                "estimated_time_minutes": 10,
                "algorithm_version": cls.ALGORITHM_VERSION
            }

        return {
            "action_type": "HIGH_YIELD_DISCOVERY",
            "priority": "STANDARD",
            "title": "Start Daily Practice: High-Yield Core Concepts",
            "description": "Prioritized because:\n- All scheduled revisions and active misconceptions are resolved\n- Daily high-yield syllabus exploration recommended.",
            "concept_id": None,
            "subject_name": None,
            "recommended_mode": "FULL_TEST",
            "estimated_time_minutes": 15,
            "algorithm_version": cls.ALGORITHM_VERSION
        }
