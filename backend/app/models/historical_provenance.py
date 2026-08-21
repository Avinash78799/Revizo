import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class ProvenanceClassification(str, enum.Enum):
    OFFICIAL_PYQ = "OFFICIAL_PYQ"
    RECALL_CORROBORATED = "RECALL_CORROBORATED"
    RECALL_SINGLE_SOURCE = "RECALL_SINGLE_SOURCE"
    PYQ_PATTERN = "PYQ_PATTERN"
    UNVERIFIED_HISTORICAL = "UNVERIFIED_HISTORICAL"

class HistoricalProvenanceRecord(Base):
    __tablename__ = "historical_provenance_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=True, index=True)
    concept_id = Column(String(36), ForeignKey("concepts.id"), nullable=False, index=True)
    subject_id = Column(String(36), ForeignKey("subjects.id"), nullable=False, index=True)
    exam_year = Column(Integer, nullable=False, index=True) # e.g. 2021, 2022, 2023, 2024, 2025
    
    provenance_classification = Column(
        String(30),
        nullable=False,
        default=ProvenanceClassification.PYQ_PATTERN.value,
        index=True
    )
    
    source_url = Column(String(500), nullable=True)
    source_organization = Column(String(150), nullable=False)
    source_publication_date = Column(DateTime, nullable=True)
    source_type = Column(String(50), nullable=False) # 'OFFICIAL_BLUEPRINT', 'PUBLIC_ANALYSIS', 'RECALL_COMPILATION', 'FACULTY_REVIEW'
    exact_source_title = Column(String(255), nullable=False)
    
    is_memory_based = Column(Boolean, default=True, nullable=False)
    corroboration_count = Column(Integer, default=1, nullable=False)
    answer_key_agreement_status = Column(String(50), default="UNANIMOUS", nullable=False)
    medical_reviewer_status = Column(String(50), default="APPROVED", nullable=False)
    provenance_confidence = Column(String(20), default="HIGH", nullable=False)
    copyright_status = Column(String(80), default="PUBLIC_DOMAIN_FACT_STATEMENT", nullable=False)
    internal_provenance_id = Column(String(50), unique=True, nullable=False, index=True)
    
    clinical_vignette_style = Column(Boolean, default=True, nullable=False)
    repeated_frequency_score = Column(Integer, default=1, nullable=False) # Number of years/sessions concept appeared
    trend_category = Column(String(100), default="CLINICAL_APPLICATION") # 'CLINICAL_APPLICATION', 'PHARMACOLOGY_REGIMEN', 'DIAGNOSTIC_CRITERIA', 'INVESTIGATION_OF_CHOICE'
    takeaway_pearl = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    concept = relationship("Concept", lazy="joined")
    subject = relationship("Subject", lazy="joined")
