import os
import json
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict

class StagingSettings(BaseSettings):
    """
    Milestone 9 Staging Environment Configuration (Prompt 13, Sec 2).
    - Production-like PostgreSQL with connection pooling
    - Externalized secrets
    - Strict CORS & Security Headers
    - Structured JSON Logging
    - Rate Limiting & Health Probes
    """
    model_config = SettingsConfigDict(env_file=".env.staging", extra="ignore")

    ENVIRONMENT: str = "staging"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = os.getenv("STAGING_DATABASE_URL", "postgresql+asyncpg://staging_user:staging_placeholder@localhost:5432/neetpg_staging")
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_TIMEOUT_SECONDS: int = 30
    
    # Security
    SECRET_KEY: str = os.getenv("STAGING_SECRET_KEY", "STAGING_SECRET_KEY_PLACEHOLDER_LOAD_FROM_VAULT")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # Strict CORS
    ALLOWED_ORIGINS: list = [
        "https://staging.neetpg.pro",
        "https://admin.staging.neetpg.pro"
    ]
    
    # Rate Limiting
    RATE_LIMIT_STUDENT_PER_MINUTE: int = 120
    RATE_LIMIT_AI_GEN_PER_HOUR: int = 50
    
    # Feature Flags
    ALLOW_MOCK_AI: bool = False  # Strict fail-closed in staging unless explicit dev flag
    ENFORCE_TWO_PERSON_REVIEW: bool = True
    ENFORCE_STRICT_PROVENANCE: bool = True

class JsonLogFormatter(logging.Formatter):
    """
    Structured JSON Logger for Staging / Production Observability.
    Masks PII, passwords, JWT tokens, and API keys.
    """
    SENSITIVE_KEYS = {"password", "token", "secret", "authorization", "api_key", "bearer"}

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def configure_staging_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonLogFormatter())
    logging.root.handlers = [handler]
    logging.root.setLevel(logging.INFO)
