import uuid
from datetime import datetime, timedelta
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="student")  # 'student', 'medical_reviewer', 'admin'
    target_exam_year: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sessions: Mapped[list["TestSession"]] = relationship("TestSession", back_populates="user", cascade="all, delete-orphan")
    attempts: Mapped[list["TestAttempt"]] = relationship("TestAttempt", back_populates="user", cascade="all, delete-orphan")
    mastery_records: Mapped[list["StudentConceptMastery"]] = relationship("StudentConceptMastery", back_populates="user", cascade="all, delete-orphan")


class TestSession(Base):
    __tablename__ = "test_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(50), nullable=False)  # 'quick_test', 'topic_test', 'chapter_test', 'rapid_recall', 'mistake_revision', 'adaptive', 'five_minute_revision', 'grand_test'
    subject_id: Mapped[str] = mapped_column(String(36), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    chapter_id: Mapped[str] = mapped_column(String(36), ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True)
    topic_id: Mapped[str] = mapped_column(String(36), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_questions: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    attempts: Mapped[list["TestAttempt"]] = relationship("TestAttempt", back_populates="session", cascade="all, delete-orphan")


class TestAttempt(Base):
    __tablename__ = "test_attempts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False, index=True)
    selected_option_key: Mapped[str] = mapped_column(String(1), nullable=True)  # 'A', 'B', 'C', 'D'
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidence: Mapped[str] = mapped_column(String(30), default="somewhat_confident")  # 'definitely_know', 'somewhat_confident', 'guessing'
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    is_danger_zone_item: Mapped[bool] = mapped_column(Boolean, default=False, index=True)  # Wrong + definitely_know
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped["TestSession"] = relationship("TestSession", back_populates="attempts")
    user: Mapped["User"] = relationship("User", back_populates="attempts")


class StudentConceptMastery(Base):
    __tablename__ = "student_concept_mastery"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    total_attempts: Mapped[int] = mapped_column(Integer, default=0)
    correct_attempts: Mapped[int] = mapped_column(Integer, default=0)
    high_confidence_wrong_count: Mapped[int] = mapped_column(Integer, default=0)  # Danger Zone indicator
    mastery_percentage: Mapped[float] = mapped_column(Float, default=0.0)

    # Adaptive Spaced Repetition parameters
    last_practiced_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    next_revision_due: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=1), index=True)
    revision_interval_days: Mapped[int] = mapped_column(Integer, default=1)
    ease_factor: Mapped[float] = mapped_column(Float, default=2.50)
    consecutive_correct_count: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship("User", back_populates="mastery_records")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="mastery_records")
