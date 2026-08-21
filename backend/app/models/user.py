import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="student")  # 'student', 'medical_reviewer', 'admin'
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    sessions: Mapped[list["TestSession"]] = relationship("TestSession", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    attempts: Mapped[list["TestAttempt"]] = relationship("TestAttempt", back_populates="user", cascade="all, delete-orphan")
    mastery_records: Mapped[list["StudentConceptMastery"]] = relationship("StudentConceptMastery", back_populates="user", cascade="all, delete-orphan")
    revision_schedules: Mapped[list["RevisionSchedule"]] = relationship("RevisionSchedule", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=True)
    target_exam_year: Mapped[int] = mapped_column(Integer, nullable=True)
    daily_question_goal: Mapped[int] = mapped_column(Integer, default=10)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user: Mapped["User"] = relationship("User", back_populates="profile")
