#!/usr/bin/env python3
"""
scripts/build_sandwich_pdf.py — Assembles a 100% searchable 1:1 Sandwich PDF
of Otto von Böhtlingk's Pāṇini (Leipzig 1887).

Visible Layer: Original high-resolution facsimile scans from UB Heidelberg.
Invisible Layer: Full-text Mistral OCR + canonical Devanāgarī / IAST placed
accurately using PDF Text Rendering Mode 3 (Neither fill nor stroke text).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import List, Tuple

import fitz  # PyMuPDF


ADHYAYA_NAMES = {
    1: "Prathamo 'dhyāyaḥ",
    2: "Dvitīyo 'dhyāyaḥ",
    3: "Tṛtīyo 'dhyāyaḥ",
    4: "Caturtho 'dhyāyaḥ",
    5: "Pañcamo 'dhyāyaḥ",
    6: "Ṣaṣṭho 'dhyāyaḥ",
    7: "Saptamo 'dhyāyaḥ",
    8: "Aṣṭamo 'dhyāyaḥ",
}

PADA_NAMES = {
    1: "Prathamaḥ Pādaḥ",
    2: "Dvitīyaḥ Pādaḥ",
    3: "Tṛtīyaḥ Pādaḥ",
    4: "Caturthaḥ Pādaḥ",
}


def clean_markdown_text(text: str) -> str:
    """Strip markdown formatting artifacts while preserving philological content."""
    t = re.sub(r"^#{1,6}\s+", "", text.strip(), flags=re.MULTILINE)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    return t.strip()


def insert_invisible_text(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    fontfile: str,
    fontname: str,
) -> None:
    """Insert text in PDF render_mode=3 (invisible) fitting inside rect."""
    clean = clean_markdown_text(text)
    if not clean:
        return

    # Try decreasing font sizes until it fits
    max_fs = min(36.0, max(8.0, rect.height * 0.8))
    for fs in [max_fs, max_fs * 0.85, max_fs * 0.7, 12.0, 10.0, 8.0, 6.0, 4.0]:
        rc = page.insert_textbox(
            rect,
            clean,
            fontfile=fontfile,
            fontname=fontname,
            render_mode=3,
            fontsize=fs,
        )
        if rc >= 0:
            return

    # Fallback minimal size
    page.insert_textbox(
        rect,
        clean,
        fontfile=fontfile,
        fontname=fontname,
        render_mode=3,
        fontsize=4.0,
    )


def build_toc(master_json: Path) -> List[Tuple[int, str, int]]:
    """Build PDF Table of Contents (Bookmarks) from master dataset."""
    toc = [[1, "Śivasūtrāṇi (Akṣarasamāmnāyaḥ)", 1]]

    if master_json.is_file():
        data = json.loads(master_json.read_text(encoding="utf-8"))
        sutras = data.get("sutras", [])

        adhyaya_starts = {}
        pada_starts = {}

        for s in sutras:
            a = s["adhyaya"]
            p = s["pada"]
            if a not in adhyaya_starts:
                adhyaya_starts[a] = s["page"]
            if (a, p) not in pada_starts:
                pada_starts[(a, p)] = s["page"]

        for a in range(1, 9):
            a_page = adhyaya_starts.get(a, 2)
            sa_name = ADHYAYA_NAMES.get(a, f"Adhyāya {a}")
            toc.append([1, f"{a}. Adhyāya ({sa_name})", a_page])

            for p in range(1, 5):
                p_page = pada_starts.get((a, p), a_page)
                sa_pname = PADA_NAMES.get(p, f"Pāda {p}")
                toc.append([2, f"{p}. Pāda ({sa_pname})", p_page])

    toc.append([1, "Nachträge und Verbesserungen", 477])
    return toc


def assemble_sandwich(
    img_dir: Path,
    mistral_dir: Path,
    master_json: Path,
    output_pdf: Path,
    font_path: str = "/Library/Fonts/Arial Unicode.ttf",
) -> None:
    t0 = time.time()
    print("=" * 70)
    print("AlexandriaSandwich — Assembling 1:1 Sandwich PDF (Pages 1 to 478)")
    print("=" * 70)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()

    total_pages = 478
    total_blocks_inserted = 0

    for p in range(1, total_pages + 1):
        img_name = f"7_3A{p:09d}_jpg_full_max_0_default_jpg.jpg"
        json_name = f"7_3A{p:09d}_jpg_full_max_0_default_jpg.mistral.json"

        img_path = img_dir / img_name
        json_path = mistral_dir / json_name

        if not img_path.is_file() or not json_path.is_file():
            print(f"Error: Missing image or OCR JSON for page {p}", file=sys.stderr)
            sys.exit(1)

        j_data = json.loads(json_path.read_text(encoding="utf-8"))
        page_info = j_data["pages"][0]
        dims = page_info["dimensions"]
        w, h = dims["width"], dims["height"]

        # Create 1:1 page matching scan resolution exactly
        page = doc.new_page(width=w, height=h)

        # Layer 1: Visible Image (Lossless)
        page.insert_image(fitz.Rect(0, 0, w, h), filename=str(img_path))

        # Layer 2: Invisible OCR Text Layer
        blocks = page_info.get("blocks", [])
        for b in blocks:
            txt = b.get("content", "")
            # Filter Heidelberg digital collection stamp / watermarks
            if any(w_word in txt for w_word in ["UNIVERSITÄTS", "HEIDELBERG", "digi.ub", "Baden-Württemberg"]):
                continue

            rect = fitz.Rect(b["top_left_x"], b["top_left_y"], b["bottom_right_x"], b["bottom_right_y"])
            insert_invisible_text(page, rect, txt, font_path, "ArialUni")
            total_blocks_inserted += 1

        if p % 50 == 0 or p == total_pages:
            elapsed = time.time() - t0
            print(f"Processed page {p:3d}/{total_pages} ({total_blocks_inserted:5d} text blocks inserted, {elapsed:.1f}s)")

    # Bookmarks / Outline
    print("Adding Table of Contents / Bookmarks...")
    toc = build_toc(master_json)
    doc.set_toc(toc)

    # Document Metadata
    doc.set_metadata({
        "title": "Pâṇini's Grammatik (Leipzig 1887)",
        "author": "Otto von Böhtlingk",
        "subject": "Aṣṭādhyāyī Sūtrapāṭha mit deutscher Übersetzung und Erläuterungen (1:1 Sandwich-PDF)",
        "keywords": "Panini, Astadhyayi, Boethlingk, Sanskrit, Grammatik, Sandwich-PDF, OCR",
        "creator": "AlexandriaSandwich Digital Humanities Pipeline",
        "producer": "PyMuPDF / Mistral OCR",
    })

    print(f"Saving optimized PDF to {output_pdf} (deflate + garbage collection)...")
    doc.save(
        str(output_pdf),
        deflate=True,
        garbage=4,
        clean=True,
    )
    doc.close()

    total_time = time.time() - t0
    size_mb = output_pdf.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"Sandwich PDF successfully built: {output_pdf}")
    print(f"Total Pages: {total_pages} | File Size: {size_mb:.2f} MB | Build Time: {total_time:.1f}s")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build searchable 1:1 Sandwich PDF")
    parser.add_argument(
        "--img-dir",
        type=Path,
        default=Path("data/img_cache"),
        help="Directory with cached facsimile images",
    )
    parser.add_argument(
        "--mistral-dir",
        type=Path,
        default=Path("data/mistral"),
        help="Directory with Mistral OCR JSON files",
    )
    parser.add_argument(
        "--master-json",
        type=Path,
        default=Path("data/ashtadhyayi_complete_boethlingk1887.json"),
        help="Path to consolidated master JSON",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/boehtlingk1887_sandwich.pdf"),
        help="Path to output PDF",
    )
    parser.add_argument(
        "--font",
        type=str,
        default="/Library/Fonts/Arial Unicode.ttf",
        help="Path to Unicode TTF font supporting Devanagari and Latin diacritics",
    )
    args = parser.parse_args()

    assemble_sandwich(
        img_dir=args.img_dir,
        mistral_dir=args.mistral_dir,
        master_json=args.master_json,
        output_pdf=args.output,
        font_path=args.font,
    )


if __name__ == "__main__":
    main()
