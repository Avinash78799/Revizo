import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Question(Base):
    """
    Medical Question Model with 7 Content Trust Classes, High-Yield Provenance & Quality Hard Gates (Prompt 10 & 11).
    """
    __tablename__ = "questions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    # 7-Level Content Trust Hierarchy (Prompt 10, Sec 2)
    # LEVEL 1: 'VERIFIED_CORE_QUESTION'
    # LEVEL 2: 'VERIFIED_PYQ'
    # LEVEL 3: 'SOURCE_REFERENCED'
    # LEVEL 4: 'AI_GENERATED_REVIEW_PENDING'
    # LEVEL 5: 'DEVELOPMENT_SEED'
    # LEVEL 6: 'QUARANTINED'
    # LEVEL 7: 'WITHDRAWN'
    trust_class: Mapped[str] = mapped_column(String(50), default="AI_GENERATED_REVIEW_PENDING", index=True)
    
    # Question Lifecycle State Machine
    status: Mapped[str] = mapped_column(String(30), default="PROPOSED", index=True)
    
    question_type: Mapped[str] = mapped_column(String(50), default="clinical_vignette")
    difficulty: Mapped[str] = mapped_column(String(20), default="moderate")
    difficulty_score: Mapped[float] = mapped_column(Float, default=0.50)  # 0.00 to 1.00
    observed_difficulty_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    total_attempts_count: Mapped[int] = mapped_column(Integer, default=0)
    correct_attempts_count: Mapped[int] = mapped_column(Integer, default=0)
    discrimination_index: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_high_yield: Mapped[bool] = mapped_column(Boolean, default=False)
    exam_relevance_tag: Mapped[str] = mapped_column(String(50), default="HIGH_YIELD")

    # High-Yield Evidence Provenance (Prompt 11, Sec 8)
    pyq_recurrence_component: Mapped[float] = mapped_column(Float, default=0.0)
    clinical_importance_component: Mapped[float] = mapped_column(Float, default=0.50)
    curriculum_centrality_component: Mapped[float] = mapped_column(Float, default=0.50)
    high_yield_evidence_count: Mapped[int] = mapped_column(Integer, default=0)

    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Structured Corrective Explanation Anatomy
    correct_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    remember_takeaway: Mapped[str] = mapped_column(Text, nullable=False)
    exam_connection: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detailed_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Source and PYQ Links
    source_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    source_citation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pyq_reference_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("pyq_references.id", ondelete="SET NULL"), nullable=True)

    # High-Risk Content & Two-Person Review
    is_high_risk: Mapped[bool] = mapped_column(Boolean, default=False)
    high_risk_category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    first_reviewer_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    first_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    second_reviewer_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    second_reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Provenance & AI Metadata
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=True)
    ai_model_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    prompt_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    author_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    review_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Medical Freshness
    freshness_status: Mapped[str] = mapped_column(String(30), default="CURRENT")

    # Deduplication & Versioning
    text_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    content_version: Mapped[int] = mapped_column(Integer, default=1)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    review_due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    guideline_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    concept: Mapped["Concept"] = relationship("Concept", back_populates="questions", lazy="selectin")
    options: Mapped[List["QuestionOption"]] = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    source: Mapped[Optional["Source"]] = relationship("Source", back_populates="questions", lazy="selectin")
    evidence_references: Mapped[List["EvidenceReference"]] = relationship("EvidenceReference", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    pyq_reference: Mapped[Optional["PyqReference"]] = relationship("PyqReference", back_populates="questions", lazy="selectin")
    versions: Mapped[List["QuestionVersion"]] = relationship("QuestionVersion", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    reviews: Mapped[List["QuestionReview"]] = relationship("QuestionReview", back_populates="question", cascade="all, delete-orphan", lazy="selectin")
    quality_scorecard: Mapped[Optional["QuestionQualityScorecard"]] = relationship("QuestionQualityScorecard", back_populates="question", uselist=False, cascade="all, delete-orphan", lazy="selectin")
    reports: Mapped[List["QuestionReport"]] = relationship("QuestionReport", back_populates="question", cascade="all, delete-orphan")
    quarantine_records: Mapped[List["QuestionQuarantineRegistry"]] = relationship("QuestionQuarantineRegistry", back_populates="question", cascade="all, delete-orphan")


class QuestionOption(Base):
    __tablename__ = "question_options"
    __table_args__ = (
        UniqueConstraint('question_id', 'option_key', name='uq_question_option_key'),
        {"extend_existing": True}
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    option_key: Mapped[str] = mapped_column(String(1), nullable=False)
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    why_wrong_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    question: Mapped["Question"] = relationship("Question", back_populates="options")


class QuestionVersion(Base):
    __tablename__ = "question_versions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    correct_option_key: Mapped[str] = mapped_column(String(1), nullable=False)
    correct_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    remember_takeaway: Mapped[str] = mapped_column(Text, nullable=False)
    source_citation: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    changed_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    change_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    question: Mapped["Question"] = relationship("Question", back_populates="versions")


class QuestionReview(Base):
    __tablename__ = "question_reviews"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    reviewer_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    verdict: Mapped[str] = mapped_column(String(50), nullable=False)
    question_version: Mapped[int] = mapped_column(Integer, default=1)
    reviewer_credential_status: Mapped[str] = mapped_column(String(50), default="VERIFIED_ACTIVE")
    source_verification_decision: Mapped[str] = mapped_column(String(50), default="VERIFIED")
    guideline_verification_decision: Mapped[str] = mapped_column(String(50), default="VERIFIED")
    clinical_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    guideline_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    question: Mapped["Question"] = relationship("Question", back_populates="reviews")


class QuestionQualityScorecard(Base):
    """
    Multidimensional Question Quality Scorecard & Hard Gates (Prompt 11, Sec 6-7).
    All component scores normalized strictly to 0.0 - 1.0.
    Critical failures always trigger HARD_REJECT regardless of aggregate overall score.
    """
    __tablename__ = "question_quality_scorecards"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Normalized Dimension Scores (0.00 to 1.00)
    clinical_accuracy_score: Mapped[float] = mapped_column(Float, default=1.0)
    single_best_answer_score: Mapped[float] = mapped_column(Float, default=1.0)
    distractor_quality_score: Mapped[float] = mapped_column(Float, default=0.85)
    exam_relevance_score: Mapped[float] = mapped_column(Float, default=0.80)
    source_support_score: Mapped[float] = mapped_column(Float, default=1.0)
    explanation_quality_score: Mapped[float] = mapped_column(Float, default=0.90)
    novelty_score: Mapped[float] = mapped_column(Float, default=0.85)
    overall_quality_score: Mapped[float] = mapped_column(Float, default=0.90)

    # Boolean Sub-Checks
    clinical_accuracy_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    medical_accuracy_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    syllabus_alignment_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    single_best_answer_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    source_support_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    source_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    
    question_clarity_score: Mapped[float] = mapped_column(Float, default=1.0)
    difficulty_predicted: Mapped[float] = mapped_column(Float, default=0.50)
    concept_relevance_score: Mapped[float] = mapped_column(Float, default=0.90)
    ambiguity_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    ambiguity_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    outdated_info_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    duplicate_risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    language_quality_score: Mapped[float] = mapped_column(Float, default=0.95)
    
    # Quality Hard Gate (Prompt 11, Sec 6)
    # 'PASSED', 'CRITICAL_FAILURE_HARD_REJECT', 'REVIEW_REQUIRED'
    quality_gate_status: Mapped[str] = mapped_column(String(50), default="PASSED", index=True)
    failed_gate: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    validation_report: Mapped[dict] = mapped_column(JSON, default=dict)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    question: Mapped["Question"] = relationship("Question", back_populates="quality_scorecard")


class QuestionReport(Base):
    __tablename__ = "question_reports"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reason: Mapped[str] = mapped_column(String(50), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_serious_medical_error: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    question: Mapped["Question"] = relationship("Question", back_populates="reports")


class QuestionQuarantineRegistry(Base):
    __tablename__ = "question_quarantine_registry"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    quarantine_reason: Mapped[str] = mapped_column(String(100), nullable=False)
    resolution_status: Mapped[str] = mapped_column(String(50), default="quarantined")
    audit_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quarantined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    revalidated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    question: Mapped["Question"] = relationship("Question", back_populates="quarantine_records")


class AICallLog(Base):
    __tablename__ = "ai_call_logs"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    request_type: Mapped[str] = mapped_column(String(50), nullable=False)
    question_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    prompt_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    tokens_prompt: Mapped[int] = mapped_column(Integer, default=0)
    tokens_completion: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
