import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.infrastructure.llm.grok_client import GrokClient
from app.infrastructure.llm.prompts import TOPIC_MAP_SYSTEM
from app.models import Chunk, Document
from app.services.job_service import mark_job_completed, mark_job_failed, mark_job_running


def run_topic_map_generation(db: Session, job_id: uuid.UUID, document_id: uuid.UUID) -> None:
    doc = db.query(Document).filter(Document.id == document_id).one()
    try:
        mark_job_running(db, job_id, "loading_chunks")
        chunks = db.query(Chunk).filter(Chunk.document_id == document_id).order_by(Chunk.logical_page).all()
        if not chunks:
            raise ValueError("Document has no chunks; index first")

        text = _summarize_chunks(chunks, max_chars=120_000)
        mark_job_running(db, job_id, "grok_topic_map")
        grok = GrokClient()
        result = grok.chat_json(TOPIC_MAP_SYSTEM, f"Document content:\n{text}")
        doc.topic_map = result
        doc.topic_map_at = datetime.now(UTC)
        db.commit()
        mark_job_completed(db, job_id)
    except Exception as exc:
        mark_job_failed(db, job_id, str(exc))
        raise


def _summarize_chunks(chunks: list[Chunk], max_chars: int) -> str:
    parts: list[str] = []
    total = 0
    for ch in chunks:
        piece = f"[p{ch.logical_page} {ch.section_path}]\n{ch.text}\n"
        if total + len(piece) > max_chars:
            break
        parts.append(piece)
        total += len(piece)
    return "\n".join(parts)
