
from __future__ import annotations

import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from src.core.converter import convert_pdf_to_docx
from src.config import WORD_DOCS_DIR
from src.utils.logger import get_logger

log = get_logger(__name__)


class Pdf2WordApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PDF ➜ Word Converter")
        self.geometry("650x450")
        self.resizable(False, False)

        self._build_widgets()
        self._conversion_thread: threading.Thread | None = None

    def _build_widgets(self) -> None:
        pad = {"padx": 8, "pady": 4}

        tk.Label(self, text="PDF Path:").grid(row=0, column=0, sticky="e", **pad)
        self.pdf_path_var = tk.StringVar()
        tk.Entry(self, textvariable=self.pdf_path_var, width=55).grid(row=0, column=1, **pad)
        tk.Button(self, text="Browse…", command=self._browse).grid(row=0, column=2, **pad)

        tk.Label(self, text="Username:").grid(row=1, column=0, sticky="e", **pad)
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var, width=25).grid(row=1, column=1, sticky="w", **pad)

        tk.Label(self, text="Password:").grid(row=2, column=0, sticky="e", **pad)
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var, show="*", width=25).grid(row=2, column=1, sticky="w", **pad)

        tk.Label(self, text="OCR Language:").grid(row=3, column=0, sticky="e", **pad)
        self.lang_var = tk.StringVar(value="eng")
        tk.Entry(self, textvariable=self.lang_var, width=12).grid(row=3, column=1, sticky="w", **pad)
        tk.Label(self, text="(e.g. 'eng', 'eng+spa')").grid(row=3, column=1, sticky="e", **pad)

        self.convert_btn = tk.Button(self, text="Convert", command=self.start_conversion)
        self.convert_btn.grid(row=4, column=1, sticky="w", **pad)

        self.status_var = tk.StringVar(value="Idle")
        tk.Label(self, textvariable=self.status_var, fg="blue").grid(row=4, column=1, sticky="e", **pad)

        tk.Label(self, text="Progress Log:").grid(row=5, column=0, sticky="ne", **pad)
        self.log_text = ScrolledText(self, height=15, width=80, state="disabled")
        self.log_text.grid(row=5, column=1, columnspan=2, sticky="nsew", **pad)

    def _browse(self) -> None:
        path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if path:
            self.pdf_path_var.set(path)

    def _append_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _progress_callback(self, msg: str) -> None:
        self.after(0, lambda: self._append_log(msg))

    def start_conversion(self) -> None:
        if self._conversion_thread and self._conversion_thread.is_alive():
            messagebox.showinfo("Busy", "A conversion is already in progress.")
            return

        pdf_path = self.pdf_path_var.get().strip()
        if not pdf_path:
            messagebox.showwarning("Missing", "Please provide a PDF path.")
            return

        if not pdf_path.lower().endswith(".pdf"):
            messagebox.showwarning("Invalid", "Selected file must be a .pdf")
            return

        self.status_var.set("Working…")
        self.convert_btn.config(state="disabled")
        self._append_log(f"Starting conversion: {pdf_path}")

        args = dict(
            pdf_path=pdf_path,
            username=self.username_var.get() or None,
            password=self.password_var.get() or None,
            progress_cb=self._progress_callback,
            ocr_lang=self.lang_var.get() or None,
        )
        self._conversion_thread = threading.Thread(target=self._run_conversion, kwargs=args, daemon=True)
        self._conversion_thread.start()

    def _run_conversion(self, **kwargs) -> None:
        try:
            output_path = convert_pdf_to_docx(**kwargs)
        except Exception as exc:
            log.exception("Conversion failed.")
            self.after(0, lambda e=exc: self._on_conversion_failed(e))
        else:
            self.after(0, lambda p=output_path: self._on_conversion_success(p))

    def _on_conversion_success(self, output_path: Path) -> None:
        self._append_log(f"Completed: {output_path}")
        self.status_var.set("Done")
        self.convert_btn.config(state="normal")
        messagebox.showinfo(
            "Success",
            f"Conversion complete!\nSaved as:\n{output_path}\n\nFolder:\n{WORD_DOCS_DIR}"
        )

    def _on_conversion_failed(self, exc: Exception) -> None:
        self._append_log(f"ERROR: {exc}")
        self.status_var.set("Error")
        self.convert_btn.config(state="normal")
        messagebox.showerror("Conversion failed", str(exc))


def launch() -> None:
    app = Pdf2WordApp()
    app.mainloop()
