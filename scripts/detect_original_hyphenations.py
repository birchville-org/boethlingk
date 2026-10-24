#!/usr/bin/env python3
"""
scripts/detect_original_hyphenations.py

Inspects original Böhtlingk (1887) page scans via Tesseract OCR to accurately
detect all hyphenation and line-break points in multi-line Sūtra headings.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf


def main() -> None:
    with open("data/ashtadhyayi_complete_boethlingk1887.json", encoding="utf-8") as f:
        master = json.load(f)

    sutra_map = {s["ref"]: s for s in master["sutras"]}

    # Candidates: max_word >= 28 or len >= 50
    candidates = []
    for s in master["sutras"]:
        deva = s.get("canonical_devanagari", "")
        words = deva.split()
        max_w = max((len(w) for w in words), default=0)
        if max_w >= 28 or len(deva) >= 50:
            candidates.append(s["ref"])

    print(f"Total candidate sutras to inspect: {len(candidates)}")

    results = {}
    for r in candidates:
        s = sutra_map[r]
        p = s["page"]
        snum = s["sutra_num"]
        deva = s["canonical_devanagari"]

        m_json_path = Path(f"data/mistral/7_3A000000{p:03d}_jpg_full_max_0_default_jpg.mistral.json")
        img_path = Path(f"data/img_cache/7_3A000000{p:03d}_jpg_full_max_0_default_jpg.jpg")
        if not m_json_path.exists() or not img_path.exists():
            continue

        with open(m_json_path, encoding="utf-8") as f:
            m_data = json.load(f)

        page_m = m_data["pages"][0]
        mw = page_m["dimensions"]["width"]
        mh = page_m["dimensions"]["height"]

        doc = pymupdf.open(str(img_path))
        page_img = doc[0]
        iw = page_img.rect.width
        ih = page_img.rect.height
        sx, sy = iw / mw, ih / mh

        found_block = None
        for b in page_m.get("blocks", []):
            c = b.get("content", "")
            if f"॥ {snum} ॥" in c or f"॥ {snum}॥" in c or f"|| {snum} ||" in c or f" {snum} ॥" in c or f" {snum}॥" in c:
                found_block = b
                break
            elif b.get("type") in ("title", "text") and any(w in c for w in deva.split()[:2] if len(w) > 6):
                found_block = b
                break

        if found_block:
            x0 = max(0, found_block["top_left_x"] * sx - 15)
            y0 = max(0, found_block["top_left_y"] * sy - 15)
            x1 = min(iw, found_block["bottom_right_x"] * sx + 15)
            y1 = min(ih, found_block["bottom_right_y"] * sy + 15)

            pix = page_img.get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=200)
            tmp_png = Path(f"tmp_crop_{r}.png")
            pix.save(str(tmp_png))

            cmd = ["tesseract", str(tmp_png), "stdout", "-l", "san", "--psm", "6"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]

            # filter out commentary lines if any (lines with latin text)
            deva_lines = [l for l in lines if not re.search(r"[a-zA-Z]{3,}", l)]

            if len(deva_lines) > 1 or any("-" in l for l in deva_lines):
                results[r] = {
                    "ref": r,
                    "page": p,
                    "canonical": deva,
                    "ocr_lines": deva_lines,
                }
            tmp_png.unlink(missing_ok=True)
        doc.close()

    out_file = Path("data/original_multiline_sutras.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n--- Extracted {len(results)} Multiline / Hyphenated Sutras ---")
    for r, d in results.items():
        print(f"\n[{r}] (S. {d['page']}): {d['canonical'][:40]}...")
        for l in d["ocr_lines"]:
            print(f"    {l}")


if __name__ == "__main__":
    main()
