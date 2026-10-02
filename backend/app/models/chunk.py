import uuid

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id"), index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    logical_page: Mapped[int] = mapped_column(Integer, nullable=False)
    section_path: Mapped[str] = mapped_column(Text, default="")
    paragraph_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_page_label: Mapped[str | None] = mapped_column(Text, nullable=True)
    faiss_row_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    document = relationship("Document", back_populates="chunks")
