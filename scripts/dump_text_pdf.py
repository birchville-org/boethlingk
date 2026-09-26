#!/usr/bin/env python3
"""
scripts/dump_text_pdf.py — Extract raw layout text from Sandwich PDF and format as plain text PDF.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
import fitz  # PyMuPDF


def dump_text_pdf(
    input_pdf: Path,
    output_pdf: Path,
    start_page: int = 2,
    end_page: int = 3,
) -> None:
    doc = fitz.open()

    for p in range(start_page, end_page + 1):
        txt = subprocess.check_output(
            ["pdftotext", "-f", str(p), "-l", str(p), "-layout", str(input_pdf), "-"]
        ).decode("utf-8")

        lines = [
            line for line in txt.splitlines()
            if not any(w in line for w in ["UNIVERSITÄTS", "HEIDELBERG", "Baden-Württemberg", "gefördert durch"])
        ]
        cleaned = "\n".join(lines).strip()

        page = doc.new_page(width=595, height=842)  # A4
        rect = fitz.Rect(40, 40, 555, 802)
        page.insert_textbox(
            rect,
            cleaned,
            fontname="Helvetica",
            fontfile="/Library/Fonts/Arial Unicode.ttf",
            fontsize=8.5,
            render_mode=0,
        )

    if hasattr(doc, "subset_fonts"):
        doc.subset_fonts()

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_pdf), garbage=4, deflate=True)
    doc.close()
    print(f"Erfolg: {output_pdf} erstellt ({output_pdf.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate raw text dump PDF from Sandwich PDF")
    parser.add_argument("--input", type=Path, default=Path("data/output/boehtlingk1887_sandwich.pdf"))
    parser.add_argument("--output", type=Path, default=Path("data/output/vergleich_methode_2_textdump.pdf"))
    parser.add_argument("--start", type=int, default=2)
    parser.add_argument("--end", type=int, default=3)
    args = parser.parse_args()

    dump_text_pdf(args.input, args.output, args.start, args.end)
