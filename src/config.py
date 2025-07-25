
from __future__ import annotations

import os
import sys
from pathlib import Path


def _detect_base_dir() -> Path:
    """
    • If running from a frozen executable (PyInstaller) the code is unpacked
      in a temp dir, but the executable itself lives where the user launched it.
      We want that directory.
    • Otherwise use the repo root (folder containing this file).
    """
    if getattr(sys, "frozen", False):  # PyInstaller sets this
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


BASE_DIR: Path = _detect_base_dir()
WORD_DOCS_DIR: Path = BASE_DIR / "word_docs"
LOG_FILE: Path = BASE_DIR / "pdf2word.log"

# make sure the output directory exists right‑away
WORD_DOCS_DIR.mkdir(exist_ok=True)
