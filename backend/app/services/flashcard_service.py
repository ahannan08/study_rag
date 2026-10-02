import uuid

from sqlalchemy.orm import Session

from app.models import Flashcard, ReviewLog
from app.services.spaced_repetition import sm2_update


def list_flashcards(db: Session, document_id: uuid.UUID) -> list[Flashcard]:
    return db.query(Flashcard).filter(Flashcard.document_id == document_id).order_by(Flashcard.section_tag).all()


def due_flashcards(db: Session, user_id: uuid.UUID) -> list[Flashcard]:
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    from app.models import Document

    return (
        db.query(Flashcard)
        .join(Document, Flashcard.document_id == Document.id)
        .filter(Document.user_id == user_id)
        .filter((Flashcard.next_review_at.is_(None)) | (Flashcard.next_review_at <= now))
        .order_by(Flashcard.next_review_at.nullsfirst())
        .all()
    )


def review_flashcard(db: Session, user_id: uuid.UUID, flashcard_id: uuid.UUID, correct: bool) -> Flashcard:
    from app.models import Document

    card = (
        db.query(Flashcard)
        .join(Document, Flashcard.document_id == Document.id)
        .filter(Flashcard.id == flashcard_id, Document.user_id == user_id)
        .one_or_none()
    )
    if not card:
        raise LookupError("Flashcard not found")
    sm2_update(card, correct)
    log = ReviewLog(
        flashcard_id=card.id,
        user_id=user_id,
        correct=correct,
        next_review_at=card.next_review_at,
    )
    db.add(log)
    db.commit()
    db.refresh(card)
    return card
