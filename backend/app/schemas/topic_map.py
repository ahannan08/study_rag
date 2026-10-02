import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class TopicMapOut(BaseModel):
    document_id: uuid.UUID
    topic_map: dict | list
    generated_at: datetime


class TopicMapGenerateResponse(BaseModel):
    job_id: uuid.UUID
