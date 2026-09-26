#!/usr/bin/env python3
"""
scripts/download_scans.py — Download high-resolution IIIF facsimile scans
from Universitätsbibliothek Heidelberg for Otto von Böhtlingk's Pāṇini (1887).

Canonical IIIF Manifest:
https://digi.ub.uni-heidelberg.de/diglit/boehtlingk1887
"""
from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

TOTAL_PAGES = 478
IIIF_URL_TEMPLATE = "https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3A{page:09d}.jpg/full/max/0/default.jpg"
FILENAME_TEMPLATE = "7_3A{page:09d}_jpg_full_max_0_default_jpg.jpg"
USER_AGENT = "boethlingk-digitization/1.0 (+https://github.com/birchville-org/boethlingk)"


def download_page(page: int, out_dir: Path, force: bool = False, max_retries: int = 3) -> tuple[int, bool, str]:
    """Download a single page scan. Returns (page, success, message)."""
    target_file = out_dir / FILENAME_TEMPLATE.format(page=page)
    if target_file.exists() and not force and target_file.stat().st_size > 1000:
        return (page, True, "cached")

    url = IIIF_URL_TEMPLATE.format(page=page)
    req = Request(url, headers={"User-Agent": USER_AGENT})

    for attempt in range(1, max_retries + 1):
        try:
            with urlopen(req, timeout=30) as resp:
                if resp.status != 200:
                    raise HTTPError(url, resp.status, f"HTTP status {resp.status}", resp.headers, None)
                data = resp.read()
                target_file.write_bytes(data)
                return (page, True, f"downloaded ({len(data) / 1024:.1f} KB)")
        except (HTTPError, URLError, TimeoutError) as e:
            if attempt < max_retries:
                time.sleep(1.5 * attempt)
            else:
                return (page, False, f"failed after {max_retries} attempts: {e}")

    return (page, False, "unknown error")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download IIIF facsimile scans from UB Heidelberg (Bibliotheca Palatina)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start page number (1-based, default: 1)",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=TOTAL_PAGES,
        help=f"End page number (inclusive, default: {TOTAL_PAGES})",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/img_cache"),
        help="Output directory for scanned images (default: data/img_cache)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Number of concurrent download threads (default: 4)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download images even if already present locally",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    pages = list(range(args.start, args.end + 1))
    total = len(pages)

    print("=" * 70)
    print(f"Downloading {total} facsimile scans from UB Heidelberg")
    print(f"Page range: {args.start} to {args.end}")
    print(f"Target directory: {args.out_dir}")
    print(f"Concurrency: {args.concurrency}")
    print("=" * 70)

    success_count = 0
    cached_count = 0
    error_count = 0

    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        future_map = {
            executor.submit(download_page, p, args.out_dir, args.force): p
            for p in pages
        }

        for i, future in enumerate(as_completed(future_map), start=1):
            page, ok, msg = future.result()
            if ok:
                if msg == "cached":
                    cached_count += 1
                else:
                    success_count += 1
            else:
                error_count += 1
                print(f"[ERROR] Page {page:3d}: {msg}", file=sys.stderr)

            if i % 25 == 0 or i == total:
                print(f"Progress: {i}/{total} pages checked/downloaded (new: {success_count}, cached: {cached_count}, errors: {error_count})")

    print("=" * 70)
    print(f"Download complete: {success_count} downloaded, {cached_count} already cached, {error_count} errors.")
    print("=" * 70)

    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
