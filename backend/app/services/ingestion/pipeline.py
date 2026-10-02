import uuid

from sqlalchemy.orm import Session

from app.infrastructure.storage.file_store import FileStore
from app.models import Chunk, Document, DocumentStatus, JobType
from app.services.faiss_store import FaissStore
from app.services.ingestion.extractors import extract_and_chunk
from app.infrastructure.embeddings.minilm import encode_texts
from app.services.job_service import mark_job_completed, mark_job_failed, mark_job_running
def run_ingest_index(db: Session, job_id: uuid.UUID, document_id: uuid.UUID) -> None:
    doc = db.query(Document).filter(Document.id == document_id).one()
    try:
        mark_job_running(db, job_id, "parsing")
        doc.status = DocumentStatus.INDEXING.value
        db.commit()

        db.query(Chunk).filter(Chunk.document_id == document_id).delete()
        FaissStore(document_id).delete_files()

        drafts = extract_and_chunk(doc.blob_path)
        if not drafts:
            raise ValueError("No text extracted from document")

        mark_job_running(db, job_id, "embedding")
        texts = [d["text"] for d in drafts]
        vectors = encode_texts(texts)

        mark_job_running(db, job_id, "storing")
        chunk_ids: list[uuid.UUID] = []
        chunks: list[Chunk] = []
        for i, draft in enumerate(drafts):
            ch = Chunk(
                document_id=document_id,
                text=draft["text"],
                logical_page=draft["logical_page"],
                section_path=draft["section_path"],
                paragraph_index=draft["paragraph_index"],
                source_page_label=draft.get("source_page_label"),
                faiss_row_id=i,
            )
            chunks.append(ch)
        db.add_all(chunks)
        db.flush()
        chunk_ids = [c.id for c in chunks]

        store = FaissStore(document_id)
        faiss_path = store.build(chunk_ids, vectors)

        doc.faiss_path = faiss_path
        doc.status = DocumentStatus.INDEXED.value
        db.commit()
        mark_job_completed(db, job_id)
    except Exception as exc:
        db.rollback()
        doc = db.query(Document).filter(Document.id == document_id).one_or_none()
        if doc:
            doc.status = DocumentStatus.FAILED.value
            db.commit()
        mark_job_failed(db, job_id, str(exc))
        raise


def delete_document_assets(db: Session, doc: Document) -> None:
    FileStore().delete_file(doc.blob_path)
    if doc.faiss_path:
        FaissStore(doc.id).delete_files()
    db.delete(doc)
    db.commit()
