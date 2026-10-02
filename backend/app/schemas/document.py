import uuid
from datetime import datetime

from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: uuid.UUID
    title: str
    status: str
    uploaded_at: datetime
    indexed: bool
    topic_map_ready: bool
    flashcards_ready: bool
    chunk_count: int = 0

    model_config = {"from_attributes": True}


class DocumentDetailOut(DocumentOut):
    topic_map: dict | list | None = None
    topic_map_at: datetime | None = None


class DocumentUploadResponse(BaseModel):
    document_id: uuid.UUID
    job_id: uuid.UUID
