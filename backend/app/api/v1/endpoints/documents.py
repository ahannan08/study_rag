import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_owned_document
from app.config import get_settings
from app.db.session import get_db
from app.infrastructure.storage.file_store import FileStore
from app.models import Document, DocumentStatus, Job, User
from app.schemas.document import DocumentDetailOut, DocumentOut, DocumentUploadResponse
from app.services.document_service import document_to_out, start_ingest_job
from app.services.ingestion.pipeline import delete_document_assets

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DocumentUploadResponse:
    settings = get_settings()
    data = await file.read()
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename required")
    ext = file.filename.lower().split(".")[-1]
    if ext not in {"pdf", "docx", "doc"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF and DOCX supported")

    doc_id = uuid.uuid4()
    store = FileStore()
    path = store.save_upload(user.id, doc_id, file.filename, data)
    doc = Document(
        id=doc_id,
        user_id=user.id,
        title=file.filename,
        blob_path=path,
        status=DocumentStatus.UPLOADING.value,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    job = start_ingest_job(db, user.id, doc.id)
    return DocumentUploadResponse(document_id=doc.id, job_id=job.id)


@router.get("", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[DocumentOut]:
    docs = db.query(Document).filter(Document.user_id == user.id).order_by(Document.uploaded_at.desc()).all()
    return [DocumentOut(**document_to_out(d, db)) for d in docs]


@router.get("/{document_id}", response_model=DocumentDetailOut)
def get_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DocumentDetailOut:
    doc = get_owned_document(db, user, document_id)
    base = document_to_out(doc, db)
    return DocumentDetailOut(**base, topic_map=doc.topic_map, topic_map_at=doc.topic_map_at)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    doc = get_owned_document(db, user, document_id)
    delete_document_assets(db, doc)
