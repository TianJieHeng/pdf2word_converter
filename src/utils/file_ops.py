
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable

from src.config import WORD_DOCS_DIR
from src.utils.logger import get_logger

log = get_logger(__name__)


def copy_to_output(src: Path) -> Path:
    """
    Copy `src` into WORD_DOCS_DIR, preserving filename; return new path.
    Overwrites if already present.
    """
    if not src.exists():
        raise FileNotFoundError(src)
    dest = WORD_DOCS_DIR / src.name
    shutil.copy2(src, dest)
    log.debug("Copied %s ➜ %s", src, dest)
    return dest


def ensure_parent_dirs(paths: Iterable[Path]) -> None:
    """Guarantee parent directories exist for each provided Path."""
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)
