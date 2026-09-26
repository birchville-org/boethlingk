#!/usr/bin/env python3
"""
scripts/batch_ocr_runner.py — Automated batch OCR runner for Boethlingk pages.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PRICE_PER_PAGE = 0.004

def run_batch(start_page: int, end_page: int, out_dir: Path = Path("data/mistral")) -> None:
    pages_to_run = []
    for p in range(start_page, end_page + 1):
        md_file = out_dir / f"7_3A000000{p:03d}_jpg_full_max_0_default_jpg.mistral.md"
        img_file = Path(f"data/img_cache/7_3A000000{p:03d}_jpg_full_max_0_default_jpg.jpg")
        if not img_file.exists():
            print(f"Warning: Image file not found: {img_file}", file=sys.stderr)
            continue
        if md_file.exists():
            print(f"Page {p} already processed, skipping.", file=sys.stderr)
            continue
        pages_to_run.append(str(img_file))

    if not pages_to_run:
        print(f"No pages to process for range {start_page}-{end_page}.")
        return

    cost = len(pages_to_run) * PRICE_PER_PAGE
    print(f"Starting OCR on {len(pages_to_run)} pages ({start_page}-{end_page}). Estimated cost: {cost:.4f} $")

    cmd = [
        "uv", "run", "--with", "mistralai", "python3", "scripts/mistral_ocr.py",
        "--out-dir", str(out_dir),
        "--json",
    ] + pages_to_run

    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"Error running OCR batch (exit {res.returncode})", file=sys.stderr)
        sys.exit(res.returncode)

    print(f"Batch {start_page}-{end_page} completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch OCR runner")
    parser.add_argument("start_page", type=int, help="Start page number (inclusive)")
    parser.add_argument("end_page", type=int, help="End page number (inclusive)")
    parser.add_argument("--out-dir", type=Path, default=Path("data/mistral"))
    args = parser.parse_args()

    run_batch(args.start_page, args.end_page, args.out_dir)
