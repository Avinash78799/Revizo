import time
import random
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, delete, and_
from app.core.database import AsyncSessionLocal, Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
import uuid

logger = logging.getLogger("revizo.auth.otp")

class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), index=True, nullable=False)
    otp = Column(String(10), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PasswordResetService:
    """
    Database-backed 6-digit password reset OTP generator, validator, and rate-limiter.
    """

    @classmethod
    async def generate_otp(cls, email: str) -> str:
        clean_email = email.lower().strip()
        otp = f"{random.randint(100000, 999999)}"
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)

        async with AsyncSessionLocal() as db:
            # Invalidate any older unused OTPs for this email
            await db.execute(delete(PasswordResetOTP).where(PasswordResetOTP.email == clean_email))
            
            record = PasswordResetOTP(
                email=clean_email,
                otp=otp,
                expires_at=expires_at,
                attempts=0,
                is_used=False
            )
            db.add(record)
            await db.commit()

        logger.info(f"[OTP GENERATED] Database record created for {clean_email} (valid 10 mins).")
        return otp

    @classmethod
    async def verify_and_consume_otp(cls, email: str, submitted_otp: str) -> bool:
        clean_email = email.lower().strip()
        now = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as db:
            stmt = select(PasswordResetOTP).where(
                and_(
                    PasswordResetOTP.email == clean_email,
                    PasswordResetOTP.is_used == False
                )
            ).order_by(PasswordResetOTP.created_at.desc())

            res = await db.execute(stmt)
            record = res.scalars().first()

            if not record:
                return False

            # Check expiration
            exp = record.expires_at
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if now > exp:
                return False

            record.attempts += 1
            if record.attempts > 5:
                # Exceeded attempts
                record.is_used = True
                await db.commit()
                return False

            if record.otp == submitted_otp.strip():
                record.is_used = True
                await db.commit()
                return True
            else:
                await db.commit()
                return False
