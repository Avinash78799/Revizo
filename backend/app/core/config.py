from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "NEET-PG AI Practice & Revision Platform"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./neet_pg.db"
    
    # Security & Tokens
    SECRET_KEY: str = "neet_pg_pro_dev_secret_key_change_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Environment & Safety
    ENVIRONMENT: str = "development"  # 'development', 'staging', 'production'
    ALLOW_MOCK_AI: bool = True
    
    # AI Dynamic Layer & Safety Controls
    AI_GENERATION_ENABLED: bool = True
    AI_PROVIDER: str = "mock"  # or openai, anthropic, gemini
    AI_API_KEY: Optional[str] = None
    AI_DAILY_TOKEN_LIMIT: int = 100_000
    
    # Quality & Review Controls
    MIN_QUALITY_SCORE_THRESHOLD: float = 0.85
    MAX_DUPLICATE_SIMILARITY: float = 0.85
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
