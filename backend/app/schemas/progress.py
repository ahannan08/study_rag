from pydantic import BaseModel


class SectionStat(BaseModel):
    section_tag: str
    question_count: int
    review_count: int
    error_rate: float | None


class ProgressOut(BaseModel):
    document_id: str
    sections: list[SectionStat]
    total_questions: int
    total_reviews: int


class WeakPointOut(BaseModel):
    section_tag: str
    error_rate: float
    suggestion_text: str | None = None


class WeakPointsResponse(BaseModel):
    weak_points: list[WeakPointOut]
