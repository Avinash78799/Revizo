import pytest
import time
import jwt
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    JWT_ALGORITHM,
    JWT_ISSUER,
    JWT_AUDIENCE
)
from app.core.config import settings

# ==============================================================================
# 1. PASSWORD HASHING TESTS
# ==============================================================================

def test_password_hashing_and_verification():
    password = "SecureMedicalPassword2026!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")  # bcrypt prefix
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_salt_uniqueness_for_same_password():
    password = "IdenticalPassword"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True

def test_malformed_and_empty_passwords():
    assert verify_password("", "$2b$12$e8Y...invalid") is False
    assert verify_password("Password", "") is False
    assert verify_password("Password", "invalid_plain_string") is False
    assert verify_password("Password", "$invalid$format$hash") is False
    
    with pytest.raises(ValueError):
        get_password_hash("")

# ==============================================================================
# 2. JWT TOKEN SECURITY TESTS
# ==============================================================================

def test_jwt_valid_creation_and_decoding():
    payload_data = {"sub": "user-uuid-12345", "role": "student", "email": "doc@neetpg.pro"}
    token = create_access_token(payload_data, expires_delta_seconds=3600)
    
    assert isinstance(token, str)
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "user-uuid-12345"
    assert decoded["role"] == "student"
    assert decoded["email"] == "doc@neetpg.pro"
    assert decoded["iss"] == JWT_ISSUER
    assert decoded["aud"] == JWT_AUDIENCE
    assert "exp" in decoded
    assert "iat" in decoded

def test_jwt_expired_token_rejection():
    payload_data = {"sub": "user-expired"}
    # Token expired 10 seconds ago
    token = create_access_token(payload_data, expires_delta_seconds=-10)
    decoded = decode_access_token(token)
    assert decoded is None

def test_jwt_algorithm_confusion_attack_rejection():
    """Tests that unsigned tokens using the 'none' algorithm are strictly rejected."""
    payload = {
        "sub": "attacker-user",
        "role": "admin",
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    # Forge token with alg='none'
    forged_token = jwt.encode(payload, key="", algorithm="none")
    decoded = decode_access_token(forged_token)
    assert decoded is None

def test_jwt_invalid_signature_and_tampered_payload_rejection():
    payload_data = {"sub": "user-genuine", "role": "student"}
    valid_token = create_access_token(payload_data, expires_delta_seconds=3600)
    
    # Tamper with signature
    tampered_token = valid_token[:-5] + "XXXXX"
    assert decode_access_token(tampered_token) is None
    
    # Signed with completely different 32-byte secret
    alien_token = jwt.encode(
        {"sub": "user-genuine", "iss": JWT_ISSUER, "aud": JWT_AUDIENCE, "exp": int(time.time()) + 3600, "iat": int(time.time())},
        "wrong_secret_key_that_is_at_least_32_bytes_long_1234567890",
        algorithm=JWT_ALGORITHM
    )
    assert decode_access_token(alien_token) is None
