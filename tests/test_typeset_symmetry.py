"""
Tests for visual and typographical symmetry in the compiled PDF edition.
Verifies that running headers on even (verso) and odd (recto) pages maintain
uniform font family (STIXTwoText), upright style, consistent colors, and mirror placement,
and audits Pāṇini outer-margin sūtra references.
"""

import json
import os
import re
from pathlib import Path
import pytest
import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "data" / "output" / "boethlingk1887_facsimile_dense.pdf"
STRUCT_PATH = REPO_ROOT / "data" / "edition_structure.json"
MARGIN_REF_RE = re.compile(r"^\d+, \d+, \d+\.$")


@pytest.fixture(scope="module")
def structure():
    with open(STRUCT_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def pdf_document():
    if not PDF_PATH.exists():
        msg = f"PDF not found at {PDF_PATH}. Run build_facsimile_dense_edition.py first."
        if os.environ.get("BOETHLINGK_REQUIRE_PDF") == "1":
            pytest.fail(msg)
        pytest.skip(msg)
    doc = pymupdf.open(str(PDF_PATH))
    yield doc
    doc.close()


def test_header_symmetry_and_style(pdf_document, structure):
    """
    Ensure running headers across original pages 2..479 (PDF pages 7..484) use
    STIXTwoText, upright posture (no italic flag), approved header colors,
    and consistent verso/recto horizontal mirroring.
    """
    fm = structure["front_matter_pages"]
    total = len(pdf_document)
    violations = []

    for pno in range(fm + 1, total):
        orig_p = pno - fm + 1
        pdf_page_num = pno + 1
        page = pdf_document[pno]
        blocks = page.get_text("dict").get("blocks", [])
        if not blocks:
            violations.append((pdf_page_num, "Empty page"))
            continue

        header_spans = [
            s
            for b in blocks
            for l in b.get("lines", [])
            for s in l.get("spans", [])
            if s["bbox"][1] < 45.0 and s.get("text", "").strip()
        ]
        if len(header_spans) < 3:
            violations.append((pdf_page_num, f"Expected >= 3 header spans, found {len(header_spans)}"))
            continue

        for s in header_spans:
            text = s["text"].strip()
            font = s.get("font", "")
            flags = s.get("flags", 0)
            color = s.get("color", -1)

            if not font.startswith("STIXTwoText"):
                violations.append((pdf_page_num, "Unexpected header font", font, text))
            if flags & 2:
                violations.append((pdf_page_num, "Italic header span detected", font, text))
            if color not in (0x0, 0x03192E):
                violations.append((pdf_page_num, f"Unexpected header color {hex(color)}", text))

        # Check horizontal mirror symmetry between even (verso) and odd (recto) pages
        header_spans.sort(key=lambda sp: sp["bbox"][0])
        left_x = header_spans[0]["bbox"][0]
        left_text = header_spans[0]["text"].strip()
        right_x = header_spans[-1]["bbox"][0]
        right_text = header_spans[-1]["text"].strip()

        if orig_p % 2 == 0:
            if not (left_text.isdigit() and left_x < 100.0 and right_x > 380.0):
                violations.append((pdf_page_num, f"Verso mirror mismatch (orig {orig_p})", left_text, right_text))
        else:
            if not (right_text.isdigit() and left_x < 120.0 and right_x > 380.0):
                violations.append((pdf_page_num, f"Recto mirror mismatch (orig {orig_p})", left_text, right_text))

    assert not violations, f"Detected running header style/symmetry violations: {violations[:10]}"


def test_panini_marginalia_format(pdf_document, structure):
    """
    Verify outer-margin Pāṇini sūtra references on Sūtrapāṭha pages (orig S. 2..476)
    are present, set in STIXTwoText, upright, and ink-colored (#03192e).
    """
    fm = structure["front_matter_pages"]
    text_end_idx = fm + structure["text_pages_count"]
    violations = []

    for pno in range(fm + 1, text_end_idx):
        pdf_page_num = pno + 1
        margin_spans = [
            s
            for b in pdf_document[pno].get_text("dict").get("blocks", [])
            for l in b.get("lines", [])
            for s in l.get("spans", [])
            if s["bbox"][1] >= 45.0
            and s["bbox"][0] > 405.0
            and MARGIN_REF_RE.match(s.get("text", ""))
        ]
        if not margin_spans:
            violations.append((pdf_page_num, "No outer-margin sūtra reference found"))
            continue

        for s in margin_spans:
            if not s.get("font", "").startswith("STIXTwoText"):
                violations.append((pdf_page_num, "Wrong margin font", s.get("font"), s["text"]))
            if s.get("flags", 0) & 2:
                violations.append((pdf_page_num, "Italic margin ref", s["text"]))
            if s.get("color", -1) != 0x03192E:
                violations.append((pdf_page_num, f"Wrong margin color {hex(s.get('color', 0))}", s["text"]))

    assert not violations, f"Detected Pāṇini marginalia violations: {violations[:10]}"
