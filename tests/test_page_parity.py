"""
Tests for 1:1 facsimile page parity.
Verifies 484 PDF pages: 5 front matter pages (i–v), 476 text pages in strict 1:1 parity
with Böhtlingk 1887 (S. 1–476), and 3 corrigenda pages (S. 477–479).
"""

import json
import os
from pathlib import Path
import pytest
import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "data" / "output" / "boethlingk1887_facsimile_dense.pdf"
STRUCT_PATH = REPO_ROOT / "data" / "edition_structure.json"
DENSE_JSON_PATH = REPO_ROOT / "data" / "ashtadhyayi_facsimile_dense.json"


@pytest.fixture(scope="module")
def structure():
    assert STRUCT_PATH.exists(), f"Structure file not found at {STRUCT_PATH}"
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


def _body_text(page: pymupdf.Page) -> str:
    """Return text lines located below the top running header (y >= 45pt)."""
    parts = []
    for b in page.get_text("dict").get("blocks", []):
        for line in b.get("lines", []):
            for span in line.get("spans", []):
                if span["bbox"][1] >= 45.0:
                    parts.append(span.get("text", ""))
    return " ".join(parts)


def test_exact_page_count(pdf_document, structure):
    """
    Ensure PDF page total matches structure:
    5 Front Matter (i–v) + 476 Text pages (1–476) + 3 Corrigenda pages (477–479) = 484.
    """
    expected = structure["total_facsimile_pdf_pages"]
    total = len(pdf_document)
    assert total == expected, f"Expected {expected} pages in facsimile edition, got {total}"


def test_page_labels_alignment(pdf_document, structure):
    """
    Ensure PDF native page label ranges match historical numbering:
    - Front matter (PDF pages 1..5) uses lowercase Roman numerals ('r')
    - Main text (PDF page 6 onwards) uses Arabic decimals ('D') starting with 1
    """
    ranges = pdf_document.get_page_labels()
    assert len(ranges) >= 2, f"Expected at least 2 page label ranges, got {len(ranges)}"
    assert ranges[0]["startpage"] == 0 and ranges[0]["style"] == "r"
    assert ranges[1]["startpage"] == structure["front_matter_pages"]
    assert ranges[1]["style"] == "D" and ranges[1]["firstpagenum"] == 1


def test_original_content_boundaries(pdf_document, structure):
    """
    Ensure exact body placement of Śiva-Sūtras (S. 1), concluding Sūtra 8.4.68 (S. 476),
    and Corrigenda section (S. 477–479) excluding running header matches.
    """
    fm = structure["front_matter_pages"]

    p1_body = _body_text(pdf_document[fm])
    assert "Śiva-Sūtras (Akṣarasamāmnāya)" in p1_body and "(Śiva-Sūtra 14 — ha l)" in p1_body, "PDF p.6 missing Śiva-Sūtras body"

    p476_idx = fm + structure["text_pages_count"] - 1
    p476_page = pdf_document[p476_idx]
    p476_body = _body_text(p476_page)
    assert "अ अ" in p476_body and "॥ इति " in p476_body and "(a a)" in p476_body and "Das in der Grammatik als offen behandelte" in p476_body, "PDF p.481 missing concluding sūtra/colophon"

    margin_refs = {
        s["text"].strip()
        for b in p476_page.get_text("dict").get("blocks", [])
        for l in b.get("lines", [])
        for s in l.get("spans", [])
        if s["bbox"][1] >= 45.0 and s["bbox"][0] > 350.0
    }
    assert "8, 4, 68." in margin_refs, "Right-margin ref '8, 4, 68.' missing on original p.476"

    corr_start_idx = fm + structure["text_pages_count"]
    corr_body = _body_text(pdf_document[corr_start_idx])
    assert "Nachträge und Verbesserungen (Corrigenda)" in corr_body, "Corrigenda heading missing on PDF p.482"


def test_all_sutras_on_assigned_pages(pdf_document, structure):
    """Verify every sutra ref (S. 2–476) appears in the right margin of its assigned PDF page."""
    if not DENSE_JSON_PATH.exists():
        pytest.skip(f"{DENSE_JSON_PATH} not generated yet")

    with open(DENSE_JSON_PATH, encoding="utf-8") as f:
        pages_data = json.load(f)

    fm = structure["front_matter_pages"]
    overflows = []
    for p_info in pages_data:
        orig_p = p_info["page_num"]
        pdf_idx = fm + (orig_p - 1)
        margin_refs = {
            s["text"].strip()
            for b in pdf_document[pdf_idx].get_text("dict").get("blocks", [])
            for l in b.get("lines", [])
            for s in l.get("spans", [])
            if s["bbox"][1] >= 45.0 and s["bbox"][0] > 350.0
        }
        for s in p_info["sutras"]:
            ref_str = f"{s['adhyaya']}, {s['pada']}, {s['sutra_num']}."
            if ref_str not in margin_refs:
                overflows.append((orig_p, ref_str))

    assert not overflows, f"Page parity overflows detected: {overflows[:10]}"
