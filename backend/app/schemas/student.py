from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DueConceptItem(BaseModel):
    concept_id: str
    concept_name: str
    topic_name: str
    subject_name: str
    revision_interval_days: int
    next_revision_due: datetime

class WeakAreaItem(BaseModel):
    topic_id: str
    topic_name: str
    subject_name: str
    mastery_percentage: float
    total_attempts: int

class DangerZoneItem(BaseModel):
    concept_id: str
    concept_name: str
    topic_name: str
    subject_name: str
    high_confidence_wrong_count: int
    last_practiced_at: datetime
    clinical_pearl: Optional[str] = None
    trigger_reason: Optional[str] = "Overconfidence Error (Wrong with 100% confidence)"
    trigger_type: Optional[str] = "overconfidence"
    occurrence_count: int = 1

class DashboardResponse(BaseModel):
    todays_practice_count: int
    todays_practice_est_minutes: int
    due_revisions: List[DueConceptItem]
    weak_areas: List[WeakAreaItem]
    danger_zone_count: int
    total_mistakes_count: int
    total_questions_attempted: int
    overall_accuracy_percentage: float
    calibration_percentage: float = 0.0

