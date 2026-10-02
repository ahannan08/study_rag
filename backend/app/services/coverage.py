import enum

from app.config import get_settings


class CoverageLabel(str, enum.Enum):
    FULLY_COVERED = "fully_covered"
    PARTIALLY_COVERED = "partially_covered"
    NOT_IN_DOCUMENT = "not_in_document"


def label_from_scores(scores: list[float]) -> CoverageLabel:
    if not scores:
        return CoverageLabel.NOT_IN_DOCUMENT
    best = max(scores)
    settings = get_settings()
    if best >= settings.coverage_full_threshold:
        return CoverageLabel.FULLY_COVERED
    if best >= settings.coverage_partial_threshold:
        return CoverageLabel.PARTIALLY_COVERED
    return CoverageLabel.NOT_IN_DOCUMENT
