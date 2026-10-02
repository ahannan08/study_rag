import uuid
from datetime import UTC, datetime

from redis import Redis
from rq import Queue
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Job, JobStatus, JobType

settings = get_settings()


def get_queue() -> Queue:
    conn = Redis.from_url(settings.redis_url)
    return Queue(connection=conn)


def create_job(db: Session, user_id: uuid.UUID, document_id: uuid.UUID, job_type: JobType) -> Job:
    job = Job(
        user_id=user_id,
        document_id=document_id,
        type=job_type.value,
        status=JobStatus.QUEUED.value,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def enqueue_job(job: Job, task_name: str, *args: str) -> None:
    q = get_queue()
    q.enqueue(task_name, *args, job_id=str(job.id))


def update_job(db: Session, job_id: uuid.UUID, **fields) -> None:
    job = db.query(Job).filter(Job.id == job_id).one()
    for k, v in fields.items():
        setattr(job, k, v)
    db.commit()


def mark_job_running(db: Session, job_id: uuid.UUID, stage: str) -> None:
    update_job(
        db,
        job_id,
        status=JobStatus.RUNNING.value,
        stage=stage,
        started_at=datetime.now(UTC),
        error=None,
    )


def mark_job_completed(db: Session, job_id: uuid.UUID) -> None:
    update_job(
        db,
        job_id,
        status=JobStatus.COMPLETED.value,
        stage="done",
        progress=100,
        finished_at=datetime.now(UTC),
    )


def mark_job_failed(db: Session, job_id: uuid.UUID, error: str) -> None:
    update_job(
        db,
        job_id,
        status=JobStatus.FAILED.value,
        error=error[:2000],
        finished_at=datetime.now(UTC),
    )
