import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Text, Integer, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class SyllabusRegistry(Base):
    """
    NEET-PG Canonical Curriculum Versioning (Prompt 10 & 11).
    """
    __tablename__ = "syllabus_registry"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    syllabus_version: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # 'neet-pg-nmc-2026-v1.0'
    source: Mapped[str] = mapped_column(String(150), default="National Medical Commission (NMC)")
    effective_date: Mapped[str] = mapped_column(String(10), default="2026-01-01")
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED")  # 'VERIFIED', 'UNVERIFIED'
    import_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class SyllabusSourceArtifact(Base):
    """
    Authoritative Syllabus Source Provenance (Prompt 11, Sec 1).
    Preserves exact source documents, hashes, and verification audit trails.
    """
    __tablename__ = "syllabus_source_artifacts"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    syllabus_version: Mapped[str] = mapped_column(String(50), ForeignKey("syllabus_registry.syllabus_version"), nullable=False)
    source_name: Mapped[str] = mapped_column(String(200), nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    document_identifier: Mapped[str] = mapped_column(String(100), nullable=False)
    document_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    effective_date: Mapped[str] = mapped_column(String(10), nullable=False)
    verification_status: Mapped[str] = mapped_column(String(50), default="UNVERIFIED")  # 'VERIFIED', 'UNVERIFIED'
    verified_by: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    verification_timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Subject(Base):
    __tablename__ = "subjects"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    chapters: Mapped[list["Chapter"]] = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan", lazy="selectin")


class Chapter(Base):
    __tablename__ = "chapters"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subject_id: Mapped[str] = mapped_column(String(36), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    subject: Mapped["Subject"] = relationship("Subject", back_populates="chapters", lazy="selectin")
    topics: Mapped[list["Topic"]] = relationship("Topic", back_populates="chapter", cascade="all, delete-orphan", lazy="selectin")


class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id: Mapped[str] = mapped_column(String(36), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="topics", lazy="selectin")
    concepts: Mapped[list["Concept"]] = relationship("Concept", back_populates="topic", cascade="all, delete-orphan", lazy="selectin")


class Concept(Base):
    """
    NEET-PG Curriculum Concept with Authoritative Source Mapping (Prompt 11, Sec 2).
    """
    __tablename__ = "concepts"
    __table_args__ = {"extend_existing": True}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic_id: Mapped[str] = mapped_column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Subtopic handling
    subtopic_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    subtopic_required: Mapped[bool] = mapped_column(Boolean, default=False)
    
    high_yield_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    clinical_pearl: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    exam_relevance_score: Mapped[float] = mapped_column(Float, default=0.80)
    pyq_frequency: Mapped[int] = mapped_column(Integer, default=0)
    learning_objectives: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    common_mistake_patterns: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Provenance & Source Mapping
    source_mapping: Mapped[dict] = mapped_column(JSON, default=dict)
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED")  # 'VERIFIED', 'UNVERIFIED'
    syllabus_version: Mapped[str] = mapped_column(String(50), default="neet-pg-nmc-2026-v1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    topic: Mapped["Topic"] = relationship("Topic", back_populates="concepts", lazy="selectin")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="concept")
    mastery_records: Mapped[list["StudentConceptMastery"]] = relationship("StudentConceptMastery", back_populates="concept")
