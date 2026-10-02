from dataclasses import dataclass


@dataclass
class PageBlock:
    logical_page: int
    text: str
    source_page_label: str | None = None
