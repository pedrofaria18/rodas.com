from typing import TypedDict
from datetime import datetime
import hashlib


class Hash:
    """Esta classe implementa um método para calcular o checksum de uma string."""
    value: bytes = None

    def __init__(self, content: str = None, hex_hash: str = None):
        if content is None and hex_hash is None:
            raise ValueError('É necessário informar o conteúdo ou o hex_hash, não ambos.')
        if hex_hash is None:
            self.value = hashlib.md5(content.encode()).digest()
        else:
            self.value = bytes.fromhex(hex_hash)

    def __eq__(self, other):
        if isinstance(other, Hash):
            return self.value == other.value
        return False

    def hexdigest(self):
        return self.value.hex()

    def equals(self, other: str):
        return self.value == hashlib.md5(other.encode()).digest()


class DownloadRecord(TypedDict):
    url_hash:   Hash
    html_hash:  Hash | None
    url:        str
    html:       str | None
    status:     int | None
    visited_on: datetime | None


class HTMLDocumentRecord(TypedDict):
    id:               int
    url_hash:         Hash
    html_hash:        Hash
    num_of_downloads: int
    last_visit_on:    datetime
    first_visit_on:   datetime
