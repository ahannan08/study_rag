import json
import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.infrastructure.llm.grok_client import GrokClient
from app.infrastructure.llm.prompts import FLASHCARD_SYSTEM
from app.models import Chunk, Document, Flashcard
from app.services.job_service import mark_job_completed, mark_job_failed, mark_job_running
from app.services.topic_map_service import _summarize_chunks


def run_flashcard_generation(db: Session, job_id: uuid.UUID, document_id: uuid.UUID) -> None:
    doc = db.query(Document).filter(Document.id == document_id).one()
    try:
        mark_job_running(db, job_id, "loading_chunks")
        chunks = db.query(Chunk).filter(Chunk.document_id == document_id).order_by(Chunk.logical_page).all()
        if not chunks:
            raise ValueError("Document has no chunks; index first")

        text = _summarize_chunks(chunks, max_chars=100_000)
        topic_hint = ""
        if doc.topic_map:
            topic_hint = f"\nTopic map JSON:\n{json.dumps(doc.topic_map)}"

        mark_job_running(db, job_id, "grok_flashcards")
        grok = GrokClient()
        result = grok.chat_json(FLASHCARD_SYSTEM, f"Generate study flashcards from:\n{text}{topic_hint}")
        cards = result.get("cards") or result if isinstance(result, list) else []
        if isinstance(result, dict) and "cards" in result:
            cards = result["cards"]

        db.query(Flashcard).filter(Flashcard.document_id == document_id).delete()
        now = datetime.now(UTC)
        for item in cards:
            if not isinstance(item, dict):
                continue
            q = str(item.get("question", "")).strip()
            a = str(item.get("answer", "")).strip()
            if not q or not a:
                continue
            fc = Flashcard(
                document_id=document_id,
                question=q,
                answer=a,
                section_tag=str(item.get("section_tag", "")),
                next_review_at=now,
            )
            db.add(fc)
        db.commit()
        mark_job_completed(db, job_id)
    except Exception as exc:
        db.rollback()
        mark_job_failed(db, job_id, str(exc))
        raise
