import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.db.seed import seed_database
from app.models.user import User
from app.models.reviewer import MedicalReviewerProfile
from app.models.source import Source
from app.services.reviewer_service import ReviewerService
from app.services.source_provenance_service import SourceProvenanceService
from app.core.errors import ValidationError, AuthorizationError, NotFoundError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.mark.asyncio
async def test_harrison_21e_authoritative_onboarding_lifecycle():
    """
    Milestone 12.2: First Authoritative Textbook Onboarding.
    Target: Harrison's Principles of Internal Medicine, 21st Edition.
    Sequence:
    1. Register Harrison 21e -> MUST default to UNVERIFIED.
    2. Candidate holds exact metadata (Title, Edition, Publisher, ISBN-13: 978-1264268504).
    3. Unverified auditor / student attempt -> MUST FAIL (AuthorizationError).
    4. Verified Medical Auditor audits and promotes to VERIFIED with immutable audit evidence.
    5. No question generation in this phase.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False
    )
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await seed_database(session)

        # Set up users: Student, Admin, and Medical Reviewer
        admin = User(email="chief_auditor@neetpg.pro", hashed_password="pw", role="admin", is_active=True)
        student = User(email="student_user@neetpg.pro", hashed_password="pw", role="student", is_active=True)
        doctor = User(email="dr_med_auditor@neetpg.pro", hashed_password="pw", role="medical_reviewer", is_active=True)
        session.add_all([admin, student, doctor])
        await session.commit()

        # Doctor onboards with MD in Internal Medicine
        p_doc = await ReviewerService.register_reviewer_profile(
            db=session,
            user_id=doctor.id,
            credential_type="MD",
            registration_number="KMC-45120",
            medical_council="Karnataka Medical Council",
            specialty="General Medicine"
        )
        assert p_doc.verification_status == "PENDING_VERIFICATION"

        # 1. Register Harrison's 21st Edition Candidate Source
        harrison_candidate = await SourceProvenanceService.register_source_candidate(
            db=session,
            title="Harrison's Principles of Internal Medicine",
            source_type="STANDARD_TEXTBOOK",
            publisher="McGraw Hill Professional",
            edition="21st Edition",
            publication_year=2022,
            reference_identifier="ISBN-9781264268504",
            url="https://accessmedicine.mhmedical.com/book.aspx?bookid=3095",
            specialty="General Medicine",
            notes="Authoritative 2-Volume textbook for internal medicine core curriculum."
        )

        # Invariant 1: Must strictly default to UNVERIFIED
        assert harrison_candidate.verification_status == "UNVERIFIED"
        assert harrison_candidate.verified_by is None
        assert harrison_candidate.verified_at is None
        assert harrison_candidate.reference_identifier == "ISBN-9781264268504"

        # Invariant 2: Student cannot audit/verify source
        with pytest.raises(AuthorizationError) as exc_student:
            await SourceProvenanceService.audit_and_verify_source(
                db=session,
                source_id=harrison_candidate.id,
                verifier_id=student.id,
                decision="VERIFIED",
                reference_identifier="ISBN-9781264268504",
                edition="21st Edition",
                publisher="McGraw Hill Professional",
                audit_evidence_notes="Attempted by student"
            )
        assert "Only VERIFIED reviewers or Admins can audit" in str(exc_student.value)

        # Invariant 3: Unverified doctor cannot audit/verify source
        with pytest.raises(AuthorizationError) as exc_unver_doc:
            await SourceProvenanceService.audit_and_verify_source(
                db=session,
                source_id=harrison_candidate.id,
                verifier_id=doctor.id,
                decision="VERIFIED",
                reference_identifier="ISBN-9781264268504",
                edition="21st Edition",
                publisher="McGraw Hill Professional",
                audit_evidence_notes="Attempted before credential verification"
            )
        assert "not an active verified medical reviewer" in str(exc_unver_doc.value)

        # Admin verifies doctor's credentials
        await ReviewerService.verify_reviewer_credentials(
            db=session,
            profile_id=p_doc.id,
            verifier_user_id=admin.id,
            decision="VERIFIED",
            verification_evidence_ref="KMC-REG-45120-CONFIRMED",
            audit_notes="State council registration verified against official registry."
        )
        assert p_doc.verification_status == "VERIFIED"
        assert p_doc.active_status is True

        # Invariant 4: Verified Medical Doctor audits and approves Harrison 21e
        audit_result = await SourceProvenanceService.audit_and_verify_source(
            db=session,
            source_id=harrison_candidate.id,
            verifier_id=doctor.id,
            decision="VERIFIED",
            reference_identifier="ISBN-9781264268504",
            edition="21st Edition",
            publisher="McGraw Hill Professional",
            audit_evidence_notes="Audited against physical 2-volume print edition (ISBN-13: 978-1264268504) and McGraw Hill AccessMedicine official electronic entry."
        )

        assert audit_result["verification_status"] == "VERIFIED"
        assert audit_result["verified_by"] == doctor.id
        assert audit_result["reference_identifier"] == "ISBN-9781264268504"
        assert audit_result["edition"] == "21st Edition"
        assert audit_result["publisher"] == "McGraw Hill Professional"
        assert audit_result["verified_at"] is not None
        assert "AccessMedicine" in audit_result["audit_notes"]

        # Confirm persisted source in database
        stmt = select(Source).where(Source.id == harrison_candidate.id)
        persisted_src = (await session.execute(stmt)).scalars().first()
        assert persisted_src.verification_status == "VERIFIED"
        assert persisted_src.verified_by == doctor.id
        assert persisted_src.notes == audit_result["audit_notes"]

    await engine.dispose()
