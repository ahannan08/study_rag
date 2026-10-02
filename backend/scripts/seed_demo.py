#!/usr/bin/env python3
"""Load demo_bundle.json into Postgres for fresh local/docker DBs."""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Document, DocumentStatus, Flashcard, User
from app.services.auth_service import hash_password

DEMO_USER_EMAIL = "demo@local.study-rag"
DEMO_USER_PASSWORD = "demo-not-for-production"


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def seed(db: Session, bundle_path: Path) -> None:
    raw = json.loads(bundle_path.read_text(encoding="utf-8"))
    user = db.query(User).filter(User.email == DEMO_USER_EMAIL).one_or_none()
    if not user:
        user = User(email=DEMO_USER_EMAIL, hashed_password=hash_password(DEMO_USER_PASSWORD))
        db.add(user)
        db.flush()

    for entry in raw.get("documents", []):
        snap = entry["snapshot"]
        doc_data = snap["document"]
        doc_id = uuid.UUID(doc_data["id"])

        doc = db.query(Document).filter(Document.id == doc_id).one_or_none()
        if not doc:
            doc = Document(
                id=doc_id,
                user_id=user.id,
                title=doc_data["title"],
                status=DocumentStatus.INDEXED.value,
                blob_path="demo://snapshot",
                faiss_path=None,
            )
            db.add(doc)
        else:
            doc.title = doc_data["title"]
            doc.status = DocumentStatus.INDEXED.value

        doc.topic_map = doc_data.get("topic_map")
        doc.topic_map_at = parse_dt(doc_data.get("topic_map_at"))

        db.query(Flashcard).filter(Flashcard.document_id == doc_id).delete()
        for fc in snap.get("flashcards", []):
            db.add(
                Flashcard(
                    id=uuid.UUID(fc["id"]),
                    document_id=doc_id,
                    question=fc["question"],
                    answer=fc["answer"],
                    section_tag=fc.get("section_tag") or "",
                    next_review_at=parse_dt(fc.get("next_review_at")),
                )
            )

    db.commit()
    print(f"Seeded {len(raw.get('documents', []))} demo document(s) for {DEMO_USER_EMAIL}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bundle",
        type=Path,
        default=Path("demo/demo_bundle.json"),
        help="Path to demo bundle (relative to backend/)",
    )
    args = parser.parse_args()
    backend_root = Path(__file__).resolve().parent.parent
    bundle_path = args.bundle if args.bundle.is_absolute() else backend_root / args.bundle
    if not bundle_path.is_file():
        raise SystemExit(f"Bundle not found: {bundle_path}")

    db = SessionLocal()
    try:
        seed(db, bundle_path)
    finally:
        db.close()


if __name__ == "__main__":
    main()
