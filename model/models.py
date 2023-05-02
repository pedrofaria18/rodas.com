from typing import TypedDict
from datetime import datetime


class DownloadResult(TypedDict):
    url: str
    html_doc: str | None
    status: int | None
    visited_at: datetime | None


class HTMLDocument(TypedDict):
    id: int
    url_hash: str
    html_hash: str
    url: str
    html_doc: str
    visit_count: int
    is_active: bool
    created_at: datetime
    visited_at: datetime
