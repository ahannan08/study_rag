import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class QuestionLog(Base):
    __tablename__ = "question_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    matched_chunk_ids: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    coverage_label: Mapped[str] = mapped_column(String(32), nullable=False)
    section_tag: Mapped[str] = mapped_column(Text, default="")
    answer_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
