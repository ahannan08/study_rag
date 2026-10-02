import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_document
from app.db.session import get_db
from app.models import User
from app.schemas.progress import ProgressOut, WeakPointsResponse
from app.services.weak_point_service import get_progress, get_weak_points

router = APIRouter(tags=["progress"])


@router.get("/documents/{document_id}/progress", response_model=ProgressOut)
def progress(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProgressOut:
    get_owned_document(db, user, document_id)
    return get_progress(db, document_id)


@router.get("/documents/{document_id}/weak-points", response_model=WeakPointsResponse)
def weak_points(
    document_id: uuid.UUID,
    phrase: bool = Query(default=True),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> WeakPointsResponse:
    get_owned_document(db, user, document_id)
    return get_weak_points(db, document_id, phrase=phrase)
