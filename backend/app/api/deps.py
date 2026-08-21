from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services.authorization import AuthenticationError, AuthorizationError

security_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Extracts and verifies JWT token from Authorization header and loads current User.
    """
    if not credentials:
        raise AuthenticationError("Authorization header missing or invalid format")
    
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise AuthenticationError("Invalid, expired, or tampered access token")
    
    user_id = payload["sub"]
    stmt = select(User).where(User.id == user_id, User.is_active == True)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        raise AuthenticationError("User account not found or inactive")
        
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Restricts access strictly to Admin role."""
    if current_user.role != "admin":
        raise AuthorizationError("Access denied: Administrative privileges required")
    return current_user

async def get_current_reviewer_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Restricts access to Medical Reviewers and Admins."""
    if current_user.role not in ("admin", "medical_reviewer"):
        raise AuthorizationError("Access denied: Medical Reviewer privileges required")
    return current_user
