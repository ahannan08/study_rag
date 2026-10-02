import uuid

from pydantic import BaseModel, Field


class ChatIn(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class CitationOut(BaseModel):
    chunk_id: uuid.UUID
    logical_page: int
    section_path: str
    excerpt: str
    label: str


class ChatOut(BaseModel):
    answer: str
    citations: list[CitationOut]
    coverage_label: str
    chunk_ids_used: list[uuid.UUID]
    refusal: bool
