"""
Tests for text and data integrity in Böhtlingk 1887.
Audits all 14 Śiva-Sūtras, 3,983 Aṣṭādhyāyī sūtras, and 50 Corrigenda entries against a
strict Unicode script whitelist, placeholder ban, orphan punctuation checks, and regression anchors.
"""

import json
import re
import unicodedata
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data" / "ashtadhyayi_complete_boethlingk1887.json"
CORRIGENDA_PATH = REPO_ROOT / "data" / "corrigenda.json"

PERMITTED_LETTER_PREFIXES = ("LATIN", "DEVANAGARI", "VEDIC", "GREEK", "COMBINING", "MODIFIER")
PERMITTED_NUMBER_PREFIXES = ("DIGIT", "DEVANAGARI", "SUPERSCRIPT", "VULGAR")


@pytest.fixture(scope="module")
def dataset():
    assert DATA_PATH.exists(), f"Master dataset not found at {DATA_PATH}"
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def corrigenda():
    assert CORRIGENDA_PATH.exists(), f"Corrigenda file not found at {CORRIGENDA_PATH}"
    with open(CORRIGENDA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _iter_corpus_texts(dataset, corrigenda):
    """Yield (record_id, field_name, text) across Śiva-Sūtras, Sūtrapāṭha, and Corrigenda."""
    for i, ss in enumerate(dataset.get("shiva_sutras", []), start=1):
        rid = f"shiva:{ss.get('sutra_num', ss.get('num', i))}"
        for field, val in ss.items():
            if isinstance(val, str) and val:
                yield rid, field, val

    for s in dataset.get("sutras", []):
        rid = s["ref"]
        for field in ("canonical_devanagari", "canonical_iast", "translation", "commentary", "sutra_num_deva"):
            val = s.get(field) or ""
            if val:
                yield rid, field, val

    for i, c in enumerate(corrigenda, start=1):
        txt = c.get("text") or ""
        if txt:
            yield f"corrigenda:{i}", "text", txt


def test_corpus_completeness_and_uniqueness(dataset, corrigenda):
    """Ensure all 14 Śiva-Sūtras, 3,983 Aṣṭādhyāyī sūtras (total 3,997, 0 duplicates), and 50 Corrigenda exist."""
    shiva = dataset.get("shiva_sutras", [])
    sutras = dataset.get("sutras", [])
    assert len(shiva) == 14, f"Expected 14 Śiva-Sūtras, found {len(shiva)}"
    assert len(sutras) == 3983, f"Expected 3983 Aṣṭādhyāyī sūtras, found {len(sutras)}"
    assert len(shiva) + len(sutras) == 3997

    refs = [s.get("ref") for s in sutras]
    assert len(refs) == len(set(refs)), "Duplicate sūtra references detected in master dataset"
    assert len(corrigenda) == 50, f"Expected 50 corrigenda entries, found {len(corrigenda)}"


def test_no_placeholder_tokens(dataset, corrigenda):
    """Ensure no generic placeholder tokens like [Sanskrit] or [OCR] exist."""
    forbidden_pattern = re.compile(r"\[(Sanskrit|OCR|TODO|FIXME)\]|\?\?\?", re.IGNORECASE)
    violations = []

    for rid, field, val in _iter_corpus_texts(dataset, corrigenda):
        matches = forbidden_pattern.findall(val)
        if matches:
            violations.append((rid, field, matches))

    assert not violations, f"Found forbidden placeholder tokens: {violations}"


def test_unicode_script_whitelist(dataset, corrigenda):
    """
    Positive Unicode script whitelist across all corpus letters, marks, and numerals.
    Permits only Latin (incl. IAST), Devanāgarī, Vedic, Greek, Combining/Modifier,
    and ASCII/Devanāgarī/Superscript/Vulgar numerals.
    """
    violations = []

    for rid, field, val in _iter_corpus_texts(dataset, corrigenda):
        for ch in val:
            cat = unicodedata.category(ch)
            name = unicodedata.name(ch, f"UNNAMED_{ord(ch):04X}")
            if cat[0] in ("L", "M"):
                if not name.startswith(PERMITTED_LETTER_PREFIXES):
                    violations.append((rid, field, ch, cat, name))
            elif cat[0] == "N":
                if not name.startswith(PERMITTED_NUMBER_PREFIXES):
                    violations.append((rid, field, ch, cat, name))

    assert not violations, f"Found non-whitelisted script/numeral tokens: {violations[:10]}"


def test_no_isolated_orphan_punctuation(dataset, corrigenda):
    """Ensure no orphan punctuation (e.g., ' , ' or ', , ') caused by silent letter deletion."""
    orphan_pattern = re.compile(r"\s+,\s+|, ,|\(\s*,|[a-zA-ZäöüÄÖÜß]\s{2,},")
    violations = []

    for rid, field, val in _iter_corpus_texts(dataset, corrigenda):
        if field in ("translation", "commentary", "text"):
            m = orphan_pattern.search(val)
            if m:
                violations.append((rid, field, m.group()))

    assert not violations, f"Found orphan punctuation anomalies: {violations[:10]}"


def test_restored_ocr_regression_anchors(dataset):
    """Verify repaired OCR readings remain intact across historically affected sūtras."""
    by_ref = {s["ref"]: s for s in dataset["sutras"]}

    assert "प्रतिदीव्नः" in by_ref["1.1.58"]["commentary"]
    assert "जक्षतुः" in by_ref["1.1.58"]["commentary"]
    assert "कु, चु, टु, तु, पु" in by_ref["1.1.69"]["translation"]
    assert "folgendem त् bezeichnet" in by_ref["1.1.70"]["translation"]
    assert "अत् nur das kurze अ, इत् nur das kurze इ" in by_ref["1.1.70"]["commentary"]
    assert "ङी oder आप्" in by_ref["4.1.1"]["translation"]
    assert "tritt ङी." in by_ref["4.1.5"]["translation"]
    assert by_ref["4.4.11"]["translation"] == "An श्वगण auch ±´_इक."
    assert by_ref["5.1.17"]["translation"] == "An परिखा tritt in dieser Bedeutung ±´_एय an."
    assert by_ref["6.3.51"]["translation"] == "Vor शोक, vor dem Suffix ±´_य und vor रोग nicht nothwendig."
