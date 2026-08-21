import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class GenerationJob(Base):
    """
    Asynchronous AI Question Generation Job (Prompt 7, Sec 34).
    Tracks batch status, quotas, cost, and lifecycle states:
    QUEUED -> RUNNING -> COMPLETED / PARTIAL / FAILED / CANCELLED.
    """
    __tablename__ = "generation_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), default="QUEUED", index=True)  # 'QUEUED', 'RUNNING', 'COMPLETED', 'PARTIAL', 'FAILED', 'CANCELLED'
    
    # Request Parameters & Quotas
    request_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    requested_count: Mapped[int] = mapped_column(Integer, default=1)
    generated_count: Mapped[int] = mapped_column(Integer, default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    rejected_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Cost & Observability
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    concept: Mapped["Concept"] = relationship("Concept", lazy="selectin")


class AIEvaluationDataset(Base):
    """
    Fixed evaluation benchmark dataset containing known expert-reviewed questions (Prompt 7, Sec 39 & 44).
    Used to benchmark AI validator accuracy, false-positive rates, and prompt regressions.
    """
    __tablename__ = "ai_evaluation_datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20), default="v1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    items: Mapped[List["AIEvaluationItem"]] = relationship("AIEvaluationItem", back_populates="dataset", cascade="all, delete-orphan", lazy="selectin")
    runs: Mapped[List["AIEvaluationRun"]] = relationship("AIEvaluationRun", back_populates="dataset", cascade="all, delete-orphan")


class AIEvaluationItem(Base):
    __tablename__ = "ai_evaluation_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("ai_evaluation_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    question_payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    expected_verdict: Mapped[str] = mapped_column(String(20), nullable=False)  # 'PASS', 'REJECT', 'REVIEW_REQUIRED'
    known_issue_type: Mapped[str] = mapped_column(String(50), default="NONE")  # 'AMBIGUITY', 'CONTRADICTION', 'OUTDATED', 'DISTRACTOR_ABSURD', 'NONE'
    expert_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    dataset: Mapped["AIEvaluationDataset"] = relationship("AIEvaluationDataset", back_populates="items")


class AIEvaluationRun(Base):
    __tablename__ = "ai_evaluation_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("ai_evaluation_datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt_version: Mapped[str] = mapped_column(String(30), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    accuracy_score: Mapped[float] = mapped_column(Float, default=0.0)
    false_positive_rate: Mapped[float] = mapped_column(Float, default=0.0)
    false_negative_rate: Mapped[float] = mapped_column(Float, default=0.0)
    metrics_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    dataset: Mapped["AIEvaluationDataset"] = relationship("AIEvaluationDataset", back_populates="runs")
