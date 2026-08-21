import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Source(Base):
    """
    Authoritative Medical Source Registry & Freshness Lifecycle (Prompt 10, Sec 9 & 29).
    """
    __tablename__ = "sources"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'STANDARD_TEXTBOOK', 'GUIDELINE', 'OFFICIAL_DOCUMENT', 'PEER_REVIEWED_ARTICLE', 'QUESTION_BANK_REFERENCE', 'EXAM_ARCHIVE', 'OTHER'
    edition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    edition_or_year: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    publication_date: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # 'YYYY-MM-DD'
    publisher: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    specialty: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), default="National / International")
    guideline_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    superseded_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    
    chapter_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    reference_identifier: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)  # ISBN, DOI, PMID
    license_status: Mapped[Optional[str]] = mapped_column(String(50), default="reference_only")
    
    # Freshness & Verification Lifecycle: 'UNVERIFIED', 'VERIFIED', 'OUTDATED', 'SUPERSEDED', 'CONFLICTED', 'REJECTED'
    verification_status: Mapped[str] = mapped_column(String(50), default="UNVERIFIED")
    verified_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_verified_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=utc_now)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Relationships
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="source")
    evidence_references: Mapped[List["EvidenceReference"]] = relationship("EvidenceReference", back_populates="source", cascade="all, delete-orphan")
    pyq_references: Mapped[List["PyqReference"]] = relationship("PyqReference", back_populates="source")
    versions: Mapped[List["SourceVersion"]] = relationship("SourceVersion", back_populates="source", cascade="all, delete-orphan", lazy="selectin", foreign_keys="[SourceVersion.source_id]")


class SourceConflict(Base):
    """
    Guideline & Source Conflict Registry (Prompt 10, Sec 10).
    Captures contradictory medical claims across authoritative sources for expert doctor review.
    """
    __tablename__ = "source_conflicts"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    source_a_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    source_b_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    conflicting_claim: Mapped[str] = mapped_column(Text, nullable=False)
    specialty: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Status: 'UNRESOLVED', 'REVIEW_REQUIRED', 'RESOLVED_BY_MEDICAL_BOARD'
    status: Mapped[str] = mapped_column(String(50), default="REVIEW_REQUIRED", index=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class EvidenceReference(Base):
    """
    Structured Evidence Reference: Links specific factual claims/explanations to source metadata.
    Does NOT store full-text copyrighted books; stores structured citation pointers and factual claims.
    """
    __tablename__ = "evidence_references"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id: Mapped[str] = mapped_column(String(36), ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    fact_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'CORRECT_ANSWER_EVIDENCE', 'DISTRACTOR_REFUTATION', 'CLINICAL_PEARL', 'DIAGNOSTIC_CRITERION'
    claim_snippet: Mapped[str] = mapped_column(Text, nullable=False)
    page_or_section: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    confidence_level: Mapped[float] = mapped_column(Float, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    source: Mapped["Source"] = relationship("Source", back_populates="evidence_references", lazy="selectin")
    question: Mapped["Question"] = relationship("Question", back_populates="evidence_references")


class SourceVersion(Base):
    __tablename__ = "source_versions"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    version_label: Mapped[str] = mapped_column(String(50), nullable=False)
    changes_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    superseded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    source: Mapped["Source"] = relationship("Source", back_populates="versions", foreign_keys=[source_id])


class PyqReference(Base):
    """
    PYQ Provenance Model (Prompt 10, Sec 3):
    Strictly distinguishes VERIFIED_PYQ from derived/linked/unverified questions.
    Never automatically marks AI-generated questions as VERIFIED_PYQ without independent human verification.
    """
    __tablename__ = "pyq_references"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    concept_id: Mapped[str] = mapped_column(String(36), ForeignKey("concepts.id", ondelete="RESTRICT"), nullable=False)
    exam_name: Mapped[str] = mapped_column(String(50), nullable=False)  # 'NEET-PG', 'INI-CET', 'FMGE'
    exam_year: Mapped[int] = mapped_column(Integer, nullable=False)
    exam_session: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # 'May', 'November', 'Regular'
    question_identifier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source_document: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    provenance_confidence: Mapped[float] = mapped_column(Float, default=1.0)
    
    provenance_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    pyq_status: Mapped[str] = mapped_column(String(50), default="UNVERIFIED")  # 'VERIFIED_PYQ', 'PYQ_DERIVED', 'PYQ_CONCEPT_LINKED', 'ORIGINAL', 'AI_PROPOSED', 'UNVERIFIED'
    source_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    
    verification_status: Mapped[str] = mapped_column(String(50), default="UNVERIFIED")  # 'VERIFIED', 'UNVERIFIED', 'DISPUTED'
    verified_by_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    historical_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    source: Mapped[Optional["Source"]] = relationship("Source", back_populates="pyq_references", lazy="selectin")
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="pyq_reference")
