
from __future__ import annotations

from io import BytesIO
from typing import Optional

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

from src.utils.logger import get_logger

log = get_logger(__name__)


def ocr_page(page: fitz.Page, dpi: int = 300, lang: Optional[str] = None) -> str:
    """
    OCR a single page object.

    Args:
        page: fitz.Page instance.
        dpi: rendering resolution; higher improves OCR but costs CPU.
        lang: optional Tesseract language code (e.g. 'eng', 'eng+spa').

    Returns:
        Extracted text (stripped).
    """
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img = Image.open(BytesIO(pix.tobytes("png")))
    config = "--psm 3"  # fully automatic page segmentation
    text = pytesseract.image_to_string(img, lang=lang or "eng", config=config)
    cleaned = text.strip()
    log.debug("OCR page %s produced %d chars.", page.number, len(cleaned))
    return cleaned
