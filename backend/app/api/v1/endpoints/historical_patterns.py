from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.taxonomy import Subject, Concept, Topic, Chapter
from app.models.historical_provenance import HistoricalProvenanceRecord, ProvenanceClassification

router = APIRouter()

@router.get("/summary", status_code=status.HTTP_200_OK)
async def get_historical_patterns_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns aggregate historical exam trend analytics across NEET-PG years:
    - Most repeated clinical concepts
    - High-frequency topics
    - Subject-wise distribution
    - Clinical vignette vs direct fact ratio
    - Recurring pharmacology & investigation themes
    - Strict 0 verified PYQ governance status
    """
    # 1. Fetch all provenance records
    stmt = select(HistoricalProvenanceRecord).options(
        selectinload(HistoricalProvenanceRecord.concept),
        selectinload(HistoricalProvenanceRecord.subject)
    ).order_by(desc(HistoricalProvenanceRecord.repeated_frequency_score))
    
    result = await db.execute(stmt)
    records = result.scalars().all()

    # 2. Subject distribution
    subj_dist: Dict[str, int] = {}
    category_dist: Dict[str, int] = {}
    years_represented = set()
    clinical_vignette_count = 0
    total_records = len(records)

    repeated_concepts = []
    for r in records:
        s_name = r.subject.name if r.subject else "General Medicine"
        subj_dist[s_name] = subj_dist.get(s_name, 0) + 1
        category_dist[r.trend_category] = category_dist.get(r.trend_category, 0) + 1
        years_represented.add(r.exam_year)
        if r.clinical_vignette_style:
            clinical_vignette_count += 1
            
        repeated_concepts.append({
            "id": r.id,
            "internal_id": r.internal_provenance_id,
            "concept_name": r.concept.name if r.concept else r.exact_source_title,
            "subject_name": s_name,
            "exam_year": r.exam_year,
            "frequency_score": r.repeated_frequency_score,
            "category": r.trend_category,
            "provenance_classification": r.provenance_classification,
            "source_organization": r.source_organization,
            "corroboration_count": r.corroboration_count,
            "takeaway_pearl": r.takeaway_pearl
        })

    clinical_ratio = round((clinical_vignette_count / max(1, total_records)) * 100, 1)

    return {
        "status": "success",
        "governance_notice": {
            "verified_pyq_count": 0,
            "disclaimer": "VERIFIED_PYQ remains strictly 0. All patterns are original Revizo clinical questions modeled on multi-source corroborated historical recall trends.",
            "sources_analyzed": "NBEMS Sample Blueprints, Careers360, Shiksha, AglaSem, and Medical Faculty Recall Compilations."
        },
        "total_historical_patterns": total_records,
        "years_analyzed": sorted(list(years_represented)),
        "clinical_vignette_percentage": clinical_ratio,
        "subject_distribution": subj_dist,
        "category_breakdown": category_dist,
        "most_repeated_concepts": repeated_concepts[:15]
    }

@router.get("/provenance", status_code=status.HTTP_200_OK)
async def get_provenance_records(
    year: Optional[int] = Query(None, description="Filter by exam year"),
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    category: Optional[str] = Query(None, description="Filter by trend category"),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Searchable provenance registry for student transparency.
    """
    stmt = select(HistoricalProvenanceRecord).options(
        selectinload(HistoricalProvenanceRecord.concept),
        selectinload(HistoricalProvenanceRecord.subject)
    )

    if year:
        stmt = stmt.where(HistoricalProvenanceRecord.exam_year == year)
    if subject_id:
        stmt = stmt.where(HistoricalProvenanceRecord.subject_id == subject_id)
    if category:
        stmt = stmt.where(HistoricalProvenanceRecord.trend_category == category)

    stmt = stmt.order_by(desc(HistoricalProvenanceRecord.repeated_frequency_score)).limit(limit)
    result = await db.execute(stmt)
    records = result.scalars().all()

    return [
        {
            "id": r.id,
            "internal_provenance_id": r.internal_provenance_id,
            "concept_name": r.concept.name if r.concept else r.exact_source_title,
            "subject_name": r.subject.name if r.subject else "Medical Discipline",
            "exam_year": r.exam_year,
            "provenance_classification": r.provenance_classification,
            "source_organization": r.source_organization,
            "source_type": r.source_type,
            "exact_source_title": r.exact_source_title,
            "corroboration_count": r.corroboration_count,
            "answer_key_agreement_status": r.answer_key_agreement_status,
            "medical_reviewer_status": r.medical_reviewer_status,
            "provenance_confidence": r.provenance_confidence,
            "repeated_frequency_score": r.repeated_frequency_score,
            "trend_category": r.trend_category,
            "takeaway_pearl": r.takeaway_pearl
        }
        for r in records
    ]
