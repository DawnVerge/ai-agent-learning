"""Load and fingerprint the same PDF bytes for indexing."""

import hashlib
from pathlib import Path
from urllib.parse import urlparse

import requests


class PdfBytesStore:
    def read(self, source: str) -> bytes:
        parsed = urlparse(source)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            response = requests.get(source, timeout=30)
            response.raise_for_status()
            return response.content
        return Path(source).read_bytes()

    def compute_hash(self, pdf_bytes: bytes) -> str:
        return hashlib.sha256(pdf_bytes).hexdigest()
