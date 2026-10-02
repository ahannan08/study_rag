import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_document
from app.db.session import get_db
from app.models import User
from app.schemas.topic_map import TopicMapGenerateResponse, TopicMapOut
from app.services.document_service import start_topic_map_job

router = APIRouter(tags=["topic-map"])


@router.get("/documents/{document_id}/topic-map", response_model=TopicMapOut)
def get_topic_map(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TopicMapOut:
    doc = get_owned_document(db, user, document_id)
    if not doc.topic_map or not doc.topic_map_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic map not generated")
    return TopicMapOut(document_id=doc.id, topic_map=doc.topic_map, generated_at=doc.topic_map_at)


@router.post(
    "/documents/{document_id}/topic-map/generate",
    response_model=TopicMapGenerateResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_topic_map(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TopicMapGenerateResponse:
    doc = get_owned_document(db, user, document_id)
    if not doc.indexed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document must be indexed first")
    job = start_topic_map_job(db, user.id, doc.id)
    return TopicMapGenerateResponse(job_id=job.id)
