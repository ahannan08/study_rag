from dataclasses import dataclass
from pathlib import Path

import fitz
from docx import Document as DocxDocument

from app.services.ingestion.chunker import chunk_pages
from app.services.ingestion.types import PageBlock


def extract_document(path: str) -> list[PageBlock]:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return _extract_pdf(path)
    if ext in {".docx", ".doc"}:
        return _extract_docx(path)
    raise ValueError(f"Unsupported file type: {ext}")


def _extract_pdf(path: str) -> list[PageBlock]:
    blocks: list[PageBlock] = []
    with fitz.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if not text:
                continue
            label = page.get_label() or None
            blocks.append(PageBlock(logical_page=i, text=text, source_page_label=label))
    return blocks


def _extract_docx(path: str) -> list[PageBlock]:
    doc = DocxDocument(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    full = "\n\n".join(paragraphs)
    if not full:
        return []
    # Pseudo-pages ~3000 chars
    page_size = 3000
    blocks: list[PageBlock] = []
    logical = 1
    for start in range(0, len(full), page_size):
        blocks.append(PageBlock(logical_page=logical, text=full[start : start + page_size]))
        logical += 1
    return blocks


def extract_and_chunk(path: str) -> list[dict]:
    pages = extract_document(path)
    return chunk_pages(pages)
