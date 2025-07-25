
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import LOG_FILE

# ── Formatter ---------------------------------------------------------------
_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

def _build_file_handler(log_path: Path) -> RotatingFileHandler:
    """
    1 MB rotating log, keeps last 3 files (…log.1, …log.2).
    """
    handler = RotatingFileHandler(
        log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf‑8",
    )
    handler.setFormatter(logging.Formatter(_FMT, _DATEFMT))
    return handler

def _build_stream_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(_FMT, _DATEFMT))
    return handler

def _configure_root() -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:                   # avoid duplicates on reload
        root.addHandler(_build_stream_handler())
        root.addHandler(_build_file_handler(LOG_FILE))

_configure_root()

def get_logger(name: str | None = None) -> logging.Logger:  # noqa: D401
    """Return a module‑scoped logger with our standard formatting."""
    return logging.getLogger(name)
