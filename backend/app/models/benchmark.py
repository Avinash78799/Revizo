import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class BenchmarkCase(Base):
    """
    Expert-Reviewed Gold Medical Benchmark Case (Prompt 11 & 12).
    Permanent benchmark instances across 16 standard categories with explicit provenance tracking.
    """
    __tablename__ = "benchmark_cases"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    benchmark_case_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[dict] = mapped_column(JSON, nullable=False)
    correct_option_key: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    
    # Expected outcome: 'PASS', 'HARD_REJECT', 'REVIEW_REQUIRED'
    expected_result: Mapped[str] = mapped_column(String(50), nullable=False)
    expected_validator_behavior: Mapped[str] = mapped_column(String(100), nullable=False)
    medical_rationale: Mapped[str] = mapped_column(Text, nullable=False)
    authoritative_source: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Provenance Tracking (Prompt 12, Sec 2): 'DEVELOPMENT_BENCHMARK', 'EXPERT_VERIFIED'
    provenance_status: Mapped[str] = mapped_column(String(50), default="DEVELOPMENT_BENCHMARK", index=True)
    reviewer_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    expert_verified_by: Mapped[str] = mapped_column(String(150), nullable=False)
    verification_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    benchmark_version: Mapped[str] = mapped_column(String(50), default="gold-benchmark-v1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
