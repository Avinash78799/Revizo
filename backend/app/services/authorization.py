from fastapi import HTTPException, status
from typing import Dict, Any, Optional

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Access forbidden: Insufficient permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Invalid or expired authentication credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationService:
    """
    Centralized server-authoritative authorization engine.
    Enforces student data isolation and administrative access boundaries.
    """

    @staticmethod
    def verify_ownership(current_user_id: str, resource_owner_id: str, current_user_role: str = "student") -> bool:
        """
        Validates that a student can ONLY access resources they own.
        Admins possess elevated oversight for administrative triage.
        """
        if current_user_role in ("admin", "medical_reviewer"):
            return True
        if current_user_id != resource_owner_id:
            raise AuthorizationError(
                detail="Security Violation: You do not have permission to access another student's performance records."
            )
        return True

    @staticmethod
    def require_role(current_user_role: str, allowed_roles: list[str]) -> bool:
        """
        Restricts sensitive mutations (quarantine, review, question withdrawal) to designated roles.
        """
        if current_user_role not in allowed_roles:
            raise AuthorizationError(
                detail=f"Security Violation: Required role in {allowed_roles}, but caller possesses '{current_user_role}'."
            )
        return True

    @staticmethod
    def require_admin(current_user_role: str) -> bool:
        return AuthorizationService.require_role(current_user_role, ["admin"])

    @staticmethod
    def require_reviewer_or_admin(current_user_role: str) -> bool:
        return AuthorizationService.require_role(current_user_role, ["admin", "medical_reviewer"])
