import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_document
from app.db.session import get_db
from app.models import User
from app.schemas.flashcard import (
    FlashcardGenerateResponse,
    FlashcardOut,
    FlashcardReviewIn,
    FlashcardReviewOut,
)
from app.services.document_service import start_flashcards_job
from app.services.flashcard_service import due_flashcards, list_flashcards, review_flashcard

router = APIRouter(tags=["flashcards"])


@router.get("/documents/{document_id}/flashcards", response_model=list[FlashcardOut])
def get_flashcards(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[FlashcardOut]:
    get_owned_document(db, user, document_id)
    return list_flashcards(db, document_id)


@router.post(
    "/documents/{document_id}/flashcards/generate",
    response_model=FlashcardGenerateResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_flashcards(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FlashcardGenerateResponse:
    doc = get_owned_document(db, user, document_id)
    if not doc.indexed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document must be indexed first")
    job = start_flashcards_job(db, user.id, doc.id)
    return FlashcardGenerateResponse(job_id=job.id)


@router.get("/flashcards/due", response_model=list[FlashcardOut])
def get_due_flashcards(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[FlashcardOut]:
    return due_flashcards(db, user.id)


@router.post("/flashcards/{flashcard_id}/review", response_model=FlashcardReviewOut)
def submit_review(
    flashcard_id: uuid.UUID,
    body: FlashcardReviewIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> FlashcardReviewOut:
    try:
        card = review_flashcard(db, user.id, flashcard_id, body.correct)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return FlashcardReviewOut(
        flashcard_id=card.id,
        next_review_at=card.next_review_at,
        interval_days=card.interval_days,
        ease_factor=card.ease_factor,
    )
