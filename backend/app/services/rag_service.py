import uuid

from sqlalchemy.orm import Session

from app.infrastructure.llm.grok_client import GrokClient
from app.infrastructure.llm.prompts import RAG_SYSTEM
from app.models import Chunk, QuestionLog
from app.schemas.chat import ChatOut, CitationOut
from app.services.coverage import CoverageLabel, label_from_scores
from app.services.retrieval_service import retrieve_chunks


def build_citation(chunk: Chunk) -> CitationOut:
    section = chunk.section_path.split(">")[-1].strip() if chunk.section_path else "Document"
    excerpt = chunk.text[:200].replace("\n", " ")
    label = f'After section "{section}" (document page {chunk.logical_page})'
    return CitationOut(
        chunk_id=chunk.id,
        logical_page=chunk.logical_page,
        section_path=chunk.section_path,
        excerpt=excerpt,
        label=label,
    )


def ask_document(db: Session, user_id: uuid.UUID, document_id: uuid.UUID, question: str) -> ChatOut:
    retrieved = retrieve_chunks(db, document_id, question)
    scores = [s for _, s in retrieved]
    coverage = label_from_scores(scores)

    if coverage == CoverageLabel.NOT_IN_DOCUMENT or not retrieved:
        log = QuestionLog(
            document_id=document_id,
            user_id=user_id,
            question=question,
            matched_chunk_ids=[],
            coverage_label=coverage.value,
            section_tag="",
            answer_snapshot="Not covered in this document.",
        )
        db.add(log)
        db.commit()
        return ChatOut(
            answer="This is not covered in this document.",
            citations=[],
            coverage_label=coverage.value,
            chunk_ids_used=[],
            refusal=True,
        )

    chunk_map = {str(c.id): c for c, _ in retrieved}
    context_lines = []
    for chunk, _ in retrieved:
        context_lines.append(f"chunk_id={chunk.id}\nsection={chunk.section_path}\n{chunk.text}")
    user_prompt = f"Question: {question}\n\nContext:\n" + "\n---\n".join(context_lines)

    grok = GrokClient()
    result = grok.chat_json(RAG_SYSTEM, user_prompt)
    answer = str(result.get("answer", ""))
    refusal = bool(result.get("refusal", False))
    raw_ids = result.get("chunk_ids") or []
    used_ids: list[uuid.UUID] = []
    for cid in raw_ids:
        try:
            used_ids.append(uuid.UUID(str(cid)))
        except ValueError:
            continue

    citations = []
    for cid in used_ids:
        ch = chunk_map.get(str(cid))
        if ch:
            citations.append(build_citation(ch))

    section_tag = retrieved[0][0].section_path if retrieved else ""
    log = QuestionLog(
        document_id=document_id,
        user_id=user_id,
        question=question,
        matched_chunk_ids=[str(c.id) for c, _ in retrieved],
        coverage_label=coverage.value,
        section_tag=section_tag,
        answer_snapshot=answer,
    )
    db.add(log)
    db.commit()

    return ChatOut(
        answer=answer,
        citations=citations,
        coverage_label=coverage.value,
        chunk_ids_used=used_ids,
        refusal=refusal,
    )
