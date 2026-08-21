from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.question import SanitizedQuestionResponse

class CreateTestSessionRequest(BaseModel):
    user_id: Optional[str] = None
    mode: str = Field(default="quick_test", description="'quick_test', 'topic_test', 'chapter_test', 'five_minute_revision'")
    subject_id: Optional[str] = None
    chapter_id: Optional[str] = None
    topic_id: Optional[str] = None
    question_count: int = Field(default=5, ge=1, le=50)

class TestSessionResponse(BaseModel):
    session_id: str
    user_id: str
    mode: str
    total_questions: int
    completed_questions: int
    score: int
    started_at: datetime
    questions: List[SanitizedQuestionResponse]
