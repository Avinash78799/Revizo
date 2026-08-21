import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class TestTemplate(Base):
    __tablename__ = "test_templates"
    __table_args__ = {"extend_existing": True}
    __test__ = False

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    mode: Mapped[str] = mapped_column(String(50), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    sessions: Mapped[list["TestSession"]] = relationship("TestSession", back_populates="template")


class TestSession(Base):
    """
    Server-Authoritative Test Session Lifecycle, Blueprint & Integrity Engine (Prompt 9 & 9.1).
    """
    __tablename__ = "test_sessions"
    __table_args__ = {"extend_existing": True}
    __test__ = False

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    template_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("test_templates.id", ondelete="SET NULL"), nullable=True)
    
    # Test Modes: 'DAILY_SHORT_TEST', 'CHAPTER_REVISION_TEST', 'TOPIC_TEST', 'SUBJECT_TEST', 'WEEKLY_GRAND_TEST', 'RAPID_RECALL_TEST', 'MISTAKE_RETEST', 'DANGER_ZONE_RETEST', 'CUSTOM_PRACTICE'
    mode: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="IN_PROGRESS", nullable=False, index=True)  # 'NOT_STARTED', 'IN_PROGRESS', 'SUBMITTED', 'EXPIRED', 'CANCELLED', 'TERMINATED_INTEGRITY'
    
    subject_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    chapter_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("chapters.id", ondelete="SET NULL"), nullable=True)
    topic_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_questions: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[int] = mapped_column(Integer, default=0)
    
    # Blueprint Configuration & Provenance Metadata (Prompt 9.1, Sec 5 & 6)
    blueprint_config: Mapped[dict] = mapped_column(JSON, default=dict)
    test_reproducibility_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Server Authoritative Timers
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Integrity & Anti-Cheating Tracking (Prompt 9.1, Sec 1-3)
    integrity_mode: Mapped[str] = mapped_column(String(30), default="WARNING_MODE")  # 'WARNING_MODE', 'STRICT_MODE'
    integrity_score: Mapped[int] = mapped_column(Integer, default=100)
    is_terminated_by_integrity: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    template: Mapped[Optional["TestTemplate"]] = relationship("TestTemplate", back_populates="sessions")
    questions: Mapped[list["TestQuestion"]] = relationship("TestQuestion", back_populates="session", cascade="all, delete-orphan", lazy="selectin")
    attempts: Mapped[list["TestAttempt"]] = relationship("TestAttempt", back_populates="session", cascade="all, delete-orphan", lazy="selectin")
    integrity_events: Mapped[list["IntegrityEvent"]] = relationship("IntegrityEvent", back_populates="session", cascade="all, delete-orphan", lazy="selectin")


class TestQuestion(Base):
    __tablename__ = "test_questions"
    __table_args__ = {"extend_existing": True}
    __test__ = False

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    session: Mapped["TestSession"] = relationship("TestSession", back_populates="questions")
    question: Mapped["Question"] = relationship("Question", lazy="selectin")


class TestAttempt(Base):
    __tablename__ = "test_attempts"
    __table_args__ = {"extend_existing": True}
    __test__ = False

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False)
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    selected_option_key: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidence: Mapped[str] = mapped_column(String(30), default="DEFINITELY_KNOW")  # 'DEFINITELY_KNOW', 'PROBABLY_KNOW', 'UNSURE', 'GUESSING'
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    is_danger_zone_item: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    session: Mapped["TestSession"] = relationship("TestSession", back_populates="attempts")
    user: Mapped["User"] = relationship("User", back_populates="attempts")
    question: Mapped["Question"] = relationship("Question", lazy="selectin")
    concept: Mapped["Concept"] = relationship("Concept", lazy="selectin")


class IntegrityEvent(Base):
    """
    Integrity Event Audit Log with Severity Weight Model (Prompt 9.1, Sec 1).
    """
    __tablename__ = "integrity_events"
    __table_args__ = {"extend_existing": True}
    __test__ = False

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Event Types: 'NETWORK_INTERRUPTION', 'WINDOW_BLURRED', 'VISIBILITY_CHANGE', 'FULLSCREEN_EXIT', 'TAB_HIDDEN', 'REPEATED_SUSPICIOUS_VISIBILITY', 'RECONNECT', 'OTHER'
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity_weight: Mapped[int] = mapped_column(Integer, default=1)  # 0, 1, 2, 3, 4
    severity: Mapped[str] = mapped_column(String(20), default="LOW")  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    source: Mapped[str] = mapped_column(String(50), default="browser_visibility")
    event_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    session: Mapped["TestSession"] = relationship("TestSession", back_populates="integrity_events")
