import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_document
from app.db.session import get_db
from app.models import User
from app.schemas.chat import ChatIn, ChatOut
from app.services.rag_service import ask_document

router = APIRouter(tags=["chat"])


@router.post("/documents/{document_id}/chat", response_model=ChatOut)
def chat(
    document_id: uuid.UUID,
    body: ChatIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ChatOut:
    doc = get_owned_document(db, user, document_id)
    if not doc.indexed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document must be indexed first")
    return ask_document(db, user.id, document_id, body.question)
