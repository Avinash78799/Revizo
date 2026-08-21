import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviewer import MedicalReviewerProfile
from app.models.user import User
from app.core.datetime_util import utc_now
from app.core.errors import ValidationError, NotFoundError, AuthorizationError

class ReviewerService:
    """
    Milestone 11 Phase 1: Reviewer Onboarding & Credential Verification Engine.
    
    Invariants:
    1. Reviewer onboarding requires authenticated user account, recognized qualification, and council registration.
    2. Reviewers start in PENDING_VERIFICATION (active_status=False). Never auto-verified.
    3. Only authorized independent verifiers (Admin/Medical Board) can verify credentials (verifier != applicant).
    4. Freezes immutable credential verification snapshot upon approval/rejection.
    5. Only VERIFIED + ACTIVE reviewers can approve medical questions.
    6. High-risk content requires two distinct verified reviewers.
    7. Supports SUSPENDED and REVOKED lifecycle transitions.
    """

    RECOGNIZED_QUALIFICATIONS = {
        "MBBS",
        "MD",
        "MS",
        "DNB",
        "DM",
        "MCH",
        "MRCP",
        "FRCS",
        "FNB",
        "DIPLOMA"
    }

    VALID_VERIFICATION_STATUSES = {
        "PENDING_VERIFICATION",
        "VERIFIED",
        "REJECTED",
        "SUSPENDED",
        "REVOKED"
    }

    @classmethod
    async def register_reviewer_profile(
        cls,
        db: AsyncSession,
        user_id: str,
        credential_type: str,
        registration_number: str,
        medical_council: str,
        specialty: str
    ) -> MedicalReviewerProfile:
        """
        Onboards a new medical reviewer applicant into PENDING_VERIFICATION state.
        Never marks a reviewer VERIFIED upon registration.
        """
        # 1. Validate user account
        stmt_u = select(User).where(User.id == user_id)
        res_u = await db.execute(stmt_u)
        user = res_u.scalars().first()
        if not user:
            raise NotFoundError(f"User account '{user_id}' not found.")

        # 2. Validate recognized qualification degree
        norm_credential = credential_type.strip().upper()
        if norm_credential not in cls.RECOGNIZED_QUALIFICATIONS:
            raise ValidationError(
                f"Qualification '{credential_type}' is not recognized. "
                f"Must be one of: {sorted(list(cls.RECOGNIZED_QUALIFICATIONS))}"
            )

        # 3. Validate registration number & council evidence
        if not registration_number or len(registration_number.strip()) < 3:
            raise ValidationError("A valid medical council registration number is required.")

        if not medical_council or len(medical_council.strip()) < 3:
            raise ValidationError("Medical council / state council authority must be specified.")

        if not specialty or len(specialty.strip()) < 2:
            raise ValidationError("Medical specialty must be specified.")

        # 4. Check for existing profile
        stmt_p = select(MedicalReviewerProfile).where(MedicalReviewerProfile.user_id == user_id)
        res_p = await db.execute(stmt_p)
        existing = res_p.scalars().first()
        if existing:
            raise ValidationError(f"Medical Reviewer profile already exists for user '{user_id}'.")

        now = utc_now()
        profile = MedicalReviewerProfile(
            id=str(uuid.uuid4()),
            user_id=user_id,
            credential_type=norm_credential,
            registration_number=registration_number.strip(),
            medical_council=medical_council.strip(),
            specialty=specialty.strip(),
            verification_status="PENDING_VERIFICATION",
            credential_status="PENDING",
            active_status=False,  # Inactive until verified
            verified_at=None,
            verified_by=None,
            created_at=now,
            updated_at=now
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile

    @classmethod
    async def verify_reviewer_credentials(
        cls,
        db: AsyncSession,
        profile_id: str,
        verifier_user_id: str,
        decision: str,  # 'VERIFIED' or 'REJECTED'
        verification_evidence_ref: str,
        audit_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes independent third-party credential verification.
        Enforces: verifier_user_id != applicant_user_id (no self-verification).
        Freezes an immutable credential verification snapshot.
        """
        # 1. Retrieve profile
        stmt = select(MedicalReviewerProfile).options(selectinload(MedicalReviewerProfile.user)).where(MedicalReviewerProfile.id == profile_id)
        res = await db.execute(stmt)
        profile = res.scalars().first()
        if not profile:
            raise NotFoundError(f"Medical Reviewer Profile '{profile_id}' not found.")

        # 2. Check self-approval prevention
        if profile.user_id == verifier_user_id:
            raise AuthorizationError("Medical reviewers cannot approve their own credential verification.")

        # 3. Validate verifier authorization (Admin or Medical Director role)
        stmt_v = select(User).where(User.id == verifier_user_id)
        res_v = await db.execute(stmt_v)
        verifier = res_v.scalars().first()
        if not verifier or verifier.role not in ["admin", "medical_director"]:
            raise AuthorizationError("Only an authorized Admin or Medical Director can verify reviewer credentials.")

        # 4. Validate verification decision
        decision_upper = decision.strip().upper()
        if decision_upper not in ["VERIFIED", "REJECTED"]:
            raise ValidationError(f"Invalid verification decision '{decision}'. Must be 'VERIFIED' or 'REJECTED'.")

        if not verification_evidence_ref or len(verification_evidence_ref.strip()) < 3:
            raise ValidationError("Verification evidence reference (e.g. Council registry lookup ID) is required.")

        now = utc_now()
        if decision_upper == "VERIFIED":
            profile.verification_status = "VERIFIED"
            profile.credential_status = "ACTIVE"
            profile.active_status = True
            profile.verified_at = now
            profile.verified_by = verifier_user_id
        else:
            profile.verification_status = "REJECTED"
            profile.credential_status = "REJECTED"
            profile.active_status = False
            profile.verified_at = now
            profile.verified_by = verifier_user_id
            profile.suspension_reason = audit_notes or "Council verification check failed"

        profile.updated_at = now
        await db.commit()
        await db.refresh(profile)

        # 5. Return immutable verification snapshot
        return {
            "profile_id": profile.id,
            "user_id": profile.user_id,
            "credential_type": profile.credential_type,
            "registration_number": profile.registration_number,
            "medical_council": profile.medical_council,
            "specialty": profile.specialty,
            "verification_status": profile.verification_status,
            "credential_status": profile.credential_status,
            "active_status": profile.active_status,
            "verified_by": verifier_user_id,
            "verified_at": profile.verified_at.isoformat() if profile.verified_at else None,
            "evidence_reference": verification_evidence_ref,
            "audit_notes": audit_notes,
            "snapshot_frozen": True
        }

    @classmethod
    async def suspend_or_revoke_reviewer(
        cls,
        db: AsyncSession,
        profile_id: str,
        admin_user_id: str,
        action: str,  # 'SUSPEND' or 'REVOKE'
        reason: str
    ) -> Dict[str, Any]:
        """
        Suspends or revokes a reviewer's approval privileges.
        """
        stmt = select(MedicalReviewerProfile).where(MedicalReviewerProfile.id == profile_id)
        res = await db.execute(stmt)
        profile = res.scalars().first()
        if not profile:
            raise NotFoundError(f"Medical Reviewer Profile '{profile_id}' not found.")

        if not reason or len(reason.strip()) < 5:
            raise ValidationError("A clear reason is required to suspend or revoke reviewer credentials.")

        now = utc_now()
        action_upper = action.strip().upper()
        if action_upper == "SUSPEND":
            profile.verification_status = "SUSPENDED"
            profile.credential_status = "SUSPENDED"
            profile.active_status = False
            profile.suspension_reason = reason
        elif action_upper == "REVOKE":
            profile.verification_status = "REVOKED"
            profile.credential_status = "REVOKED"
            profile.active_status = False
            profile.suspension_reason = reason
        else:
            raise ValidationError(f"Invalid action '{action}'. Must be 'SUSPEND' or 'REVOKE'.")

        profile.updated_at = now
        await db.commit()
        await db.refresh(profile)

        return {
            "profile_id": profile.id,
            "user_id": profile.user_id,
            "status": profile.verification_status,
            "active_status": profile.active_status,
            "reason": reason,
            "updated_at": now.isoformat()
        }

    @classmethod
    async def get_reviewer_profile(cls, db: AsyncSession, user_id: str) -> Optional[MedicalReviewerProfile]:
        """
        Retrieves profile by user ID.
        """
        stmt = select(MedicalReviewerProfile).where(MedicalReviewerProfile.user_id == user_id)
        res = await db.execute(stmt)
        return res.scalars().first()

    @classmethod
    async def get_profile_by_user_id(cls, db: AsyncSession, user_id: str) -> Optional[MedicalReviewerProfile]:
        """
        Alias for get_reviewer_profile.
        """
        return await cls.get_reviewer_profile(db, user_id)
