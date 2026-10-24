#!/usr/bin/env python3
"""
scripts/build_page_aligned_edition.py — Compiles the page-aligned test edition
of Otto von Böhtlingk's Pāṇini (1887), where every page starts at the exact
same Sūtra as the 1887 Leipzig original edition.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

from build_typeset_edition import prepare_data, post_process_pdf


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile page-aligned test PDF of Boethlingk 1887")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/boethlingk1887_page_aligned_test.pdf"),
        help="Target PDF path",
    )
    args = parser.parse_args()

    t0 = time.time()
    print("=" * 70)
    print("Kompiliere seitengetreue Testausgabe (Original-Seitenstarts)...")
    print("=" * 70)

    prepare_data()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    typst_cmd = [
        "typst", "compile",
        "--root", ".",
        "--font-path", "data/fonts",
        "scripts/boethlingk1887_page_aligned.typ",
        str(args.output),
    ]

    res = subprocess.run(typst_cmd)
    if res.returncode != 0:
        print("Fehler beim Typst-Kompilieren!", file=sys.stderr)
        sys.exit(res.returncode)

    post_process_pdf(args.output)

    # Sync to User Indologie Panini folder if present
    indologie_dest = Path("/Users/marco/Documents/00_Indologie/Panini")
    if indologie_dest.exists():
        dest_file = indologie_dest / "BOETHLINGK 1887 Panini Grammatik (Seitengetreue Testausgabe).pdf"
        shutil.copy2(args.output, dest_file)
        print(f"✓ Synchronisiert nach Indologie-Arbeitsordner: {dest_file}")

    elapsed = time.time() - t0
    size_mb = args.output.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"Erfolg: {args.output} erstellt!")
    print(f"Dateigröße: {size_mb:.2f} MB | Zeit: {elapsed:.2f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
