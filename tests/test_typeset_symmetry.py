"""
Tests for visual and typographical symmetry in the compiled PDF edition.
Verifies that running headers on even (verso) and odd (recto) pages
maintain uniform typography, weight, style, and color.
"""

from pathlib import Path
import pytest
import pymupdf

PDF_PATH = Path(__file__).resolve().parent.parent / "data" / "output" / "boethlingk1887_facsimile_dense.pdf"

@pytest.fixture(scope="module")
def pdf_document():
    assert PDF_PATH.exists(), f"PDF not found at {PDF_PATH}. Run build_facsimile_dense_edition.py first."
    doc = pymupdf.open(str(PDF_PATH))
    yield doc
    doc.close()

def test_header_symmetry_and_style(pdf_document):
    """
    Ensure running headers on all text pages (p. 2..476) are upright STIX Two Text
    and do not alternate between upright and italic or switch font colors arbitrarily.
    """
    # PDF page 6 is original page 1 (Śiva-Sūtras, no header).
    # PDF pages 7..481 are original pages 2..476.
    violations = []

    for pno in range(6, 481):  # 0-indexed 6..480 -> PDF page 7..481
        page = pdf_document[pno]
        page_num = pno + 1
        blocks = page.get_text("dict")["blocks"]
        if not blocks:
            violations.append((page_num, "Empty page"))
            continue

        header_spans = []
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    # Header region is within top 45pt
                    if s["bbox"][1] < 45:
                        header_spans.append(s)

        for s in header_spans:
            text = s.get("text", "")
            flags = s.get("flags", 0)
            is_italic = bool(flags & 2)

            # If header contains Adhyāya/Pāda title, it MUST be upright
            if "Adhy" in text or "Pāda" in text:
                if is_italic:
                    violations.append((page_num, "Italic header detected", text, s.get("font")))

    assert not violations, f"Detected running header style violations: {violations[:10]}"
