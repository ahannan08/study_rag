#!/usr/bin/env python3
"""Export indexed documents from Postgres into a demo bundle + frontend static JSON."""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Document, DocumentStatus, Flashcard, QuestionLog, User
from app.services.document_service import document_to_out
from app.services.weak_point_service import get_progress, get_weak_points


def _json_default(obj: object) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(type(obj))


def _flashcard_out(fc: Flashcard) -> dict:
    return {
        "id": str(fc.id),
        "document_id": str(fc.document_id),
        "question": fc.question,
        "answer": fc.answer,
        "section_tag": fc.section_tag or "",
        "next_review_at": fc.next_review_at.isoformat() if fc.next_review_at else None,
    }


def _chat_samples(db: Session, document_id: uuid.UUID, flashcards: list[Flashcard]) -> list[dict]:
    logs = (
        db.query(QuestionLog)
        .filter(QuestionLog.document_id == document_id)
        .order_by(QuestionLog.created_at.desc())
        .limit(10)
        .all()
    )
    samples: list[dict] = []
    for log in logs:
        if not log.answer_snapshot:
            continue
        samples.append(
            {
                "question": log.question,
                "answer": log.answer_snapshot,
                "coverage_label": log.coverage_label,
                "citations": [],
            }
        )
        if len(samples) >= 3:
            break

    if not samples and flashcards:
        fc = flashcards[0]
        samples.append(
            {
                "question": f"What is covered about: {fc.question[:80]}?",
                "answer": fc.answer,
                "coverage_label": "fully_covered",
                "citations": [
                    {
                        "chunk_id": "demo",
                        "logical_page": 1,
                        "section_path": fc.section_tag or "General",
                        "excerpt": fc.answer[:200],
                        "label": fc.section_tag or "Document",
                    }
                ],
            }
        )
        if len(flashcards) > 1:
            fc2 = flashcards[1]
            samples.append(
                {
                    "question": fc2.question,
                    "answer": fc2.answer,
                    "coverage_label": "fully_covered",
                    "citations": [],
                }
            )
    return samples


def build_document_snapshot(db: Session, doc: Document) -> dict:
    flashcards = db.query(Flashcard).filter(Flashcard.document_id == doc.id).order_by(Flashcard.section_tag).all()
    meta = document_to_out(doc, db)
    meta["id"] = str(meta["id"])
    meta["uploaded_at"] = doc.uploaded_at.isoformat()
    detail = {
        **meta,
        "topic_map": doc.topic_map,
        "topic_map_at": doc.topic_map_at.isoformat() if doc.topic_map_at else None,
    }
    progress = get_progress(db, doc.id)
    weak = get_weak_points(db, doc.id, phrase=False)
    return {
        "document": detail,
        "flashcards": [_flashcard_out(fc) for fc in flashcards],
        "progress": progress.model_dump(),
        "weak_points": weak.model_dump(),
        "chat_samples": _chat_samples(db, doc.id, flashcards),
    }


def collect_documents(
    db: Session,
    *,
    document_ids: list[uuid.UUID] | None,
    all_indexed: bool,
    user_email: str | None,
) -> list[Document]:
    q = db.query(Document)
    if document_ids:
        q = q.filter(Document.id.in_(document_ids))
    elif user_email:
        user = db.query(User).filter(User.email == user_email).one_or_none()
        if not user:
            raise SystemExit(f"No user with email {user_email}")
        q = q.filter(Document.user_id == user.id)
    docs = q.order_by(Document.uploaded_at).all()
    if all_indexed and not document_ids:
        docs = [d for d in docs if d.status == DocumentStatus.INDEXED.value]
    if not docs:
        raise SystemExit("No documents matched export criteria")
    return docs


def write_outputs(bundle: dict, out_bundle: Path, out_frontend: Path | None) -> None:
    out_bundle.parent.mkdir(parents=True, exist_ok=True)
    out_bundle.write_text(json.dumps(bundle, indent=2, default=_json_default), encoding="utf-8")

    if not out_frontend:
        return

    documents = bundle["documents"]
    manifest_docs = []
    docs_dir = out_frontend / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)

    for entry in documents:
        snap = entry["snapshot"]
        doc_meta = snap["document"]
        manifest_docs.append(
            {
                "id": doc_meta["id"],
                "title": doc_meta["title"],
                "status": doc_meta["status"],
                "uploaded_at": doc_meta["uploaded_at"],
                "indexed": doc_meta["indexed"],
                "topic_map_ready": doc_meta["topic_map_ready"],
                "flashcards_ready": doc_meta["flashcards_ready"],
                "chunk_count": doc_meta["chunk_count"],
            }
        )
        doc_path = docs_dir / f"{doc_meta['id']}.json"
        doc_path.write_text(json.dumps(snap, indent=2, default=_json_default), encoding="utf-8")

    out_frontend.mkdir(parents=True, exist_ok=True)
    (out_frontend / "manifest.json").write_text(
        json.dumps({"documents": manifest_docs}, indent=2, default=_json_default),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Export demo snapshot from Postgres")
    parser.add_argument("--document-id", action="append", dest="document_ids", help="Document UUID (repeatable)")
    parser.add_argument("--all-indexed", action="store_true", help="All indexed documents")
    parser.add_argument("--user-email", help="All documents for user email")
    parser.add_argument(
        "--out-bundle",
        type=Path,
        default=Path("demo/demo_bundle.json"),
        help="Canonical bundle path (relative to backend/)",
    )
    parser.add_argument(
        "--out-frontend",
        type=Path,
        default=Path("../frontend/public/demo"),
        help="Frontend public demo directory",
    )
    args = parser.parse_args()

    if not args.all_indexed and not args.document_ids and not args.user_email:
        args.all_indexed = True

    ids = [uuid.UUID(x) for x in args.document_ids] if args.document_ids else None

    db: Session = SessionLocal()
    try:
        docs = collect_documents(
            db,
            document_ids=ids,
            all_indexed=args.all_indexed,
            user_email=args.user_email,
        )
        bundle = {
            "version": 1,
            "exported_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "documents": [{"snapshot": build_document_snapshot(db, doc)} for doc in docs],
        }
        backend_root = Path(__file__).resolve().parent.parent
        out_bundle = args.out_bundle if args.out_bundle.is_absolute() else backend_root / args.out_bundle
        out_frontend = args.out_frontend if args.out_frontend.is_absolute() else backend_root / args.out_frontend
        write_outputs(bundle, out_bundle, out_frontend)
        print(f"Exported {len(docs)} document(s)")
        print(f"  bundle: {out_bundle}")
        print(f"  frontend: {out_frontend}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
