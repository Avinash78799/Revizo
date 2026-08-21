from fastapi import HTTPException, status
from typing import Optional, Any, Dict

class AppError(HTTPException):
    def __init__(self, status_code: int, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status_code, detail={"code": code, "message": message, "details": details or {}})
        self.code = code
        self.message = message
        self.details = details or {}

class AuthenticationError(AppError):
    def __init__(self, message: str = "Invalid, missing, or expired credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message
        )

class AuthorizationError(AppError):
    def __init__(self, message: str = "Access forbidden: Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message
        )

class NotFoundError(AppError):
    def __init__(self, entity: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"{entity} not found or unavailable."
        )

class ValidationError(AppError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=422,
            code="VALIDATION_ERROR",
            message=message,
            details=details
        )

class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            message=message
        )

class RateLimitError(AppError):
    def __init__(self, message: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMITED",
            message=message
        )

class InvalidStateTransitionError(AppError):
    def __init__(self, from_state: str, to_state: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_STATE_TRANSITION",
            message=f"Cannot transition state from '{from_state}' to '{to_state}'."
        )

class ProviderUnavailableError(AppError):
    def __init__(self, provider_name: str, message: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="PROVIDER_UNAVAILABLE",
            message=message or f"AI Provider '{provider_name}' is currently unavailable. Automatic mock fallback is forbidden in production."
        )
