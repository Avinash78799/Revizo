from pydantic import BaseModel, Field
from typing import Optional, List

class ReportQuestionRequest(BaseModel):
    question_id: str
    user_id: Optional[str] = None
    reason: str = Field(..., description="'incorrect_answer', 'ambiguous', 'outdated', 'typo', 'poor_explanation', 'other'")
    comment: Optional[str] = None
    is_serious_medical_error: bool = False

class ApproveQuestionRequest(BaseModel):
    question_id: str
    reviewer_id: Optional[str] = None
    review_notes: Optional[str] = None
    is_high_yield: bool = False

class QuarantineQuestionRequest(BaseModel):
    question_id: str
    reason: str
    audit_notes: Optional[str] = None
