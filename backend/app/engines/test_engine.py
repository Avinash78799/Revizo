import uuid
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.test import TestSession, TestQuestion, TestAttempt
from app.models.question import Question, QuestionOption
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.schemas.question import SanitizedQuestionResponse, SanitizedOptionResponse, EvaluationResultResponse
from app.engines.learning_engine import LearningEngine

def utc_now():
    return datetime.now(timezone.utc)

class TestEngine:
    @staticmethod
    async def create_test_session(
        session: AsyncSession,
        user_id: str,
        mode: str,
        subject_id: Optional[str] = None,
        chapter_id: Optional[str] = None,
        topic_id: Optional[str] = None,
        question_count: int = 5
    ) -> Tuple[TestSession, List[Question]]:
        """
        Creates a test session and selects eligible questions.
        Delegates question selection to the canonical QuestionSelectionEngine.
        """
        from app.services.question_selection_engine import QuestionSelectionEngine

        questions, _ = await QuestionSelectionEngine.select_questions_for_test(
            db=session,
            user_id=user_id,
            mode=mode,
            question_count=question_count,
            subject_id=subject_id,
            chapter_id=chapter_id,
            topic_id=topic_id
        )

        if not questions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions currently available for the selected topic."
            )

        test_session = TestSession(
            user_id=user_id,
            mode=mode,
            subject_id=subject_id,
            chapter_id=chapter_id,
            topic_id=topic_id,
            total_questions=len(questions),
            completed_questions=0,
            score=0,
            started_at=utc_now()
        )
        session.add(test_session)
        await session.flush()

        for idx, q in enumerate(questions):
            test_question = TestQuestion(
                session_id=test_session.id,
                question_id=q.id,
                order_index=idx + 1
            )
            session.add(test_question)

        await session.flush()
        return test_session, questions

    @staticmethod
    def sanitize_question(q: Question) -> SanitizedQuestionResponse:
        """
        Strictly sanitizes a Question object so NO answers or explanations
        reach the client during an active test.
        """
        sanitized_options = [
            SanitizedOptionResponse(option_key=opt.option_key, option_text=opt.option_text)
            for opt in q.options
        ]
        sanitized_options.sort(key=lambda x: x.option_key)

        return SanitizedQuestionResponse(
            id=q.id,
            concept_id=q.concept_id,
            concept_name=q.concept.name if q.concept else None,
            topic_name=q.concept.topic.name if q.concept and q.concept.topic else None,
            subject_name=q.concept.topic.chapter.subject.name if q.concept and q.concept.topic and q.concept.topic.chapter and q.concept.topic.chapter.subject else None,
            trust_class=q.trust_class,
            question_type=q.question_type,
            difficulty=q.difficulty,
            is_high_yield=q.is_high_yield,
            question_text=q.question_text,
            options=sanitized_options
        )

    @staticmethod
    async def evaluate_answer(
        session: AsyncSession,
        user_id: str,
        session_id: str,
        question_id: str,
        selected_option_key: str,
        confidence: str,
        time_spent_seconds: int = 0
    ) -> EvaluationResultResponse:
        """
        Evaluates answer server-side, updates mastery and spaced repetition intervals,
        and returns the structured corrective breakdown.
        """
        stmt_session = select(TestSession).where(TestSession.id == session_id, TestSession.user_id == user_id)
        res_session = await session.execute(stmt_session)
        test_session = res_session.scalars().first()
        if not test_session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test session not found or unauthorized.")

        stmt_q = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.concept)
        ).where(Question.id == question_id)
        res_q = await session.execute(stmt_q)
        question = res_q.scalars().first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found.")

        correct_option = next((opt for opt in question.options if opt.is_correct), None)
        selected_option = next((opt for opt in question.options if opt.option_key == selected_option_key.upper()), None)

        if not correct_option or not selected_option:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid option key submitted.")

        is_correct = (selected_option.option_key == correct_option.option_key)
        is_danger_zone = (not is_correct) and (confidence == "definitely_know")

        attempt = TestAttempt(
            session_id=session_id,
            user_id=user_id,
            question_id=question_id,
            concept_id=question.concept_id,
            selected_option_key=selected_option.option_key,
            is_correct=is_correct,
            confidence=confidence,
            time_spent_seconds=time_spent_seconds,
            is_danger_zone_item=is_danger_zone,
            answered_at=utc_now()
        )
        session.add(attempt)

        test_session.completed_questions += 1
        if is_correct:
            test_session.score += 1
        if test_session.completed_questions >= test_session.total_questions:
            test_session.completed_at = utc_now()

        mastery = await LearningEngine.update_student_concept_mastery(
            session=session,
            user_id=user_id,
            concept_id=question.concept_id,
            is_correct=is_correct,
            confidence=confidence
        )
        await LearningEngine.record_question_history(
            session=session,
            user_id=user_id,
            question_id=question_id,
            is_correct=is_correct
        )

        return EvaluationResultResponse(
            is_correct=is_correct,
            selected_option_key=selected_option.option_key,
            correct_option_key=correct_option.option_key,
            correct_explanation=question.correct_explanation,
            why_selected_was_wrong=selected_option.why_wrong_explanation if not is_correct else None,
            remember_takeaway=question.remember_takeaway,
            exam_connection=question.exam_connection,
            detailed_explanation=question.detailed_explanation,
            concept_id=question.concept_id,
            concept_name=question.concept.name if question.concept else "Medical Concept",
            is_danger_zone_item=is_danger_zone,
            revision_interval_days=mastery.revision_interval_days,
            next_revision_due=mastery.next_revision_due
        )

    @staticmethod
    async def get_retest_question(
        session: AsyncSession,
        concept_id: str,
        exclude_question_id: Optional[str] = None
    ) -> SanitizedQuestionResponse:
        query = select(Question).options(
            selectinload(Question.options),
            selectinload(Question.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
        ).where(
            Question.concept_id == concept_id,
            Question.status == "published"
        )
        if exclude_question_id:
            query = query.where(Question.id != exclude_question_id)

        result = await session.execute(query)
        alt_question = result.scalars().first()

        if not alt_question:
            stmt_fallback = select(Question).options(
                selectinload(Question.options),
                selectinload(Question.concept).selectinload(Concept.topic).selectinload(Topic.chapter).selectinload(Chapter.subject)
            ).where(Question.concept_id == concept_id)
            res_fb = await session.execute(stmt_fallback)
            alt_question = res_fb.scalars().first()

        if not alt_question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No alternative question found for this concept.")

        return TestEngine.sanitize_question(alt_question)
