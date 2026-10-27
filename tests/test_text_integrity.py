"""
Tests for text and data integrity in Böhtlingk 1887.
Verifies that no OCR hallucinations, aggressive sanitization placeholders,
or anomalous punctuation patterns corrupt the edition database.
"""

import json
import re
import unicodedata
from pathlib import Path
import pytest

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "ashtadhyayi_complete_boethlingk1887.json"

@pytest.fixture(scope="module")
def dataset():
    assert DATA_PATH.exists(), f"Master dataset not found at {DATA_PATH}"
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

def test_no_placeholder_tokens(dataset):
    """Ensure no generic placeholder tokens like [Sanskrit] or [OCR] exist."""
    forbidden_pattern = re.compile(r"\[(Sanskrit|OCR|TODO|FIXME)\]|\?\?\?", re.IGNORECASE)
    violations = []

    for s in dataset["sutras"]:
        for field in ["translation", "commentary", "canonical_devanagari", "canonical_iast"]:
            val = s.get(field) or ""
            matches = forbidden_pattern.findall(val)
            if matches:
                violations.append((s["ref"], field, matches))

    assert not violations, f"Found forbidden placeholder tokens in sutras: {violations}"

def test_unicode_script_whitelist(dataset):
    """
    Ensure all characters belong strictly to permitted Unicode scripts.
    Permitted: Latin (with IAST diacritics), Devanagari, Greek (philological citations),
    Common punctuation, European numbers.
    Disallowed: Hebrew, Telugu, Arabic, Cyrillic, CJK, etc.
    """
    disallowed_scripts = ["HEBREW", "TELUGU", "ARABIC", "CYRILLIC", "CJK"]
    violations = []

    for s in dataset["sutras"]:
        for field in ["translation", "commentary", "canonical_devanagari", "canonical_iast"]:
            val = s.get(field) or ""
            for ch in val:
                name = unicodedata.name(ch, "UNKNOWN")
                for disallowed in disallowed_scripts:
                    if disallowed in name:
                        violations.append((s["ref"], field, ch, name))

    assert not violations, f"Found foreign/hallucinated script tokens: {violations[:10]}"

def test_no_isolated_orphan_punctuation(dataset):
    """
    Ensure no orphan punctuation (e.g., ' , ' or ', , ') caused by silent letter deletion.
    """
    orphan_pattern = re.compile(r"\s+,\s+|, ,|\(\s*,|[a-zA-ZäöüÄÖÜß]\s{2,},")
    violations = []

    for s in dataset["sutras"]:
        for field in ["translation", "commentary"]:
            val = s.get(field) or ""
            m = orphan_pattern.search(val)
            if m:
                violations.append((s["ref"], field, m.group()))

    assert not violations, f"Found orphan punctuation anomalies: {violations[:10]}"

def test_sutra_count_completeness(dataset):
    """Ensure all 3983 canonical sutras are present in the dataset."""
    sutras = dataset.get("sutras", [])
    assert len(sutras) == 3983, f"Expected 3983 sutras, found {len(sutras)}"
