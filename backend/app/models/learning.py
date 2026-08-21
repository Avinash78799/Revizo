import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class StudentConceptMastery(Base):
    """
    Student Concept-Level Mastery & Spaced Repetition Engine (Prompt 8 & 8.1).
    Tracks Bayesian-smoothed mastery, clinical confidence metrics, interpretable mastery states,
    and granular misconception states (CONFIDENCE_ERROR -> SUSPECTED_MISCONCEPTION -> CONFIRMED_MISCONCEPTION -> DANGER_ZONE).
    """
    __tablename__ = "student_concept_mastery"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Statistical Attempt Metrics
    total_attempts: Mapped[int] = mapped_column(Integer, default=0)
    correct_attempts: Mapped[int] = mapped_column(Integer, default=0)
    wrong_count: Mapped[int] = mapped_column(Integer, default=0)
    high_confidence_wrong_count: Mapped[int] = mapped_column(Integer, default=0)  # Danger Zone indicator (WRONG + DEFINITELY_KNOW)
    lucky_guess_count: Mapped[int] = mapped_column(Integer, default=0)  # CORRECT + JUST_GUESSING
    
    # Statistical Mastery & Safeguards
    mastery_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    smoothed_mastery_score: Mapped[float] = mapped_column(Float, default=0.50)  # Bayesian Beta prior (correct+1)/(total+2)
    confidence_interval_width: Mapped[float] = mapped_column(Float, default=1.0)  # Lower is more statistically reliable
    
    # Interpretable Mastery State: 'UNSEEN', 'INTRODUCED', 'WEAK', 'FRAGILE', 'DEVELOPING', 'STABLE', 'STRONG', 'MASTERED'
    mastery_state: Mapped[str] = mapped_column(String(30), default="UNSEEN", index=True)
    
    # Misconception State Progression: 'NONE', 'CONFIDENCE_ERROR', 'SUSPECTED_MISCONCEPTION', 'CONFIRMED_MISCONCEPTION', 'DANGER_ZONE'
    misconception_state: Mapped[str] = mapped_column(String(40), default="NONE", index=True)
    is_cold_start: Mapped[bool] = mapped_column(Boolean, default=True)  # True when attempts < 3
    danger_zone_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)  # Active when high_conf_wrong >= 2
    
    # Adaptive Spaced Repetition (SM-2 with Clinical Confidence Modifiers)
    last_practiced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    next_revision_due: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: utc_now() + timedelta(days=1), index=True)
    revision_interval_days: Mapped[int] = mapped_column(Integer, default=1)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.50)
    consecutive_correct_count: Mapped[int] = mapped_column(Integer, default=0)
    repetition_count: Mapped[int] = mapped_column(Integer, default=0)
    algorithm_version: Mapped[str] = mapped_column(String(30), default="adaptive-v1.0")

    user: Mapped["User"] = relationship("User", back_populates="mastery_records")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="mastery_records", lazy="selectin")


class LearningEvidenceRecord(Base):
    """
    Immutable Learning Evidence Log with Idempotency & Invalidation Tracking (Prompt 8, Sec 6, 26, 27).
    Guarantees that:
    1. Duplicate answer submissions do not double-count learning events.
    2. Quarantined / defective questions can be marked is_invalidated=True to prevent poisoning mastery.
    """
    __tablename__ = "learning_evidence_records"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idempotency_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    attempt_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidence: Mapped[str] = mapped_column(String(30), nullable=False)
    response_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    is_invalidated: Mapped[bool] = mapped_column(Boolean, default=False, index=True)  # Set to True if question is quarantined
    algorithm_version: Mapped[str] = mapped_column(String(30), default="adaptive-v1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class StudentMistakeRecord(Base):
    """
    Mistake Bank & Error Taxonomy Engine (Prompt 8, Sec 6 & 18).
    Classifies student errors and tracks resolution across test sessions.
    """
    __tablename__ = "student_mistake_records"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("test_sessions.id", ondelete="SET NULL"), nullable=True)
    
    selected_option_key: Mapped[str] = mapped_column(String(1), nullable=False)
    correct_option_key: Mapped[str] = mapped_column(String(1), nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(30), default="DEFINITELY_KNOW")
    
    # Error Taxonomy: 'CONFIDENCE_ERROR', 'FACTUAL_KNOWLEDGE_GAP', 'CLINICAL_REASONING_FAULT', 'DISTRACTOR_TRAP', 'SPEED_SILLY_MISTAKE'
    error_type: Mapped[str] = mapped_column(String(50), default="CONFIDENCE_ERROR")
    
    # Misconception State: 'CONFIDENCE_ERROR', 'SUSPECTED_MISCONCEPTION', 'CONFIRMED_MISCONCEPTION', 'DANGER_ZONE', 'NOT_APPLICABLE'
    misconception_state: Mapped[str] = mapped_column(String(40), default="SUSPECTED_MISCONCEPTION")
    status: Mapped[str] = mapped_column(String(30), default="UNRESOLVED", index=True)  # 'UNRESOLVED', 'REVIEWED', 'RESOLVED_ON_RETEST'
    occurrence_count: Mapped[int] = mapped_column(Integer, default=1)
    
    first_occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", lazy="selectin")
    question: Mapped["Question"] = relationship("Question", lazy="selectin")
    concept: Mapped["Concept"] = relationship("Concept", lazy="selectin")


class DailyStudyPlan(Base):
    """
    Personalized Daily Study Plan & Next-Best-Action Engine (Prompt 8 & 8.1).
    Prioritizes Danger Zone misconceptions, due revisions, weak topics, and new concept discovery with configurable weights.
    """
    __tablename__ = "daily_study_plans"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_date: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # 'YYYY-MM-DD'
    
    total_target_questions: Mapped[int] = mapped_column(Integer, default=20)
    completed_questions_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Plan Slices (JSON arrays of concept IDs and reasons)
    danger_zone_slice: Mapped[dict] = mapped_column(JSON, default=dict)
    due_revision_slice: Mapped[dict] = mapped_column(JSON, default=dict)
    weak_subject_slice: Mapped[dict] = mapped_column(JSON, default=dict)
    discovery_slice: Mapped[dict] = mapped_column(JSON, default=dict)
    
    status: Mapped[str] = mapped_column(String(30), default="GENERATED")  # 'GENERATED', 'IN_PROGRESS', 'COMPLETED'
    algorithm_version: Mapped[str] = mapped_column(String(30), default="adaptive-v1.0")
    allocation_strategy_version: Mapped[str] = mapped_column(String(30), default="daily-alloc-v1.0")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", lazy="selectin")


class StudentQuestionHistory(Base):
    __tablename__ = "student_question_history"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    total_encounters: Mapped[int] = mapped_column(Integer, default=1)
    correct_encounters: Mapped[int] = mapped_column(Integer, default=0)
    last_encountered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class RevisionSchedule(Base):
    __tablename__ = "revision_schedule"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    scheduled_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="revision_schedules")


class UserQuestionBookmark(Base):
    """
    Feature 8: Smart Bookmarks and Personal Revision Notes.
    Enables medical students to bookmark questions and attach clinical learning notes.
    """
    __tablename__ = "user_question_bookmarks"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    question: Mapped["Question"] = relationship("Question", lazy="selectin")

