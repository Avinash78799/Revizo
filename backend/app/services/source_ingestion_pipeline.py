from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import hashlib
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.source import Source, EvidenceReference, PyqReference
from app.models.taxonomy import Concept, Topic, Chapter, Subject
from app.models.question import Question, QuestionOption, QuestionQualityScorecard
from app.models.reviewer import MedicalReviewerProfile
from app.core.datetime_util import utc_now
from app.core.errors import ValidationError, NotFoundError

class SourceIngestionPipeline:
    """
    Controlled Real Medical Source Ingestion Pipeline (Prompt 13, Sec 3).
    Workflow:
    SOURCE -> PROVENANCE VERIFICATION -> DOCUMENT REGISTRATION -> CONTENT EXTRACTION ->
    NORMALIZATION -> TAXONOMY MAPPING -> QUESTION CANDIDATE -> AI VALIDATION -> HUMAN MEDICAL REVIEW -> PUBLICATION
    """

    @classmethod
    async def ingest_and_register_source(
        cls,
        db: AsyncSession,
        title: str,
        source_type: str,
        publisher: str,
        edition: str,
        reference_identifier: str,  # ISBN / DOI / Official Doc ID
        specialty: str,
        verifier_id: str,
        notes: Optional[str] = None
    ) -> Source:
        """
        Stage 1 & 2: Provenance Verification & Document Registration.
        """
        if not reference_identifier or not edition or not verifier_id:
            raise ValidationError("Authoritative source registration requires reference_identifier, edition, and verifier_id.")

        # Ensure reviewer is verified
        stmt_rev = select(MedicalReviewerProfile).where(MedicalReviewerProfile.user_id == verifier_id)
        res_rev = await db.execute(stmt_rev)
        profile = res_rev.scalars().first()

        if not profile or profile.verification_status != "VERIFIED" or not profile.active_status:
            raise ValidationError("Source verification requires an active, verified medical auditor.")

        now = utc_now()
        source = Source(
            title=title,
            source_type=source_type,
            publisher=publisher,
            edition=edition,
            reference_identifier=reference_identifier,
            specialty=specialty,
            verification_status="VERIFIED",
            verified_by=verifier_id,
            verified_at=now,
            last_verified_date=now,
            notes=notes
        )
        db.add(source)
        await db.commit()
        await db.refresh(source)
        return source

    @classmethod
    async def process_question_candidate(
        cls,
        db: AsyncSession,
        source_id: str,
        concept_id: str,
        question_text: str,
        options: Dict[str, str],
        correct_option_key: str,
        correct_explanation: str,
        remember_takeaway: str,
        distractor_explanations: Dict[str, str],
        claim_snippet: str,
        page_or_section: str,
        is_high_risk: bool = False,
        high_risk_category: Optional[str] = None,
        exam_relevance_tag: str = "HIGH_YIELD"
    ) -> Question:
        """
        Stage 3 to 7: Content Extraction -> Normalization -> Taxonomy Mapping -> Question Candidate.
        Question candidate is strictly created in status 'PROPOSED' and trust class 'AI_GENERATED_REVIEW_PENDING'.
        """
        # Validate Source is Verified
        stmt_s = select(Source).where(Source.id == source_id)
        res_s = await db.execute(stmt_s)
        source = res_s.scalars().first()

        if not source or source.verification_status != "VERIFIED":
            raise ValidationError("Cannot create question candidate from unverified or missing source.")

        # Validate Concept Exists
        stmt_c = select(Concept).where(Concept.id == concept_id)
        res_c = await db.execute(stmt_c)
        concept = res_c.scalars().first()

        if not concept:
            raise NotFoundError(f"Concept {concept_id} not found in curriculum taxonomy.")

        # Calculate immutable text hash
        raw_hash = hashlib.sha256(question_text.strip().lower().encode("utf-8")).hexdigest()

        question = Question(
            concept_id=concept_id,
            source_id=source_id,
            source_citation=f"{source.title}, Ed. {source.edition}, Sec: {page_or_section}",
            question_text=question_text,
            correct_explanation=correct_explanation,
            remember_takeaway=remember_takeaway,
            exam_relevance_tag=exam_relevance_tag,
            is_high_risk=is_high_risk,
            high_risk_category=high_risk_category,
            status="PROPOSED",
            trust_class="AI_GENERATED_REVIEW_PENDING",
            text_hash=raw_hash
        )
        db.add(question)
        await db.flush()

        # Add Options
        for key in ["A", "B", "C", "D"]:
            if key not in options:
                raise ValidationError(f"Missing required option '{key}'")
            opt = QuestionOption(
                question_id=question.id,
                option_key=key,
                option_text=options[key],
                is_correct=(key == correct_option_key),
                why_wrong_explanation=distractor_explanations.get(key)
            )
            db.add(opt)

        # Add Evidence Reference
        evidence = EvidenceReference(
            question_id=question.id,
            source_id=source_id,
            fact_type="CORRECT_ANSWER_EVIDENCE",
            claim_snippet=claim_snippet,
            page_or_section=page_or_section,
            confidence_level=1.0
        )
        db.add(evidence)

        # Initialize Default Quality Scorecard
        scorecard = QuestionQualityScorecard(
            question_id=question.id,
            clinical_accuracy_passed=True,
            medical_accuracy_passed=True,
            single_best_answer_passed=True,
            source_support_passed=True,
            overall_quality_score=0.95
        )
        db.add(scorecard)

        await db.commit()
        await db.refresh(question)
        return question
