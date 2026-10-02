import uuid

from app.db.session import SessionLocal
from app.services.flashcard_gen_service import run_flashcard_generation
from app.services.ingestion.pipeline import run_ingest_index
from app.services.topic_map_service import run_topic_map_generation


def run_ingest_index_task(job_id: str, document_id: str) -> None:
    db = SessionLocal()
    try:
        run_ingest_index(db, uuid.UUID(job_id), uuid.UUID(document_id))
    finally:
        db.close()


def run_topic_map_task(job_id: str, document_id: str) -> None:
    db = SessionLocal()
    try:
        run_topic_map_generation(db, uuid.UUID(job_id), uuid.UUID(document_id))
    finally:
        db.close()


def run_flashcards_task(job_id: str, document_id: str) -> None:
    db = SessionLocal()
    try:
        run_flashcard_generation(db, uuid.UUID(job_id), uuid.UUID(document_id))
    finally:
        db.close()
