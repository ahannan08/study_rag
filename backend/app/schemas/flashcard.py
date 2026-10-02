import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class FlashcardOut(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    question: str
    answer: str
    section_tag: str
    next_review_at: datetime | None

    model_config = {"from_attributes": True}


class FlashcardGenerateResponse(BaseModel):
    job_id: uuid.UUID


class FlashcardReviewIn(BaseModel):
    correct: bool


class FlashcardReviewOut(BaseModel):
    flashcard_id: uuid.UUID
    next_review_at: datetime | None
    interval_days: int
    ease_factor: float
