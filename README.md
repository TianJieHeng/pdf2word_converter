# PDF ➜ Word Converter

Tkinter desktop application that converts PDFs to `.docx` files using a **two‑pass** strategy:

1. **Direct text extraction** via [PyMuPDF](https://pymupdf.readthedocs.io/).
2. **OCR fallback** with [Tesseract](https://github.com/tesseract-ocr/tesseract) (through `pytesseract`) for pages that contain little or no extractable text.

Outputs are saved next to the script/executable inside a `word_docs/` folder.  
Encrypted PDFs can be unlocked by providing a username and/or password.

## Features

- GUI built with Tkinter (no web dependencies).
- Handles password‑protected PDFs.
- Two‑pass extraction (text → OCR).
- Progress log within the UI + rotating log file `pdf2word.log`.
- Creates a Word document sharing the original PDF filename.
- Works both from source (`python main.py`) and as a packaged `.exe` (PyInstaller).

## Prerequisites

### 1. Python
Python **3.10+** recommended.

### 2. Tesseract OCR Engine
Install the native Tesseract binary (the Python package is only a wrapper):

- **Windows:** Download installer from <https://github.com/tesseract-ocr/tesseract>.  
  After installing, ensure the `tesseract.exe` directory is on your `PATH` (e.g. `C:\Program Files\Tesseract-OCR`).
- **macOS (Homebrew):**
  ```bash
  brew install tesseract

  
## Installation

Clone and install dependencies:

git clone <your-repo-url> pdf2word_converter
cd pdf2word_converter
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt


## Running the App

From the project root:

```bash
python -m src.main
