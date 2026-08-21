from fastapi import APIRouter, Depends, status, Request
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.errors import AuthenticationError, ConflictError
from app.models.user import User, Profile
from app.api.deps import get_current_user
from app.services.rate_limiter import rate_limiter

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    target_exam_year: Optional[int] = Field(default=2026, ge=2024, le=2035)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
    full_name: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: str
    email: str
    role: str
    full_name: Optional[str] = None
    target_exam_year: Optional[int] = None
    daily_question_goal: int = 10

from app.services.email_service import EmailService

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "unknown")
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()
    rate_limiter.check_rate_limit(f"register:{client_ip}", max_requests=60, window_seconds=60)

    # Check if email exists
    stmt = select(User).where(User.email == req.email.lower().strip())
    existing = (await db.execute(stmt)).scalars().first()
    if existing:
        raise ConflictError("An account with this email address already exists. Please sign in with your password.")

    user = User(
        email=req.email.lower().strip(),
        hashed_password=get_password_hash(req.password),
        role="student",
        is_active=True
    )
    db.add(user)
    await db.flush()

    profile = Profile(
        user_id=user.id,
        full_name=req.full_name,
        target_exam_year=req.target_exam_year,
        daily_question_goal=10
    )
    db.add(profile)
    await db.commit()

    # Trigger automated welcome email to student
    await EmailService.send_welcome_email(
        to_email=user.email,
        full_name=profile.full_name,
        target_year=req.target_exam_year or 2026
    )

    token = create_access_token({
        "sub": user.id,
        "email": user.email,
        "role": user.role
    })

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        role=user.role,
        full_name=profile.full_name
    )

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    client_ip = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "unknown")
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()
    rate_limiter.check_rate_limit(f"login:{client_ip}", max_requests=60, window_seconds=60)

    stmt = select(User).where(User.email == req.email.lower().strip())
    user = (await db.execute(stmt)).scalars().first()

    # Generic error message to prevent account enumeration
    if not user or not verify_password(req.password, user.hashed_password):
        raise AuthenticationError("Invalid email or password credentials.")

    if not user.is_active:
        raise AuthenticationError("Account is deactivated.")

    token = create_access_token({
        "sub": user.id,
        "email": user.email,
        "role": user.role
    })

    full_name = user.profile.full_name if user.profile else None

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        role=user.role,
        full_name=full_name
    )

@router.get("/me", response_model=UserProfileResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        full_name=current_user.profile.full_name if current_user.profile else None,
        target_exam_year=current_user.profile.target_exam_year if current_user.profile else None,
        daily_question_goal=current_user.profile.daily_question_goal if current_user.profile else 10
    )

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Stateless JWT client logout acknowledgment.
    """
    return {"status": "logged_out", "message": "Session terminated successfully."}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)

from app.services.password_reset_service import PasswordResetService

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(req: ForgotPasswordRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Generates a 6-digit OTP and sends it to the user's email address.
    """
    client_ip = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "unknown")
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()
    rate_limiter.check_rate_limit(f"forgot_password:{client_ip}", max_requests=10, window_seconds=60)

    clean_email = req.email.lower().strip()
    stmt = select(User).where(User.email == clean_email)
    user = (await db.execute(stmt)).scalars().first()

    # Generate OTP
    otp = await PasswordResetService.generate_otp(clean_email)

    # Deliver OTP via Email
    if user and user.is_active:
        await EmailService.send_password_reset_otp(to_email=clean_email, otp_code=otp)

    return {
        "status": "otp_sent",
        "email": clean_email,
        "message": f"If an account exists for {clean_email}, a 6-digit verification code has been dispatched to your email."
    }

@router.post("/reset-password", status_code=status.HTTP_200_OK)
@router.post("/reset-password-otp", status_code=status.HTTP_200_OK)
async def reset_password(req: ResetPasswordOtpRequest, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Verifies 6-digit OTP and updates the account password.
    """
    client_ip = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "unknown")
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()
    rate_limiter.check_rate_limit(f"reset_password:{client_ip}", max_requests=15, window_seconds=60)

    clean_email = req.email.lower().strip()

    # Verify OTP
    is_valid_otp = await PasswordResetService.verify_and_consume_otp(clean_email, req.otp)
    if not is_valid_otp:
        raise AuthenticationError("Invalid or expired 6-digit verification code. Please request a new code.")

    stmt = select(User).where(User.email == clean_email)
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        raise NotFoundError("Account not found.")

    # Update password
    user.hashed_password = get_password_hash(req.new_password)
    await db.commit()

    return {
        "status": "success",
        "message": "Password updated successfully. You can now sign in with your new password."
    }
