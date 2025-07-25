
from __future__ import annotations

from pathlib import Path
from typing import Optional, Iterable

import fitz  # PyMuPDF
from src.utils.logger import get_logger

log = get_logger(__name__)


def _candidate_passwords(username: Optional[str], password: Optional[str]) -> Iterable[str]:
    seen = set()
    for value in (password, username):
        if value:
            v = value.strip()
            if v and v not in seen:
                seen.add(v)
                yield v
    # also try empty string as a last resort (some PDFs are "encrypted" but blank)
    yield ""


def open_document(pdf_path: Path, username: str | None = None, password: str | None = None) -> fitz.Document:
    """
    Attempt to open a (possibly encrypted) PDF with any provided credentials.

    Raises:
        RuntimeError: if the PDF cannot be opened with given credentials.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    doc = fitz.open(pdf_path)
    if not doc.needs_pass:
        log.info("Opened unencrypted PDF: %s", pdf_path)
        return doc

    # Try each candidate password with authenticate()
    for cand in _candidate_passwords(username, password):
        try:
            if doc.authenticate(cand):
                log.info("Unlocked PDF %s with provided credentials.", pdf_path)
                return doc
        except Exception as exc:
            log.exception("Unexpected error while authenticating %s: %s", pdf_path, exc)

    doc.close()
    raise RuntimeError(f"Failed to unlock PDF: {pdf_path.name}. Check username/password.")
