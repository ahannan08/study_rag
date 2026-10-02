import uuid
from collections import defaultdict

from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.llm.grok_client import GrokClient
from app.infrastructure.llm.prompts import WEAK_POINT_SYSTEM
from app.models import Flashcard, QuestionLog, ReviewLog
from app.schemas.progress import ProgressOut, SectionStat, WeakPointOut, WeakPointsResponse


def get_progress(db: Session, document_id: uuid.UUID) -> ProgressOut:
    q_logs = db.query(QuestionLog).filter(QuestionLog.document_id == document_id).all()
    flashcard_ids = [f.id for f in db.query(Flashcard.id).filter(Flashcard.document_id == document_id).all()]
    r_logs: list[ReviewLog] = []
    if flashcard_ids:
        r_logs = db.query(ReviewLog).filter(ReviewLog.flashcard_id.in_(flashcard_ids)).all()

    sections: dict[str, dict] = defaultdict(lambda: {"q": 0, "r": 0, "errors": 0, "attempts": 0})

    for q in q_logs:
        tag = q.section_tag or "General"
        sections[tag]["q"] += 1

    fc_section = {f.id: f.section_tag or "General" for f in db.query(Flashcard).filter(Flashcard.document_id == document_id)}
    for r in r_logs:
        tag = fc_section.get(r.flashcard_id, "General")
        sections[tag]["r"] += 1
        sections[tag]["attempts"] += 1
        if not r.correct:
            sections[tag]["errors"] += 1

    stats: list[SectionStat] = []
    for tag, data in sections.items():
        rate = None
        if data["attempts"] > 0:
            rate = data["errors"] / data["attempts"]
        stats.append(
            SectionStat(
                section_tag=tag,
                question_count=data["q"],
                review_count=data["r"],
                error_rate=rate,
            )
        )

    return ProgressOut(
        document_id=str(document_id),
        sections=stats,
        total_questions=len(q_logs),
        total_reviews=len(r_logs),
    )


def get_weak_points(db: Session, document_id: uuid.UUID, phrase: bool = True) -> WeakPointsResponse:
    progress = get_progress(db, document_id)
    settings = get_settings()
    weak: list[WeakPointOut] = []
    grok = GrokClient() if phrase and settings.xai_api_key else None

    for sec in progress.sections:
        if sec.error_rate is None:
            continue
        if sec.error_rate >= settings.weak_point_error_threshold:
            suggestion = None
            if grok:
                try:
                    res = grok.chat_json(
                        WEAK_POINT_SYSTEM,
                        f"Topic: {sec.section_tag}. Error rate: {sec.error_rate:.0%}. Reviews: {sec.review_count}.",
                    )
                    suggestion = res.get("suggestion")
                except Exception:
                    suggestion = None
            weak.append(
                WeakPointOut(
                    section_tag=sec.section_tag,
                    error_rate=sec.error_rate,
                    suggestion_text=suggestion,
                )
            )
    return WeakPointsResponse(weak_points=weak)
