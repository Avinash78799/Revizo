from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ConceptBase(BaseModel):
    name: str
    high_yield_notes: Optional[str] = None
    clinical_pearl: Optional[str] = None
    exam_relevance_score: float = 0.80

class ConceptResponse(ConceptBase):
    id: str
    topic_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TopicBase(BaseModel):
    name: str
    order_index: int = 0

class TopicItemResponse(TopicBase):
    id: str
    chapter_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TopicResponse(TopicBase):
    id: str
    chapter_id: str
    concepts: List[ConceptResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChapterBase(BaseModel):
    name: str
    order_index: int = 0

class ChapterItemResponse(ChapterBase):
    id: str
    subject_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChapterResponse(ChapterBase):
    id: str
    subject_id: str
    topics: List[TopicResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    order_index: int = 0

class SubjectItemResponse(SubjectBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SubjectResponse(SubjectBase):
    id: str
    chapters: List[ChapterResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
