import time
import bcrypt
import jwt
from typing import Optional, Dict, Any
from app.core.config import settings

# Security Configuration Invariants
BCRYPT_ROUNDS = 12
JWT_ALGORITHM = "HS256"
JWT_ISSUER = "neetpg-pro-auth"
JWT_AUDIENCE = "neetpg-pro-app"

# ==============================================================================
# 1. PASSWORD HASHING (Using bcrypt)
# ==============================================================================

def get_password_hash(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt with standard cost factor (12 rounds).
    Passwords are HASHED using a one-way salt-inclusive function, never encrypted.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Timing-safe verification of plaintext password against stored bcrypt hash.
    Safely rejects malformed hashes and empty passwords without crashing.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        # Rejects malformed hash strings safely
        return False

# ==============================================================================
# 2. JWT TOKEN MANAGEMENT (Using PyJWT)
# ==============================================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta_seconds: Optional[int] = None
) -> str:
    """
    Generates a cryptographically signed JWT with explicit issuer, audience,
    expiration (exp), issued at (iat), and not-before (nbf) claims.
    """
    now = int(time.time())
    exp_seconds = expires_delta_seconds if expires_delta_seconds is not None else (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    payload = data.copy()
    payload.update({
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + exp_seconds
    })
    
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and validates a JWT token with strict signature, algorithm, issuer,
    and audience checks. Prevents algorithm confusion ('none' algorithm attacks).
    """
    if not token:
        return None
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[JWT_ALGORITHM],  # Explicitly restrict to HS256 to block 'none' attack
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
                "require": ["exp", "iat", "iss", "aud"]
            }
        )
        return payload
    except (jwt.PyJWTError, Exception):
        return None
