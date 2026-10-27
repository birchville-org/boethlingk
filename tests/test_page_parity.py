"""
Tests for 1:1 facsimile page parity.
Verifies that all 476 original text pages correspond to exactly 476 pages in the output PDF.
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

def test_exact_page_count(pdf_document):
    """
    Ensure the PDF has exactly 484 pages:
    - 5 Front Matter pages (i–v)
    - 476 Text pages (1–476)
    - 3 Corrigenda / End Matter pages (477–479)
    """
    total = len(pdf_document)
    assert total == 484, f"Expected exactly 484 pages in facsimile edition, got {total}"

def test_page_labels_alignment(pdf_document):
    """
    Ensure PDF native page label ranges match the historical structure:
    - Front matter (PDF pages 1..5) uses lowercase Roman numerals ('r')
    - Main text (PDF page 6 onwards) uses Arabic decimals ('D') starting with 1
    """
    ranges = pdf_document.get_page_labels()
    assert len(ranges) >= 2, f"Expected at least 2 page label ranges, got {len(ranges)}"
    assert ranges[0]["startpage"] == 0 and ranges[0]["style"] == "r"
    assert ranges[1]["startpage"] == 5 and ranges[1]["style"] == "D" and ranges[1]["firstpagenum"] == 1

def test_original_content_boundaries(pdf_document):
    """
    Ensure PDF page 6 contains original page 1 (Śiva-Sūtras)
    and PDF page 481 contains original page 476 (final Sūtra 8.4.68).
    """
    p6_text = pdf_document[5].get_text()
    assert "शिवसूत्राणि" in p6_text or "Śiva-Sūtra" in p6_text, "PDF page 6 does not contain Śiva-Sūtras"

    p481_text = pdf_document[480].get_text()
    assert "8, 4, 68" in p481_text, "PDF page 481 does not contain final Sūtra 8, 4, 68"
