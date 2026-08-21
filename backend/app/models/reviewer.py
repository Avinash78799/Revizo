import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class MedicalReviewerProfile(Base):
    """
    Medical Reviewer Credential & Verification Model (Prompt 11, Sec 3).
    Only VERIFIED + ACTIVE medical reviewers can approve medical questions.
    """
    __tablename__ = "medical_reviewer_profiles"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    credential_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'MBBS', 'MD', 'MS', 'DNB', 'DM', 'MCh'
    registration_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    medical_council: Mapped[Optional[str]] = mapped_column(String(150), default="State Medical Council / NMC")
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Reviewer Lifecycle: 'PENDING', 'VERIFIED', 'SUSPENDED', 'REVOKED'
    verification_status: Mapped[str] = mapped_column(String(50), default="PENDING", index=True)
    credential_status: Mapped[str] = mapped_column(String(50), default="ACTIVE")
    active_status: Mapped[bool] = mapped_column(Boolean, default=True)
    
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    suspension_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], lazy="selectin")
