#!/usr/bin/env python3
"""
scripts/extract_text_pdf.py — Extract pure vector text PDF from a Sandwich PDF
by stripping image scans and switching rendering mode 3 Tr (invisible) to 0 Tr (visible).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
import fitz  # PyMuPDF


def extract_stripped_pdf(
    input_pdf: Path,
    output_pdf: Path,
    start_page: int = 1,
    end_page: int | None = None,
) -> None:
    doc = fitz.open(input_pdf)
    total_doc_pages = len(doc)
    end = end_page or total_doc_pages

    # 0-basierte Indizes
    page_indices = list(range(start_page - 1, end))
    print(f"Lese {len(page_indices)} Seiten aus {input_pdf} (Seiten {start_page} bis {end})...")

    doc.select(page_indices)

    for i, page in enumerate(doc, start=start_page):
        # 1. Content Stream säubern
        for xref in page.get_contents():
            stream = doc.xref_stream(xref)
            # Bildaufrufe entfernen
            stream = re.sub(rb"/fzImg\d+\s+Do\s*", b"", stream)
            stream = re.sub(rb"/Im\d+\s+Do\s*", b"", stream)
            # Rendering Mode 3 (unsichtbar) auf 0 (sichtbar gefüllt) umschalten
            stream = stream.replace(b"3 Tr", b"0 Tr")
            doc.update_stream(xref, stream)

        # 2. XObject-Referenzen aus dem Seiten-Wörterbuch entfernen
        page.clean_contents()
        for img in page.get_images():
            try:
                page.delete_image(img[0])
            except Exception:
                pass

    if hasattr(doc, "subset_fonts"):
        doc.subset_fonts()

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(
        str(output_pdf),
        deflate=True,
        garbage=4,
        clean=True,
    )
    doc.close()

    size_kb = output_pdf.stat().st_size / 1024
    print(f"Erfolg: {output_pdf} erstellt ({size_kb:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract visible vector text PDF from Sandwich PDF")
    parser.add_argument("--input", type=Path, default=Path("data/output/boehtlingk1887_sandwich.pdf"))
    parser.add_argument("--output", type=Path, default=Path("data/output/vergleich_methode_1_stripping.pdf"))
    parser.add_argument("--start", type=int, default=2, help="Start page (1-based, default: 2)")
    parser.add_argument("--end", type=int, default=3, help="End page (1-based, default: 3)")
    args = parser.parse_args()

    extract_stripped_pdf(args.input, args.output, args.start, args.end)
