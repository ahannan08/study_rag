import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DocumentStatus(str, enum.Enum):
    UPLOADING = "uploading"
    INDEXING = "indexing"
    INDEXED = "indexed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=DocumentStatus.UPLOADING.value, index=True)
    blob_path: Mapped[str] = mapped_column(Text, nullable=False)
    faiss_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    topic_map: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    topic_map_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="document", cascade="all, delete-orphan")
    jobs = relationship("Job", back_populates="document", cascade="all, delete-orphan")

    @property
    def indexed(self) -> bool:
        return self.status == DocumentStatus.INDEXED.value

    @property
    def topic_map_ready(self) -> bool:
        return self.topic_map is not None

    @property
    def flashcards_ready(self) -> bool:
        return bool(self.flashcards)
