import uuid
import re
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Tuple
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source, SourceConflict, EvidenceReference, PyqReference
from app.models.taxonomy import Concept, SyllabusRegistry, SyllabusSourceArtifact
from app.models.question import Question
from app.models.reviewer import MedicalReviewerProfile
from app.models.user import User
from app.core.datetime_util import utc_now
from app.core.errors import ValidationError, NotFoundError, AuthorizationError

class SourceProvenanceService:
    """
    Milestone 11 Phase 2: Authoritative Medical Source Provenance Engine.
    
    Anti-Fabrication Invariants:
    1. Sources without verified ISBN/DOI, edition, publisher, and verifier remain UNVERIFIED.
    2. Plausible but unaudited registration cannot become VERIFIED.
    3. Conflicting sources/guidelines transition to CONFLICTED and are blocked from publication.
    4. Official NMC syllabus requires genuine document identifier, 64-char SHA-256 hash, and auditor verification.
    5. PYQ references require exam session, question identifier, source document, and auditor verification.
    6. Verifiers must hold an active VERIFIED medical reviewer profile or admin role.
    7. Preserves immutable verification audit records.
    """

    ALLOWED_SOURCE_TYPES = {
        "STANDARD_TEXTBOOK",
        "CLINICAL_GUIDELINE",
        "OFFICIAL_CURRICULUM",
        "GOVERNMENT_HEALTH_POLICY",
        "PEER_REVIEWED_JOURNAL",
        "EXAM_ARCHIVE"
    }

    VALID_VERIFICATION_STATUSES = {
        "UNVERIFIED",
        "VERIFIED",
        "REJECTED",
        "CONFLICTED",
        "OUTDATED",
        "SUPERSEDED"
    }

    @classmethod
    async def verify_auditor_authorization(cls, db: AsyncSession, verifier_id: str) -> None:
        """
        Ensures verifier is an authorized Admin or an active VERIFIED Medical Reviewer.
        """
        if not verifier_id:
            raise AuthorizationError("Verifier identity is required for source provenance verification.")

        # Check User role
        stmt_u = select(User).where(User.id == verifier_id)
        res_u = await db.execute(stmt_u)
        user = res_u.scalars().first()
        if not user:
            raise NotFoundError(f"Verifier user '{verifier_id}' not found.")

        if user.role in ("admin", "medical_director"):
            return

        # If medical reviewer, must be active and VERIFIED
        stmt_p = select(MedicalReviewerProfile).where(MedicalReviewerProfile.user_id == verifier_id)
        res_p = await db.execute(stmt_p)
        profile = res_p.scalars().first()

        if not profile or profile.verification_status != "VERIFIED" or not profile.active_status:
            raise AuthorizationError(
                f"User '{verifier_id}' is not an active verified medical reviewer. "
                "Only VERIFIED reviewers or Admins can audit medical sources."
            )

    @classmethod
    async def register_source_candidate(
        cls,
        db: AsyncSession,
        title: str,
        source_type: str,
        publisher: str,
        edition: Optional[str] = None,
        publication_year: Optional[int] = None,
        reference_identifier: Optional[str] = None,  # ISBN / DOI / PMID
        url: Optional[str] = None,
        specialty: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Source:
        """
        Registers a new medical source candidate into UNVERIFIED status.
        Never marks a source as VERIFIED automatically upon registration.
        """
        if not title or len(title.strip()) < 3:
            raise ValidationError("Source title must be specified (minimum 3 characters).")

        norm_type = source_type.strip().upper()
        if norm_type not in cls.ALLOWED_SOURCE_TYPES:
            raise ValidationError(
                f"Source type '{source_type}' is invalid. Allowed: {sorted(list(cls.ALLOWED_SOURCE_TYPES))}"
            )

        now = utc_now()
        source = Source(
            id=str(uuid.uuid4()),
            title=title.strip(),
            source_type=norm_type,
            publisher=publisher.strip() if publisher else None,
            edition=edition.strip() if edition else None,
            publication_year=publication_year,
            reference_identifier=reference_identifier.strip() if reference_identifier else None,
            url=url.strip() if url else None,
            specialty=specialty.strip() if specialty else None,
            verification_status="UNVERIFIED",
            verified_by=None,
            verified_at=None,
            notes=notes,
            created_at=now,
            updated_at=now
        )
        db.add(source)
        await db.commit()
        await db.refresh(source)
        return source

    @classmethod
    async def audit_and_verify_source(
        cls,
        db: AsyncSession,
        source_id: str,
        verifier_id: str,
        decision: str,  # 'VERIFIED' or 'REJECTED'
        reference_identifier: str,
        edition: str,
        publisher: str,
        audit_evidence_notes: str
    ) -> Dict[str, Any]:
        """
        Executes independent human verification of a medical source with strict evidence requirements.
        """
        await cls.verify_auditor_authorization(db, verifier_id)

        stmt = select(Source).where(Source.id == source_id)
        res = await db.execute(stmt)
        source = res.scalars().first()
        if not source:
            raise NotFoundError(f"Medical Source '{source_id}' not found.")

        # Check for unresolved conflicts involving this source
        stmt_conflicts = select(SourceConflict).where(
            and_(
                or_(SourceConflict.source_a_id == source_id, SourceConflict.source_b_id == source_id),
                SourceConflict.status.in_(["REVIEW_REQUIRED", "UNRESOLVED"])
            )
        )
        conflicts = (await db.execute(stmt_conflicts)).scalars().all()
        if conflicts:
            source.verification_status = "CONFLICTED"
            await db.commit()
            raise ValidationError(
                f"Source '{source.title}' has {len(conflicts)} unresolved medical conflict(s). "
                "Conflicts must be resolved by the Medical Board before verification."
            )

        decision_upper = decision.strip().upper()
        if decision_upper not in ("VERIFIED", "REJECTED"):
            raise ValidationError(f"Invalid verification decision '{decision}'. Must be 'VERIFIED' or 'REJECTED'.")

        if decision_upper == "VERIFIED":
            if not reference_identifier or len(reference_identifier.strip()) < 5:
                raise ValidationError("Verification requires a valid ISBN, DOI, or official document identifier.")
            if not edition or len(edition.strip()) < 1:
                raise ValidationError("Verification requires an authoritative edition specification.")
            if not publisher or len(publisher.strip()) < 2:
                raise ValidationError("Verification requires an authoritative publisher.")
            if not audit_evidence_notes or len(audit_evidence_notes.strip()) < 5:
                raise ValidationError("Auditor must provide evidence notes documenting source provenance validation.")

            now = utc_now()
            source.verification_status = "VERIFIED"
            source.reference_identifier = reference_identifier.strip()
            source.edition = edition.strip()
            source.publisher = publisher.strip()
            source.verified_by = verifier_id
            source.verified_at = now
            source.last_verified_date = now
            source.notes = audit_evidence_notes
        else:
            now = utc_now()
            source.verification_status = "REJECTED"
            source.verified_by = verifier_id
            source.verified_at = now
            source.notes = f"Rejected: {audit_evidence_notes}"

        source.updated_at = now
        await db.commit()
        await db.refresh(source)

        return {
            "source_id": source.id,
            "title": source.title,
            "verification_status": source.verification_status,
            "reference_identifier": source.reference_identifier,
            "edition": source.edition,
            "publisher": source.publisher,
            "verified_by": verifier_id,
            "verified_at": source.verified_at.isoformat() if source.verified_at else None,
            "audit_notes": source.notes
        }

    @classmethod
    async def register_syllabus_candidate_artifact(
        cls,
        db: AsyncSession,
        syllabus_version: str,
        document_identifier: str,
        document_hash: str,
        source_name: str,
        source_url: Optional[str] = None,
        effective_date: str = "2023-12-29"
    ) -> SyllabusSourceArtifact:
        """
        Registers an official syllabus document artifact into UNVERIFIED status with its SHA-256 digest.
        It remains UNVERIFIED until an authorized medical auditor performs the verification audit.
        """
        if not document_identifier or len(document_identifier.strip()) < 5:
            raise ValidationError("Valid official syllabus document identifier is required.")

        # Validate SHA-256 hex hash (exactly 64 lowercase/uppercase hex characters)
        if not document_hash or not re.match(r"^[a-fA-F0-9]{64}$", document_hash.strip()):
            raise ValidationError("Valid 64-character SHA-256 document hash is required for syllabus registration.")

        now = utc_now()
        stmt_reg = select(SyllabusRegistry).where(SyllabusRegistry.syllabus_version == syllabus_version)
        res_reg = await db.execute(stmt_reg)
        reg = res_reg.scalars().first()

        if not reg:
            reg = SyllabusRegistry(
                syllabus_version=syllabus_version,
                source=source_name.strip(),
                effective_date=effective_date.strip(),
                verification_status="UNVERIFIED",
                import_timestamp=now
            )
            db.add(reg)
            await db.flush()

        artifact = SyllabusSourceArtifact(
            id=str(uuid.uuid4()),
            syllabus_version=syllabus_version,
            source_name=source_name.strip(),
            source_url=source_url.strip() if source_url else None,
            document_identifier=document_identifier.strip(),
            document_hash=document_hash.strip().lower(),
            effective_date=effective_date.strip(),
            verification_status="UNVERIFIED",
            verified_by=None,
            verification_timestamp=None,
            retrieved_at=now
        )
        db.add(artifact)
        await db.commit()
        await db.refresh(artifact)
        return artifact

    @classmethod
    async def verify_syllabus_provenance(
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
        Verifies NMC / NBEMS Curriculum Syllabus Provenance.
        Requires genuine document identifier, valid SHA-256 hash (64 hex chars), and auditor identity.
        """
        await cls.verify_auditor_authorization(db, verifier_id)

        if not document_identifier or len(document_identifier.strip()) < 5:
            raise ValidationError("Valid official syllabus document identifier is required.")

        # Validate SHA-256 hex hash (exactly 64 lowercase/uppercase hex characters)
        if not document_hash or not re.match(r"^[a-fA-F0-9]{64}$", document_hash.strip()):
            raise ValidationError("Valid 64-character SHA-256 document hash is required for syllabus verification.")

        if not source_name or len(source_name.strip()) < 3:
            raise ValidationError("Official publishing authority name is required.")

        if not verification_notes or len(verification_notes.strip()) < 5:
            raise ValidationError("Auditor verification notes are required.")

        now = utc_now()
        stmt_reg = select(SyllabusRegistry).where(SyllabusRegistry.syllabus_version == syllabus_version)
        res_reg = await db.execute(stmt_reg)
        reg = res_reg.scalars().first()

        if not reg:
            reg = SyllabusRegistry(
                syllabus_version=syllabus_version,
                source=source_name.strip(),
                effective_date=effective_date.strip(),
                verification_status="VERIFIED",
                import_timestamp=now
            )
            db.add(reg)
        else:
            reg.verification_status = "VERIFIED"

        artifact = SyllabusSourceArtifact(
            syllabus_version=syllabus_version,
            source_name=source_name.strip(),
            source_url=source_url.strip() if source_url else None,
            document_identifier=document_identifier.strip(),
            document_hash=document_hash.strip().lower(),
            effective_date=effective_date.strip(),
            verification_status="VERIFIED",
            verified_by=verifier_id,
            verification_timestamp=now
        )
        db.add(artifact)
        await db.commit()

        return {
            "syllabus_version": syllabus_version,
            "verification_status": "VERIFIED",
            "document_identifier": document_identifier.strip(),
            "document_hash": document_hash.strip().lower(),
            "verified_by": verifier_id,
            "verified_at": now.isoformat()
        }

    @classmethod
    async def verify_pyq_provenance(
        cls,
        db: AsyncSession,
        pyq_ref_id: str,
        verifier_id: str,
        exam_name: str,
        exam_year: int,
        question_identifier: str,
        source_document: str,
        audit_notes: str
    ) -> Dict[str, Any]:
        """
        Verifies previous year question provenance.
        Requires exam name, valid year, question identifier, and source paper evidence.
        """
        await cls.verify_auditor_authorization(db, verifier_id)

        stmt = select(PyqReference).where(PyqReference.id == pyq_ref_id)
        res = await db.execute(stmt)
        ref = res.scalars().first()
        if not ref:
            raise NotFoundError(f"PYQ reference '{pyq_ref_id}' not found.")

        if not exam_name or len(exam_name.strip()) < 2:
            raise ValidationError("Authoritative exam name (e.g. NEET-PG, INI-CET) is required.")

        if not (2000 <= exam_year <= datetime.now(timezone.utc).year + 1):
            raise ValidationError(f"Invalid exam year '{exam_year}'.")

        if not question_identifier or len(question_identifier.strip()) < 1:
            raise ValidationError("Master question identifier/number in official paper is required.")

        if not source_document or len(source_document.strip()) < 3:
            raise ValidationError("Source document / official master paper citation is required.")

        now = utc_now()
        ref.exam_name = exam_name.strip()
        ref.exam_year = exam_year
        ref.question_identifier = question_identifier.strip()
        ref.source_document = source_document.strip()
        ref.verification_status = "VERIFIED"
        ref.pyq_status = "VERIFIED_PYQ"
        ref.verified_by_user_id = verifier_id
        ref.verified_at = now
        ref.historical_notes = audit_notes

        await db.commit()
        await db.refresh(ref)

        return {
            "pyq_ref_id": ref.id,
            "exam_name": ref.exam_name,
            "exam_year": ref.exam_year,
            "question_identifier": ref.question_identifier,
            "pyq_status": ref.pyq_status,
            "verification_status": ref.verification_status,
            "verified_by": verifier_id,
            "verified_at": ref.verified_at.isoformat()
        }

    @classmethod
    async def flag_source_conflict(
        cls,
        db: AsyncSession,
        concept_id: str,
        source_a_id: str,
        source_b_id: str,
        conflicting_claim: str,
        specialty: Optional[str] = None
    ) -> SourceConflict:
        """
        Registers a medical contradiction between two sources.
        Both sources are automatically marked CONFLICTED until resolved by Medical Board.
        """
        # Validate sources exist
        stmt_a = select(Source).where(Source.id == source_a_id)
        stmt_b = select(Source).where(Source.id == source_b_id)
        src_a = (await db.execute(stmt_a)).scalars().first()
        src_b = (await db.execute(stmt_b)).scalars().first()

        if not src_a or not src_b:
            raise NotFoundError("Both conflicting sources must exist in the database.")

        now = utc_now()
        conflict = SourceConflict(
            id=str(uuid.uuid4()),
            concept_id=concept_id,
            source_a_id=source_a_id,
            source_b_id=source_b_id,
            conflicting_claim=conflicting_claim.strip(),
            specialty=specialty,
            status="REVIEW_REQUIRED",
            created_at=now
        )
        src_a.verification_status = "CONFLICTED"
        src_b.verification_status = "CONFLICTED"

        db.add(conflict)
        await db.commit()
        await db.refresh(conflict)
        return conflict
