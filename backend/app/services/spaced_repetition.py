from datetime import UTC, datetime, timedelta

from app.models import Flashcard


def sm2_update(card: Flashcard, correct: bool) -> Flashcard:
    """SM-2 inspired scheduler."""
    now = datetime.now(UTC)
    if card.ease_factor is None:
        card.ease_factor = 2.5
    if card.interval_days is None:
        card.interval_days = 0
    if card.repetitions is None:
        card.repetitions = 0
    if correct:
        if card.repetitions == 0:
            card.interval_days = 1
        elif card.repetitions == 1:
            card.interval_days = 6
        else:
            card.interval_days = max(1, int(round(card.interval_days * card.ease_factor)))
        card.repetitions += 1
        card.next_review_at = now + timedelta(days=card.interval_days)
    else:
        card.repetitions = 0
        card.interval_days = 1
        card.next_review_at = now + timedelta(days=1)
        card.ease_factor = max(1.3, card.ease_factor - 0.2)
    if correct:
        card.ease_factor = min(2.5, card.ease_factor + 0.1)
    return card
