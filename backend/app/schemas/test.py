from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.question import SanitizedQuestionResponse

class CreateTestSessionRequest(BaseModel):
    user_id: Optional[str] = None
    mode: str = Field(
        default="quick_test",
        description="'quick_test', 'topic_test', 'chapter_test', 'five_minute_revision', 'pyq_pattern_test', 'PYQ_PATTERN_TEST', 'grand_test'"
    )
    subject_id: Optional[str] = None
    chapter_id: Optional[str] = None
    topic_id: Optional[str] = None
    question_count: int = Field(default=20, ge=10, le=50)
    total_questions: Optional[int] = Field(default=None, ge=10, le=50)

    def get_effective_count(self) -> int:
        if self.total_questions is not None and self.total_questions >= 10:
            return self.total_questions
        return self.question_count

class TestSessionResponse(BaseModel):
    session_id: str
    user_id: str
    mode: str
    total_questions: int
    completed_questions: int
    score: int
    started_at: datetime
    questions: List[SanitizedQuestionResponse]
