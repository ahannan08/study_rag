import uuid

from sqlalchemy.orm import Session

from app.models import Chunk, Document, Job, JobType
from app.services.job_service import create_job
from app.worker.tasks import (
    run_flashcards_task,
    run_ingest_index_task,
    run_topic_map_task,
)


def document_to_out(doc: Document, db: Session) -> dict:
    from app.models import Flashcard

    count = db.query(Chunk).filter(Chunk.document_id == doc.id).count()
    fc_n = db.query(Flashcard).filter(Flashcard.document_id == doc.id).count()
    return {
        "id": doc.id,
        "title": doc.title,
        "status": doc.status,
        "uploaded_at": doc.uploaded_at,
        "indexed": doc.indexed,
        "topic_map_ready": doc.topic_map is not None,
        "flashcards_ready": fc_n > 0,
        "chunk_count": count,
    }


def start_ingest_job(db: Session, user_id: uuid.UUID, document_id: uuid.UUID) -> Job:
    return create_job(db, user_id, document_id, JobType.INGEST_INDEX)


def start_topic_map_job(db: Session, user_id: uuid.UUID, document_id: uuid.UUID) -> Job:
    return create_job(db, user_id, document_id, JobType.TOPIC_MAP)


def start_flashcards_job(db: Session, user_id: uuid.UUID, document_id: uuid.UUID) -> Job:
    return create_job(db, user_id, document_id, JobType.FLASHCARDS)


def schedule_ingest(job_id: uuid.UUID, document_id: uuid.UUID) -> None:
    run_ingest_index_task(str(job_id), str(document_id))


def schedule_topic_map(job_id: uuid.UUID, document_id: uuid.UUID) -> None:
    run_topic_map_task(str(job_id), str(document_id))


def schedule_flashcards(job_id: uuid.UUID, document_id: uuid.UUID) -> None:
    run_flashcards_task(str(job_id), str(document_id))
