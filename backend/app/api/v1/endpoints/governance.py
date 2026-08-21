from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.deps import get_current_reviewer_user, get_current_admin_user
from app.models.user import User
from app.models.question import Question, QuestionReport, QuestionQuarantineRegistry
from app.models.source import Source, EvidenceReference, PyqReference
from app.services.governance_service import GovernanceService
from app.services.multi_pass_validator import MultiPassValidatorService
from app.services.question_lifecycle_service import QuestionLifecycleService
from app.core.errors import NotFoundError, ValidationError

router = APIRouter()

class ReviewDecisionRequest(BaseModel):
    question_id: str
    verdict: str = Field(..., description="'APPROVE', 'REJECT', 'REQUEST_REVISION', 'QUARANTINE', 'MARK_OUTDATED'")
    clinical_notes: Optional[str] = None
    guideline_verified: bool = True

class CreateSourceRequest(BaseModel):
    title: str
    source_type: str = Field(..., description="'STANDARD_TEXTBOOK', 'GUIDELINE', 'OFFICIAL_DOCUMENT', 'PEER_REVIEWED_ARTICLE', 'QUESTION_BANK_REFERENCE', 'EXAM_ARCHIVE', 'OTHER'")
    edition: Optional[str] = None
    publication_year: Optional[int] = None
    publisher: Optional[str] = None
    chapter_reference: Optional[str] = None
    url: Optional[str] = None
    reference_identifier: Optional[str] = None

class CreateEvidenceRequest(BaseModel):
    question_id: str
    source_id: str
    fact_type: str = Field(..., description="'CORRECT_ANSWER_EVIDENCE', 'DISTRACTOR_REFUTATION', 'CLINICAL_PEARL', 'DIAGNOSTIC_CRITERION'")
    claim_snippet: str
    page_or_section: Optional[str] = None

class VerifyPyqRequest(BaseModel):
    concept_id: str
    exam_name: str = Field(default="NEET-PG")
    exam_year: int
    exam_session: Optional[str] = "Regular"
    pyq_status: str = Field(..., description="'REAL_PYQ', 'PYQ_DERIVED', 'PYQ_CONCEPT_LINKED', 'ORIGINAL', 'UNKNOWN'")
    source_reference: Optional[str] = None
    source_id: Optional[str] = None

@router.get("/dashboard")
async def get_governance_dashboard(
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin & Reviewer Content Governance Dashboard (Prompt 6, Sec 29).
    """
    stmt_all = select(func.count(Question.id))
    total_q = (await db.execute(stmt_all)).scalar() or 0

    stmt_ver = select(func.count(Question.id)).where(Question.status == "PUBLISHED")
    verified_q = (await db.execute(stmt_ver)).scalar() or 0

    stmt_pend = select(func.count(Question.id)).where(Question.status.in_(["REVIEW_REQUIRED", "AI_VALIDATED", "MEDICAL_REVIEW"]))
    pending_q = (await db.execute(stmt_pend)).scalar() or 0

    stmt_prop = select(func.count(Question.id)).where(Question.status == "PROPOSED")
    proposed_q = (await db.execute(stmt_prop)).scalar() or 0

    stmt_quar = select(func.count(Question.id)).where(Question.status == "QUARANTINED")
    quarantined_q = (await db.execute(stmt_quar)).scalar() or 0

    stmt_out = select(func.count(Question.id)).where(Question.status == "OUTDATED")
    outdated_q = (await db.execute(stmt_out)).scalar() or 0

    stmt_rep = select(func.count(QuestionReport.id)).where(QuestionReport.resolved == False)
    pending_reports = (await db.execute(stmt_rep)).scalar() or 0

    return {
        "total_questions": total_q,
        "verified_questions": verified_q,
        "review_pending": pending_q,
        "ai_proposed": proposed_q,
        "quarantined": quarantined_q,
        "outdated": outdated_q,
        "pending_student_reports": pending_reports
    }

@router.get("/coverage")
async def get_content_coverage(
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Curriculum Coverage & Gap Analytics (Prompt 6, Sec 30).
    """
    return await GovernanceService.get_content_coverage_matrix(db)

@router.post("/validate/{question_id}")
async def run_question_validation(
    question_id: str,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Runs multi-pass validation pipeline for a question.
    """
    result = await MultiPassValidatorService.run_multi_pass_validation(db, question_id)
    await db.commit()
    return result

@router.post("/review-decision")
async def submit_review_decision(
    req: ReviewDecisionRequest,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Executes doctor review action: APPROVE, REJECT, REQUEST_REVISION, QUARANTINE, MARK_OUTDATED.
    """
    question = await GovernanceService.execute_medical_review_decision(
        db=db,
        reviewer_id=current_user.id,
        question_id=req.question_id,
        verdict=req.verdict,
        clinical_notes=req.clinical_notes,
        guideline_verified=req.guideline_verified
    )
    await db.commit()
    return {
        "status": question.status,
        "trust_class": question.trust_class,
        "question_id": question.id
    }

@router.post("/sources", status_code=status.HTTP_201_CREATED)
async def register_source(
    req: CreateSourceRequest,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    source = Source(
        title=req.title,
        source_type=req.source_type.upper(),
        edition=req.edition,
        publication_year=req.publication_year,
        publisher=req.publisher,
        chapter_reference=req.chapter_reference,
        url=req.url,
        reference_identifier=req.reference_identifier,
        verified_by=current_user.id
    )
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return {"id": source.id, "title": source.title, "source_type": source.source_type}

@router.post("/evidence", status_code=status.HTTP_201_CREATED)
async def link_evidence_reference(
    req: CreateEvidenceRequest,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    evidence = EvidenceReference(
        question_id=req.question_id,
        source_id=req.source_id,
        fact_type=req.fact_type.upper(),
        claim_snippet=req.claim_snippet,
        page_or_section=req.page_or_section
    )
    db.add(evidence)
    await db.commit()
    return {"id": evidence.id, "question_id": req.question_id, "fact_type": evidence.fact_type}

@router.post("/pyq-verify", status_code=status.HTTP_201_CREATED)
async def verify_pyq_provenance(
    req: VerifyPyqRequest,
    current_user: User = Depends(get_current_reviewer_user),
    db: AsyncSession = Depends(get_db)
):
    pyq = PyqReference(
        concept_id=req.concept_id,
        exam_name=req.exam_name,
        exam_year=req.exam_year,
        exam_session=req.exam_session,
        pyq_status=req.pyq_status.upper(),
        source_reference=req.source_reference,
        source_id=req.source_id,
        verification_status="VERIFIED" if req.pyq_status.upper() == "REAL_PYQ" else "UNVERIFIED",
        verified_by_user_id=current_user.id
    )
    db.add(pyq)
    await db.commit()
    return {"id": pyq.id, "pyq_status": pyq.pyq_status, "verification_status": pyq.verification_status}
