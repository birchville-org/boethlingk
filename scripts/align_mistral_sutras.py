#!/usr/bin/env python3
"""
scripts/align_mistral_sutras.py — Robust Alignment of Mistral OCR Markdown with canonical Ashtadhyayi Sutras.

Features:
- Handles # and ## heading markers as well as plain lines with Sūtra delimiters (॥...॥ or ||...||)
- Handles Devanagari, Telugu, Gujarati, and Arabic digits
- Handles open/closed ॥ delimiters (e.g. ॥ ४० ॥ or ४० ॥)
- Cleans rogue non-Sanskrit script tokens (Hebrew/Telugu) from commentary
- Uses sequential tracking and canonical Ground-Truth (data/sutras.json) to correct misrecognized headings
- Reliably handles Pada boundaries (e.g. colophon: इति प्रथमस्याध्यायस्य प्रथमः पादः)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional, Sequence


DIGIT_MAP = {
    # Devanagari
    "०": 0, "१": 1, "२": 2, "३": 3, "४": 4, "५": 5, "६": 6, "७": 7, "८": 8, "९": 9,
    # Telugu
    "౦": 0, "౧": 1, "౨": 2, "౩": 3, "౪": 4, "౫": 5, "౬": 6, "౭": 7, "౮": 8, "౯": 9,
    # Gujarati
    "૦": 0, "૧": 1, "૨": 2, "૩": 3, "૪": 4, "૫": 5, "૬": 6, "૭": 7, "૮": 8, "૯": 9,
}

PAT_SUTRA_DELIM = re.compile(r"(?:[॥|]{1,2}\s*[^॥|\n]{1,8}\s*[॥|]{1,2}|[\d/०-९౦-౯૦-૯]+\s*[॥|]{2})")
PAT_HEADER = re.compile(r"(?:^|\n)\s*(\d{1,2})\s*[,.]\s*(\d{1,2})\s*[,.]\s*(\d{1,3})[.,]?\s*(?:\n|$)")
PAT_INLINE_REF = re.compile(r"(?:^|\s)(\d{1,2})\s*,\s*(\d{1,2})\s*,\s*(\d{1,3})[.,]?\b")
PAT_ADHYAYA_END = re.compile(r"(?:[ऽअ]ध्याय[^\n॥]*समाप्त|इति\s+([^\n॥]+)\s*[ऽअ]ध्याय)", re.IGNORECASE)
PAT_COLOPHON = re.compile(r"(?:इति\s+([^\n॥]+)\s*पाद[ः:ौo\s]|पाठो[^\n॥]*समाप्त)", re.IGNORECASE)

# Stray scripts that occasionally drift in from small ligature noise
PAT_ROGUE_SCRIPTS = re.compile(r"[\u0590-\u05FF\u0C00-\u0C7F]+")

BOILERPLATE_PATTERNS = [
    re.compile(r"universit[äa]ts[-\s]*bibliothek\s+heidelberg", re.IGNORECASE),
    re.compile(r"digi\.ub\.uni-heidelberg\.de", re.IGNORECASE),
    re.compile(r"gef[öo]rdert\s+durch", re.IGNORECASE),
    re.compile(r"baden-w[üu]rttemberg", re.IGNORECASE),
    re.compile(r"p[āa][ṇn]ini['’]?s\s+grammatik\.?", re.IGNORECASE),
    re.compile(r"^\[LOGO\]", re.IGNORECASE),
]


def parse_multiscript_num(s: str) -> Optional[int]:
    s = s.strip()
    res = 0
    found = False
    for ch in s:
        if ch in DIGIT_MAP:
            res = res * 10 + DIGIT_MAP[ch]
            found = True
        elif ch.isdigit():
            res = res * 10 + int(ch)
            found = True
    return res if found else None


def extract_numbers_from_heading(heading: str) -> list[int]:
    """Find any sutra numbers delimited by ॥ or || or /."""
    nums = []
    m1 = re.findall(r"(?:[॥|]{1,2})\s*([०-९౦-౯૦-૯\d/]+)\s*(?=[॥|]{1,2}|$)", heading)
    for token in m1:
        if "/" in token:
            parts = token.split("/")
            if len(parts) == 2 and parts[0] == "6" and parts[1].isdigit():
                p2 = int(parts[1])
                nums.append(60 + (p2 - 4 if p2 >= 8 else p2))
                continue
        val = parse_multiscript_num(token)
        if val is not None:
            nums.append(val)

    if not nums:
        m2 = re.findall(r"([०-९౦-౯૦-૯\d]+)\s*[॥|]{1,2}", heading)
        for token in m2:
            val = parse_multiscript_num(token)
            if val is not None:
                nums.append(val)

    return nums


def is_boilerplate(line: str) -> bool:
    line_clean = line.strip()
    if not line_clean:
        return False
    return any(p.search(line_clean) for p in BOILERPLATE_PATTERNS)


def sanitize_text(text: str) -> str:
    """Clean rogue Hebrew/Telugu script tokens occasionally produced on damaged lead types."""
    # Replace repeated rogue characters with placeholder or remove
    cleaned = re.sub(r"[\u0590-\u05FF\u0C00-\u0C7F]{2,}", "[Sanskrit]", text)
    cleaned = re.sub(r"[\u0590-\u05FF\u0C00-\u0C7F]", "", cleaned)
    return cleaned


def is_colophon_line(line: str) -> bool:
    return bool(PAT_COLOPHON.search(line) or PAT_ADHYAYA_END.search(line) or "शब्दानुशासन" in line)


def clean_commentary_paragraphs(text: str) -> list[str]:
    paras = [p.strip() for p in text.split("\n\n")]
    cleaned = []
    for p in paras:
        if not p:
            continue
        lines = [sanitize_text(line.strip()) for line in p.splitlines() if line.strip() and not is_boilerplate(line) and not is_colophon_line(line)]
        if lines:
            cleaned.append("\n".join(lines))
    return cleaned


def extract_page_info(content: str) -> tuple[Optional[int], Optional[tuple[int, int, int]]]:
    """Extract book page number and running head (adhyaya, pada, sutra)."""
    header_ref = None
    m_head = PAT_HEADER.search(content[:300])
    if m_head:
        header_ref = (int(m_head.group(1)), int(m_head.group(2)), int(m_head.group(3)))

    page_num = None
    for line in content[:200].splitlines() + content[-300:].splitlines():
        line = line.strip()
        if line.isdigit() and 1 <= int(line) <= 878:
            page_num = int(line)
            break

    return page_num, header_ref


def split_into_sections(md_content: str) -> list[tuple[str, str]]:
    """Split content into (heading, body) pairs using #/## or standalone sutra lines."""
    lines = md_content.splitlines()
    sections = []
    curr_heading = ""
    curr_body_lines: list[str] = []

    def flush():
        nonlocal curr_heading, curr_body_lines
        if curr_heading or curr_body_lines:
            sections.append((curr_heading, "\n".join(curr_body_lines).strip()))
            curr_heading = ""
            curr_body_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if curr_body_lines:
                curr_body_lines.append("")
            continue

        # Check for colophon line
        if PAT_COLOPHON.search(stripped) or PAT_ADHYAYA_END.search(stripped):
            flush()
            curr_heading = stripped
            flush()
            continue

        is_heading = stripped.startswith("#") and len(stripped) > 1 and stripped.lstrip("#").startswith(" ")
        is_sutra_line = bool(PAT_SUTRA_DELIM.search(stripped)) and len(stripped) < 350

        # If current heading is hyphenated or incomplete, continue it
        if curr_heading and not curr_body_lines and (
            curr_heading.endswith("-")
            or ("॥" not in curr_heading and ("॥" in stripped or PAT_SUTRA_DELIM.search(stripped)))
        ):
            curr_heading = curr_heading.rstrip("-") + stripped
            continue

        if is_heading or is_sutra_line:
            flush()
            curr_heading = stripped
        else:
            curr_body_lines.append(stripped)

    flush()
    return sections


def is_canonical_match(heading: str, ref: str, sutras_db: dict[str, dict], threshold: float = 0.45) -> bool:
    canon = sutras_db.get(ref, {}).get("devanagari", "")
    if not canon:
        return False
    h_clean = "".join(c for c in heading if "\u0900" <= c <= "\u097F")
    c_clean = "".join(c for c in canon if "\u0900" <= c <= "\u097F")
    if not h_clean or not c_clean:
        return False
    if c_clean in h_clean or h_clean in c_clean:
        return True
    from difflib import SequenceMatcher
    return SequenceMatcher(None, h_clean, c_clean).ratio() >= threshold


def parse_markdown_sutras(
    md_content: str,
    source_file: str,
    sutras_db: dict[str, dict],
    state: dict[str, int],
    prev_entries: Optional[list[dict[str, Any]]] = None,
) -> list[dict[str, Any]]:
    page_num, header_ref = extract_page_info(md_content)

    # Detect if this page is the introductory Shiva Sutras page
    is_shiva_page = (page_num == 1) or ("शब्दानुशासनम्" in md_content and "प्रत्याहारसूत्राणि" in md_content)

    sections = split_into_sections(md_content)
    entries = []

    for heading, body in sections:
        # If section has no heading, it's text continuation from the previous page/sutra
        if not heading.strip():
            target_list = entries if entries else (prev_entries if prev_entries else [])
            if body.strip() and target_list and target_list[-1]["ref"] != "8.4.68":
                paras = clean_commentary_paragraphs(body)
                if paras:
                    continuation_text = "\n\n".join(paras)
                    if target_list[-1].get("commentary"):
                        target_list[-1]["commentary"] += "\n\n" + continuation_text
                    else:
                        target_list[-1]["commentary"] = continuation_text
            continue

        # Check for colophon ending an Adhyaya or Pada
        if PAT_ADHYAYA_END.search(heading):
            state["adhyaya"] += 1
            state["pada"] = 1
            state["last_sutra"] = 0
            continue
        elif PAT_COLOPHON.search(heading):
            state["pada"] += 1
            state["last_sutra"] = 0
            continue

        # Skip document titles
        if "शब्दानुशासनम्" in heading:
            continue

        nums = extract_numbers_from_heading(heading)

        # Fallback to sequential tracker if heading matches canon or body clearly contains translation
        if not nums:
            expected = state["last_sutra"] + 1
            expected_ref = f"{state['adhyaya']}.{state['pada']}.{expected}"
            if is_canonical_match(heading, expected_ref, sutras_db):
                nums = [expected]
            elif expected_ref in sutras_db and len(body) > 30 and (heading.startswith("#") or bool(PAT_SUTRA_DELIM.search(heading))):
                nums = [expected]

        if not nums:
            continue

        # Clean raw OCR Devanagari
        sutra_raw_deva = re.sub(r"[॥|].*[॥|]", "", heading).strip()
        sutra_raw_deva = re.sub(r"^#+\s*", "", sutra_raw_deva).strip()
        sutra_raw_deva = re.sub(r"^[†\s\d,.]+", "", sutra_raw_deva).strip()
        sutra_raw_deva = sutra_raw_deva.strip("()† \t")
        sutra_raw_deva = PAT_ROGUE_SCRIPTS.sub("", sutra_raw_deva).strip()

        paras = clean_commentary_paragraphs(body)
        translation = paras[0] if paras else ""
        commentary = "\n\n".join(paras[1:]) if len(paras) > 1 else ""

        for s_num in nums:
            if is_shiva_page:
                ref = f"shiva.{s_num}"
                entry = {
                    "ref": ref,
                    "adhyaya": 0,
                    "pada": 0,
                    "sutra_num": s_num,
                    "page": page_num,
                    "source_file": source_file,
                    "sutra_ocr": sutra_raw_deva,
                    "canonical_devanagari": "",
                    "canonical_iast": "",
                    "translation": translation,
                    "commentary": commentary,
                    "in_canonical_db": False,
                }
                entries.append(entry)
                continue

            expected = state["last_sutra"] + 1
            expected_ref = f"{state['adhyaya']}.{state['pada']}.{expected}"

            # Check for explicit inline reference in heading: e.g. "8, 1, 1."
            m_inline = PAT_INLINE_REF.search(heading)
            if m_inline:
                in_a, in_p, in_s = int(m_inline.group(1)), int(m_inline.group(2)), int(m_inline.group(3))
                if 1 <= in_a <= 8 and 1 <= in_p <= 4 and in_s in nums:
                    if in_a != state["adhyaya"] or in_p != state["pada"]:
                        state["adhyaya"] = in_a
                        state["pada"] = in_p
                        state["last_sutra"] = in_s - 1
                        expected = in_s
                        expected_ref = f"{state['adhyaya']}.{state['pada']}.{expected}"

            # Check for Pada restart: e.g. sutra 1 after sutra >= 35
            if s_num == 1 and state["last_sutra"] >= 35:
                if (header_ref and header_ref[0] > state["adhyaya"]) or state["pada"] >= 4:
                    state["adhyaya"] += 1
                    state["pada"] = 1
                else:
                    state["pada"] += 1
                state["last_sutra"] = 0
                expected = 1
                expected_ref = f"{state['adhyaya']}.{state['pada']}.{expected}"

            # 1. If heading matches expected canonical sutra text, prioritize expected
            if is_canonical_match(heading, expected_ref, sutras_db):
                s_num = expected
            # 2. If s_num goes backwards in an ongoing Pada, reconcile it
            elif s_num <= state["last_sutra"] and s_num != 1:
                if expected_ref in sutras_db:
                    s_num = expected
            # 3. If s_num jumped forward, verify whether candidate truly matches better than expected
            elif s_num != expected and expected_ref in sutras_db and s_num != 1:
                cand_ref = f"{state['adhyaya']}.{state['pada']}.{s_num}"
                if not is_canonical_match(heading, cand_ref, sutras_db, threshold=0.55):
                    s_num = expected

            ref = f"{state['adhyaya']}.{state['pada']}.{s_num}"
            canonical = sutras_db.get(ref, {})

            entry = {
                "ref": ref,
                "adhyaya": state["adhyaya"],
                "pada": state["pada"],
                "sutra_num": s_num,
                "page": page_num,
                "source_file": source_file,
                "sutra_ocr": sutra_raw_deva,
                "canonical_devanagari": canonical.get("devanagari", ""),
                "canonical_iast": canonical.get("iast", ""),
                "translation": translation,
                "commentary": commentary,
                "in_canonical_db": ref in sutras_db,
            }
            entries.append(entry)
            state["last_sutra"] = s_num

    return entries


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Align Mistral OCR Markdown with canonical Sutras")
    parser.add_argument("inputs", type=Path, nargs="+", help="Mistral Markdown file(s)")
    parser.add_argument(
        "--sutras-db",
        type=Path,
        default=Path("data/sutras.json"),
        help="Path to canonical sutras.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write aggregated aligned JSON to this path",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed alignment info",
    )
    args = parser.parse_args(argv)

    if not args.sutras_db.is_file():
        print(f"Error: Sutras DB not found at {args.sutras_db}", file=sys.stderr)
        return 2

    sutras_db = json.loads(args.sutras_db.read_text(encoding="utf-8"))
    print(f"Loaded {len(sutras_db)} canonical sutras from {args.sutras_db}", file=sys.stderr)

    sorted_inputs = sorted(args.inputs, key=lambda p: p.name)

    state = {
        "adhyaya": 1,
        "pada": 1,
        "last_sutra": 0,
    }

    all_entries = []
    for in_path in sorted_inputs:
        if in_path.is_file():
            content = in_path.read_text(encoding="utf-8")
            entries = parse_markdown_sutras(content, in_path.name, sutras_db, state, prev_entries=all_entries)
            all_entries.extend(entries)
            print(f"Parsed {len(entries):2d} sutras from {in_path.name} (state: {state['adhyaya']}.{state['pada']}.{state['last_sutra']})", file=sys.stderr)
            if args.verbose:
                for e in entries:
                    match_sym = "✓" if e["in_canonical_db"] else "✗"
                    print(f"  {match_sym} {e['ref']:<8s} | CANON: {e['canonical_devanagari']} | TR: {e['translation'][:45]}")

    print(f"\nTotal aligned sutras: {len(all_entries)}", file=sys.stderr)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(all_entries, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote output to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(json.dumps(all_entries, ensure_ascii=False, indent=2) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
