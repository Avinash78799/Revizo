import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class AIGeneration(Base):
    __tablename__ = "ai_generations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_version: Mapped[str] = mapped_column(String(20), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.00)
    raw_response: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AIValidationResult(Base):
    __tablename__ = "ai_validation_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    generation_id: Mapped[str] = mapped_column(String(36), ForeignKey("ai_generations.id", ondelete="SET NULL"), nullable=True)
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="SET NULL"), nullable=True)
    validator_version: Mapped[str] = mapped_column(String(20), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    validation_stage: Mapped[str] = mapped_column(String(50), nullable=False)  # 'structural', 'medical_consistency', 'ambiguity', 'duplicate'
    details: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
