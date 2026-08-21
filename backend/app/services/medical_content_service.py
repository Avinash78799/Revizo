from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question, QuestionOption, QuestionReview, QuestionQualityScorecard, QuestionQuarantineRegistry, QuestionReport, QuestionVersion
from app.models.source import Source, PyqReference, SourceConflict, EvidenceReference
from app.models.taxonomy import Concept, Topic, Chapter, Subject, SyllabusRegistry, SyllabusSourceArtifact
from app.models.reviewer import MedicalReviewerProfile
from app.models.user import User
from app.core.datetime_util import utc_now
from app.core.errors import ValidationError, NotFoundError, AuthorizationError

class MedicalContentService:
    """
    Milestone 8.2 Medical Content Trust & Provenance Verification Engine (Prompt 12).
    - Strict Anti-Fabrication Invariants
    - Syllabus Provenance Verification Gate
    - Benchmark Provenance Verification Gate
    - PYQ Provenance Verification Gate
    - Source Provenance Verification Gate
    - Reviewer Audit Trail with Credential Snapshotting
    """

    HIGH_RISK_CATEGORIES = {
        "treatment_recommendation",
        "drug_dosing",
        "emergency_management",
        "pregnancy_safety",
        "pediatric_dosing",
        "contraindications",
        "guideline_sensitive",
        "source_conflict"
    }

    GOLD_BENCHMARK_CATEGORIES = [
        "single_best_answer",
        "multiple_correct",
        "no_correct_answer",
        "ambiguous_stem",
        "ambiguous_options",
        "outdated_guideline",
        "source_conflict",
        "clinical_contradiction",
        "hallucinated_citation",
        "fake_pyq",
        "unsafe_treatment",
        "incorrect_dose",
        "drug_contraindication",
        "pregnancy_safety",
        "pediatric_safety",
        "emergency_management"
    ]

    @classmethod
    async def verify_reviewer_eligibility(cls, db: AsyncSession, reviewer_id: str) -> MedicalReviewerProfile:
        """
        Ensures reviewer holds an active, verified medical credential (MBBS/MD/MS/DM/MCh).
        """
        stmt = select(MedicalReviewerProfile).where(MedicalReviewerProfile.user_id == reviewer_id)
        res = await db.execute(stmt)
        profile = res.scalars().first()

        if not profile:
            raise ValidationError(f"User {reviewer_id} does not have a registered Medical Reviewer Profile.")

        if profile.verification_status != "VERIFIED" or not profile.active_status:
            raise ValidationError(
                f"Reviewer {reviewer_id} is in status '{profile.verification_status}' (active={profile.active_status}). "
                "Only VERIFIED and ACTIVE medical reviewers can approve medical questions."
            )

        return profile

    @classmethod
    async def perform_medical_review(
        cls,
        db: AsyncSession,
        question_id: str,
        reviewer_id: str,
        verdict: str,  # 'APPROVE', 'REJECT', 'REQUEST_REVISION', 'QUARANTINE'
        clinical_notes: str,
        guideline_verified: bool = True
    ) -> Dict[str, Any]:
        """
        Executes human medical review with Credential Verification, Audit Snapshot, and Two-Person Review enforcement.
        """
        profile = await cls.verify_reviewer_eligibility(db, reviewer_id)

        now = utc_now()
        stmt_q = select(Question).options(selectinload(Question.reviews), selectinload(Question.source)).where(Question.id == question_id)
        res_q = await db.execute(stmt_q)
        q = res_q.scalars().first()

        if not q:
            raise NotFoundError(f"Question {question_id} not found")

        # Source Verification Gate (Prompt 12, Sec 4)
        source_rec = None
        if q.source_id:
            stmt_s = select(Source).where(Source.id == q.source_id)
            res_s = await db.execute(stmt_s)
            source_rec = res_s.scalars().first()

        if verdict == "APPROVE" and source_rec:
            if source_rec.verification_status != "VERIFIED":
                raise ValidationError(
                    f"Cannot approve question relying on unverified source '{source_rec.title}' (status: {source_rec.verification_status})."
                )

        if verdict == "APPROVE":
            # Two-Person Review Gate for High-Risk Content
            if q.is_high_risk or (q.high_risk_category in cls.HIGH_RISK_CATEGORIES):
                if q.first_reviewer_id and q.first_reviewer_id == reviewer_id:
                    raise ValidationError("Two-person review requires two distinct medical doctors. Same reviewer cannot approve twice.")

        # Record Review Decision with Full Immutable Audit Snapshot (Prompt 12, Sec 5)
        rev = QuestionReview(
            question_id=question_id,
            reviewer_id=reviewer_id,
            verdict=verdict,
            question_version=q.content_version,
            reviewer_credential_status=f"{profile.credential_type}_{profile.verification_status}",
            source_verification_decision="VERIFIED" if (source_rec and source_rec.verification_status == "VERIFIED") else "NO_SOURCE_OR_UNVERIFIED",
            guideline_verification_decision="VERIFIED" if guideline_verified else "UNVERIFIED",
            clinical_notes=clinical_notes,
            guideline_verified=guideline_verified,
            created_at=now
        )
        db.add(rev)

        if q.is_high_risk and q.first_reviewer_id and not q.second_reviewer_id:
            q.second_reviewer_id = reviewer_id
            q.second_reviewed_at = now

        if verdict == "REJECT":
            if q.is_high_risk and q.first_reviewer_id:
                # Disagreement on high-risk content -> Route to Medical Board Quarantine
                q.status = "QUARANTINED"
                q.trust_class = "QUARANTINED"
                quarantine = QuestionQuarantineRegistry(
                    question_id=question_id,
                    quarantine_reason=f"High-Risk Review Disagreement: Doctor A approved, Doctor B rejected. Rationale: {clinical_notes}",
                    resolution_status="quarantined",
                    audit_notes=clinical_notes
                )
                db.add(quarantine)
            else:
                q.status = "REJECTED"
                q.trust_class = "WITHDRAWN"
        elif verdict == "QUARANTINE":
            q.status = "QUARANTINED"
            q.trust_class = "QUARANTINED"
            quarantine = QuestionQuarantineRegistry(
                question_id=question_id,
                quarantine_reason=f"Doctor Review Quarantine: {clinical_notes}",
                resolution_status="quarantined",
                audit_notes=clinical_notes
            )
            db.add(quarantine)
        elif verdict == "REQUEST_REVISION":
            q.status = "REVISION_REQUESTED"
        elif verdict == "APPROVE":
            # Two-Person Review Gate for High-Risk Content
            if q.is_high_risk or (q.high_risk_category in cls.HIGH_RISK_CATEGORIES):
                if not q.first_reviewer_id:
                    q.first_reviewer_id = reviewer_id
                    q.first_reviewed_at = now
                    q.status = "REVIEW_PENDING"  # Waiting for second doctor
                else:
                    q.second_reviewer_id = reviewer_id
                    q.second_reviewed_at = now
                    q.status = "APPROVED"
                    q.trust_class = "VERIFIED_CORE_QUESTION"
            else:
                q.reviewed_by = reviewer_id
                q.reviewed_at = now
                q.status = "APPROVED"
                q.trust_class = "VERIFIED_CORE_QUESTION"

        await db.commit()
        return {
            "question_id": q.id,
            "verdict": verdict,
            "status": q.status,
            "trust_class": q.trust_class,
            "is_high_risk": q.is_high_risk,
            "first_reviewer_id": q.first_reviewer_id,
            "second_reviewer_id": q.second_reviewer_id,
            "audit_trail_recorded": True
        }

    @classmethod
    async def verify_syllabus_source_provenance(
        cls,
        db: AsyncSession,
        syllabus_version: str,
        document_identifier: str,
        document_hash: str,
        source_name: str,
        source_url: str,
        effective_date: str,
        verifier_id: str,
        verification_notes: str
    ) -> Dict[str, Any]:
        """
        Authoritative Syllabus Provenance Verification Gate (Prompt 12, Sec 1).
        Transitions syllabus from UNVERIFIED to VERIFIED only when full provenance evidence is supplied.
        """
        if not document_identifier or not document_hash or not verifier_id:
            raise ValidationError("Cannot verify syllabus without authoritative document identifier, document hash, and verifier identity.")

        now = utc_now()
        stmt_reg = select(SyllabusRegistry).where(SyllabusRegistry.syllabus_version == syllabus_version)
        res_reg = await db.execute(stmt_reg)
        reg = res_reg.scalars().first()

        if not reg:
            reg = SyllabusRegistry(
                syllabus_version=syllabus_version,
                source=source_name,
                effective_date=effective_date,
                verification_status="VERIFIED",
                import_timestamp=now
            )
            db.add(reg)
        else:
            reg.verification_status = "VERIFIED"

        artifact = SyllabusSourceArtifact(
            syllabus_version=syllabus_version,
            source_name=source_name,
            source_url=source_url,
            document_identifier=document_identifier,
            document_hash=document_hash,
            effective_date=effective_date,
            verification_status="VERIFIED",
            verified_by=verifier_id,
            verification_timestamp=now
        )
        db.add(artifact)

        await db.commit()
        return {
            "syllabus_version": syllabus_version,
            "verification_status": "VERIFIED",
            "document_identifier": document_identifier,
            "document_hash": document_hash,
            "verified_by": verifier_id,
            "verified_at": now.isoformat()
        }

    @classmethod
    async def verify_source_provenance(
        cls,
        db: AsyncSession,
        source_id: str,
        verifier_id: str,
        reference_identifier: str,
        edition: str,
        publisher: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Medical Source Provenance Verification Gate (Prompt 12, Sec 4).
        """
        if not reference_identifier or not verifier_id or not edition:
            raise ValidationError("Cannot verify medical source without reference identifier (ISBN/DOI), edition, and verifier identity.")

        stmt = select(Source).where(Source.id == source_id)
        res = await db.execute(stmt)
        source = res.scalars().first()

        if not source:
            raise NotFoundError(f"Source {source_id} not found")

        now = utc_now()
        source.verification_status = "VERIFIED"
        source.verified_by = verifier_id
        source.verified_at = now
        source.reference_identifier = reference_identifier
        source.edition = edition
        source.publisher = publisher
        source.notes = notes

        await db.commit()
        return {
            "source_id": source.id,
            "title": source.title,
            "verification_status": source.verification_status,
            "reference_identifier": source.reference_identifier,
            "verified_by": verifier_id
        }

    @classmethod
    async def verify_pyq_provenance(
        cls,
        db: AsyncSession,
        pyq_ref_id: str,
        verifier_id: str,
        is_verified: bool,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        PYQ Provenance Verification Gate (Prompt 12, Sec 3).
        """
        stmt = select(PyqReference).options(selectinload(PyqReference.questions)).where(PyqReference.id == pyq_ref_id)
        res = await db.execute(stmt)
        ref = res.scalars().first()

        if not ref:
            raise NotFoundError(f"PYQ reference {pyq_ref_id} not found")

        now = utc_now()
        ref.verification_status = "VERIFIED" if is_verified else "UNVERIFIED"
        ref.pyq_status = "VERIFIED_PYQ" if is_verified else "UNVERIFIED"
        ref.verified_by_user_id = verifier_id
        ref.verified_at = now if is_verified else None
        ref.historical_notes = notes

        for q in ref.questions:
            if is_verified and q.status == "APPROVED":
                q.trust_class = "VERIFIED_PYQ"
            elif not is_verified:
                if q.trust_class == "VERIFIED_PYQ":
                    q.trust_class = "SOURCE_REFERENCED"

        await db.commit()
        return {
            "pyq_ref_id": ref.id,
            "exam_name": ref.exam_name,
            "exam_year": ref.exam_year,
            "pyq_status": ref.pyq_status,
            "verification_status": ref.verification_status,
            "verified_by": verifier_id
        }

    @classmethod
    def evaluate_quality_scorecard_with_hard_gates(
        cls,
        clinical_accuracy_passed: bool,
        medical_accuracy_passed: bool,
        single_best_answer_passed: bool,
        source_support_passed: bool,
        clinical_accuracy_score: float = 1.0,
        single_best_answer_score: float = 1.0,
        distractor_quality_score: float = 0.85,
        exam_relevance_score: float = 0.80,
        source_support_score: float = 1.0,
        explanation_quality_score: float = 0.90,
        novelty_score: float = 0.85
    ) -> Dict[str, Any]:
        overall_score = round(
            (clinical_accuracy_score * 0.30) +
            (single_best_answer_score * 0.25) +
            (source_support_score * 0.15) +
            (distractor_quality_score * 0.10) +
            (explanation_quality_score * 0.10) +
            (exam_relevance_score * 0.10),
            2
        )

        gate_status = "PASSED"
        failed_gate = None
        failure_reason = None

        if not clinical_accuracy_passed or not medical_accuracy_passed:
            gate_status = "CRITICAL_FAILURE_HARD_REJECT"
            failed_gate = "CLINICAL_ACCURACY_FAILURE"
            failure_reason = "Question failed fundamental clinical or medical correctness check."
        elif not single_best_answer_passed:
            gate_status = "CRITICAL_FAILURE_HARD_REJECT"
            failed_gate = "SINGLE_BEST_ANSWER_FAILURE"
            failure_reason = "Multiple defensible answers or no scientifically sound answer detected."
        elif not source_support_passed:
            gate_status = "CRITICAL_FAILURE_HARD_REJECT"
            failed_gate = "SOURCE_SUPPORT_FAILURE"
            failure_reason = "Unsupported claim or missing authoritative citation."

        return {
            "overall_quality_score": overall_score,
            "quality_gate_status": gate_status,
            "failed_gate": failed_gate,
            "failure_reason": failure_reason,
            "clinical_accuracy_score": clinical_accuracy_score,
            "single_best_answer_score": single_best_answer_score,
            "distractor_quality_score": distractor_quality_score,
            "exam_relevance_score": exam_relevance_score,
            "source_support_score": source_support_score,
            "explanation_quality_score": explanation_quality_score,
            "novelty_score": novelty_score
        }

    @classmethod
    def calculate_evidence_backed_high_yield_score(
        cls,
        verified_pyq_count: int,
        clinical_importance_score: float = 0.50,
        curriculum_centrality_score: float = 0.50
    ) -> Dict[str, Any]:
        pyq_component = min(1.0, verified_pyq_count * 0.25) if verified_pyq_count > 0 else 0.00
        
        final_score = round(
            (pyq_component * 0.40) +
            (clinical_importance_score * 0.30) +
            (curriculum_centrality_score * 0.30),
            2
        )

        display_badge = "Historically high-yield practice" if final_score >= 0.70 else "Standard practice topic"

        return {
            "high_yield_score": final_score,
            "pyq_recurrence_component": pyq_component,
            "clinical_importance_component": clinical_importance_score,
            "curriculum_centrality_component": curriculum_centrality_score,
            "evidence_count": verified_pyq_count,
            "display_label": display_badge
        }

    @classmethod
    async def register_source_conflict(
        cls,
        db: AsyncSession,
        concept_id: str,
        source_a_id: str,
        source_b_id: str,
        conflicting_claim: str,
        specialty: Optional[str] = None,
        jurisdiction: Optional[str] = None
    ) -> SourceConflict:
        conflict = SourceConflict(
            concept_id=concept_id,
            source_a_id=source_a_id,
            source_b_id=source_b_id,
            conflicting_claim=conflicting_claim,
            specialty=specialty,
            jurisdiction=jurisdiction,
            status="REVIEW_REQUIRED"
        )
        db.add(conflict)

        stmt_q = select(Question).where(Question.concept_id == concept_id)
        res_q = await db.execute(stmt_q)
        questions = res_q.scalars().all()
        for q in questions:
            q.is_high_risk = True
            q.high_risk_category = "source_conflict"

        await db.commit()
        await db.refresh(conflict)
        return conflict

    @classmethod
    async def process_student_question_report(
        cls,
        db: AsyncSession,
        question_id: str,
        user_id: str,
        report_type: str,
        comment: Optional[str] = None,
        severity: str = "NORMAL",
        is_serious_medical_error: bool = False
    ) -> Dict[str, Any]:
        """
        Milestone 14: Student Medical Feedback & Immediate Safety Quarantine.
        Stores student feedback report with question version and attempt context.
        If severity == 'CRITICAL' or is_serious_medical_error == True:
        Immediately triggers QUARANTINE on the question, isolating it from all future test generations.
        """
        stmt_q = select(Question).where(Question.id == question_id)
        q = (await db.execute(stmt_q)).scalars().first()
        if not q:
            raise NotFoundError(f"Question '{question_id}' not found.")

        is_critical = (
            severity.upper() == "CRITICAL"
            or is_serious_medical_error
            or (report_type in ["WRONG_ANSWER_KEY", "OUTDATED", "INCORRECT_EXPLANATION", "SOURCE_CONCERN"] and severity.upper() == "HIGH")
        )

        report = QuestionReport(
            question_id=question_id,
            user_id=user_id,
            reason=report_type,
            comment=comment,
            is_serious_medical_error=is_critical,
            created_at=utc_now()
        )
        db.add(report)

        quarantined = False
        if is_critical:
            q.status = "QUARANTINED"
            q.trust_class = "QUARANTINED"
            quarantine_record = QuestionQuarantineRegistry(
                question_id=question_id,
                quarantine_reason=f"Student Critical Safety Report: {report_type} - {comment or 'No details'}",
                resolution_status="quarantined",
                audit_notes=f"Reported by student user {user_id}. Critical severity flagged."
            )
            db.add(quarantine_record)
            quarantined = True

        await db.commit()
        return {
            "report_id": report.id,
            "question_id": question_id,
            "report_type": report_type,
            "is_critical": is_critical,
            "quarantined": quarantined,
            "current_question_status": q.status,
            "current_trust_class": q.trust_class
        }
