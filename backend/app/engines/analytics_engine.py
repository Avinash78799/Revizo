from datetime import datetime, timezone
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.learning import StudentConceptMastery
from app.models.test import TestAttempt
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.user import Profile
from app.schemas.student import DashboardResponse, DueConceptItem, WeakAreaItem, DangerZoneItem

def utc_now():
    return datetime.now(timezone.utc)

class AnalyticsEngine:
    @staticmethod
    async def get_dashboard_analytics(session: AsyncSession, user_id: str) -> DashboardResponse:
        now = utc_now()

        # 1. Profile / Daily Goal
        stmt_prof = select(Profile).where(Profile.user_id == user_id)
        res_prof = await session.execute(stmt_prof)
        profile = res_prof.scalars().first()
        daily_goal = profile.daily_question_goal if profile else 10

        # 2. Overall Attempts and Accuracy
        stmt_attempts = select(TestAttempt).where(TestAttempt.user_id == user_id)
        res_attempts = await session.execute(stmt_attempts)
        all_attempts = res_attempts.scalars().all()
        total_attempts = len(all_attempts)
        correct_attempts = sum(1 for a in all_attempts if a.is_correct)
        overall_accuracy = round((correct_attempts / total_attempts * 100.0), 1) if total_attempts > 0 else 0.0
        total_mistakes = total_attempts - correct_attempts

        # 3. Concepts Due for Revision
        stmt_due = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.next_revision_due <= now
            )
        ).order_by(StudentConceptMastery.next_revision_due.asc()).limit(5)
        res_due = await session.execute(stmt_due)
        due_records = res_due.scalars().all()

        due_concepts: list[DueConceptItem] = []
        for r in due_records:
            if r.concept:
                topic_name = r.concept.topic.name if r.concept.topic else "General Topic"
                subject_name = r.concept.topic.chapter.subject.name if (r.concept.topic and r.concept.topic.chapter and r.concept.topic.chapter.subject) else "Medical Science"
                due_concepts.append(DueConceptItem(
                    concept_id=r.concept_id,
                    concept_name=r.concept.name,
                    topic_name=topic_name,
                    subject_name=subject_name,
                    revision_interval_days=r.revision_interval_days,
                    next_revision_due=r.next_revision_due
                ))

        # 4. Danger Zone Concepts (High-confidence wrong answers)
        stmt_danger = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.high_confidence_wrong_count > 0
            )
        )
        res_danger = await session.execute(stmt_danger)
        danger_records = res_danger.scalars().all()
        danger_count = len(danger_records)

        # 5. Weak Areas (Mastery < 70%)
        stmt_weak = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.mastery_percentage < 70.0
            )
        ).limit(5)
        res_weak = await session.execute(stmt_weak)
        weak_records = res_weak.scalars().all()

        weak_areas: list[WeakAreaItem] = []
        for r in weak_records:
            if r.concept and r.concept.topic:
                subject_name = r.concept.topic.chapter.subject.name if (r.concept.topic.chapter and r.concept.topic.chapter.subject) else "Subject"
                weak_areas.append(WeakAreaItem(
                    topic_id=r.concept.topic_id,
                    topic_name=r.concept.topic.name,
                    subject_name=subject_name,
                    mastery_percentage=r.mastery_percentage,
                    total_attempts=r.total_attempts
                ))

        # Daily practice estimate
        practice_count = max(0, daily_goal)
        est_minutes = max(3, int(practice_count * 0.8))

        return DashboardResponse(
            todays_practice_count=practice_count,
            todays_practice_est_minutes=est_minutes,
            due_revisions=due_concepts,
            weak_areas=weak_areas,
            danger_zone_count=danger_count,
            total_mistakes_count=total_mistakes,
            total_questions_attempted=total_attempts,
            overall_accuracy_percentage=overall_accuracy
        )

    @staticmethod
    async def get_danger_zone_items(session: AsyncSession, user_id: str) -> list[DangerZoneItem]:
        stmt = select(StudentConceptMastery).where(
            and_(
                StudentConceptMastery.user_id == user_id,
                StudentConceptMastery.high_confidence_wrong_count > 0
            )
        ).order_by(StudentConceptMastery.high_confidence_wrong_count.desc())
        res = await session.execute(stmt)
        records = res.scalars().all()

        items: list[DangerZoneItem] = []
        for r in records:
            if r.concept:
                topic_name = r.concept.topic.name if r.concept.topic else "Topic"
                subject_name = r.concept.topic.chapter.subject.name if (r.concept.topic and r.concept.topic.chapter and r.concept.topic.chapter.subject) else "Subject"
                items.append(DangerZoneItem(
                    concept_id=r.concept_id,
                    concept_name=r.concept.name,
                    topic_name=topic_name,
                    subject_name=subject_name,
                    high_confidence_wrong_count=r.high_confidence_wrong_count,
                    last_practiced_at=r.last_practiced_at,
                    clinical_pearl=r.concept.clinical_pearl
                ))
        return items
