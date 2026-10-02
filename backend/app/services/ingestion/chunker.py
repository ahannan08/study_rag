import re
from dataclasses import dataclass

from app.services.ingestion.types import PageBlock

HEADING_RE = re.compile(r"^(#{1,6}\s+|Chapter\s+\d+|Section\s+\d+|\d+\.\s+[A-Z])", re.I)


@dataclass
class ChunkDraft:
    text: str
    logical_page: int
    section_path: str
    paragraph_index: int
    source_page_label: str | None


def chunk_pages(pages: list[PageBlock], max_chars: int = 1200, overlap: int = 150) -> list[dict]:
    drafts: list[ChunkDraft] = []
    section_stack: list[str] = ["Document"]
    para_idx = 0

    for page in pages:
        parts = [p.strip() for p in page.text.split("\n\n") if p.strip()]
        for part in parts:
            if _is_heading(part):
                title = part.strip("# ").strip()
                section_stack = [section_stack[0], title] if len(section_stack) > 0 else [title]
            section_path = " > ".join(section_stack[-2:]) if len(section_stack) >= 2 else section_stack[-1]
            for sub in _split_text(part, max_chars, overlap):
                drafts.append(
                    ChunkDraft(
                        text=sub,
                        logical_page=page.logical_page,
                        section_path=section_path,
                        paragraph_index=para_idx,
                        source_page_label=page.source_page_label,
                    )
                )
                para_idx += 1

    return [
        {
            "text": d.text,
            "logical_page": d.logical_page,
            "section_path": d.section_path,
            "paragraph_index": d.paragraph_index,
            "source_page_label": d.source_page_label,
        }
        for d in drafts
        if d.text.strip()
    ]


def _is_heading(text: str) -> bool:
    first_line = text.split("\n", 1)[0].strip()
    if len(first_line) > 120:
        return False
    return bool(HEADING_RE.match(first_line)) or (first_line.isupper() and len(first_line.split()) <= 8)


def _split_text(text: str, max_chars: int, overlap: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_chars)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks
