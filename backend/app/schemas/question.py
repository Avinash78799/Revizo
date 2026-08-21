from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class SanitizedOptionResponse(BaseModel):
    option_key: str = Field(..., description="Option label: 'A', 'B', 'C', 'D'")
    option_text: str
    model_config = ConfigDict(from_attributes=True)

class FullOptionResponse(SanitizedOptionResponse):
    id: str
    is_correct: bool
    why_wrong_explanation: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class SanitizedQuestionResponse(BaseModel):
    """Safe schema for active test runner — contains NO answer keys or explanations."""
    id: str
    concept_id: str
    concept_name: Optional[str] = None
    topic_name: Optional[str] = None
    subject_name: Optional[str] = None
    trust_class: str
    question_type: str
    difficulty: str
    is_high_yield: bool
    question_text: str
    options: List[SanitizedOptionResponse]
    model_config = ConfigDict(from_attributes=True)

class QuestionDetailResponse(BaseModel):
    """Full question schema for post-submission review and admin management."""
    id: str
    concept_id: str
    concept_name: Optional[str] = None
    topic_name: Optional[str] = None
    subject_name: Optional[str] = None
    trust_class: str
    question_type: str
    difficulty: str
    status: str
    is_high_yield: bool
    question_text: str
    options: List[FullOptionResponse]
    
    # Structured Explanation Anatomy
    correct_explanation: str
    remember_takeaway: str
    exam_connection: Optional[str] = None
    detailed_explanation: Optional[str] = None
    
    source_citation: Optional[str] = None
    is_ai_generated: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AnswerSubmissionRequest(BaseModel):
    session_id: str
    question_id: str
    selected_option_key: str = Field(..., description="'A', 'B', 'C', or 'D'")
    confidence: str = Field(default="SOMEWHAT_CONFIDENT", description="'DEFINITELY_KNOW', 'SOMEWHAT_CONFIDENT', 'GUESSING'")
    time_spent_seconds: int = Field(default=0, ge=0)

class EvaluationResultResponse(BaseModel):
    is_correct: bool
    selected_option_key: str
    correct_option_key: str
    correct_explanation: str
    why_selected_was_wrong: Optional[str] = None
    remember_takeaway: str
    exam_connection: Optional[str] = None
    detailed_explanation: Optional[str] = None
    concept_id: str
    concept_name: str
    is_danger_zone_item: bool
    revision_interval_days: int = 1
    next_revision_due: Optional[datetime] = None
    is_duplicate_submission: bool = False
    model_config = ConfigDict(from_attributes=True)

class RetestConceptRequest(BaseModel):
    concept_id: str
    exclude_question_id: Optional[str] = None
