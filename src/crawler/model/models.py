from src.crawler.model.hash import Hash
from datetime import datetime
from typing import TypedDict
from enum import Enum


class URLCategory(Enum):
    SEED = 0
    LEAF = 1
    EXTERNAL = 2


class URLRecord(TypedDict):
    url_hash:     Hash
    category:     URLCategory | None
    domain_queue: int | None
    domain_hash:  Hash | None
    url:          str


class DownloadRecord(TypedDict):
    url_hash:   Hash
    html_hash:  Hash | None
    category:   URLCategory | None
    url:        str
    html:       str | None
    status:     int | None
    visited_on: datetime | None


class DatabaseHtmlDoc(TypedDict):
    url_hash:         Hash
    html_hash:        Hash
    num_of_downloads: int
    last_visit_on:    datetime
    first_visit_on:   datetime
