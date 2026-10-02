from app.db.base import Base
from app.db.session import engine
from app.models import (  # noqa: F401 — register models
    chunk,
    document,
    flashcard,
    job,
    question_log,
    review_log,
    user,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
