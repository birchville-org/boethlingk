# Case Study: Pāṇini's Grammar (Otto von Böhtlingk, 1887)

> **Scholarly digital edition, canonical Sūtra alignment, and Typst vector typesetting for 3,997 Sūtras across 478 pages.**
>
> 🔗 **Project Repository:** [github.com/birchville-org/boethlingk](https://github.com/birchville-org/boethlingk)  
> 🔗 **Core Pipeline:** [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)

---

## 1. Context & Scope

Otto von Böhtlingk's edition *Pâṇini's Grammatik* (2nd edition, Leipzig 1887) is the definitive historical reference work for the grammatical system of the Aṣṭādhyāyī. Across 478 book pages, the work unites three distinct scripts:

1. **Sanskrit in Devanāgarī:** 19th-century metal type with complex conjunct ligatures and virāmas.
2. **German in historical Antiqua:** Scholarly translation and grammatical commentary.
3. **IAST Transliteration:** Latin script with multiple diacritics (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṃ`, `ḥ`, `ṅ`, `ñ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`) and Vedic accent marks.

This project serves as an end-to-end **reference case study** for the open-source book digitization pipeline [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich).

---

## 2. Core Pipeline vs. Böhtlingk Delta

All generic document ingestion, OCR, and image-processing tasks are handled by the central **AlexandriaSandwich pipeline**. The `boethlingk` repository focuses strictly on the **semantic and philological delta**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│            ALEXANDRIASANDWICH (GENERIC CORE PIPELINE)                  │
│  • IIIF Facsimile Ingestion (Heidelberg University Library)            │
│  • Multimodal AI OCR (mistral-ocr-latest) & Bounding-Box Geometry      │
│  • Content-Aware Margin Masking (Background Tone #f0e8d6)              │
│  • Geometric Layout Profiling (layout.profile.json)                    │
│  • 1:1 Sandwich PDF Assembly & QA Viewer Standard                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Bounding Boxes, Layout & Facsimiles
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   THE BÖHTLINGK DELTA (EDITION LAYER)                  │
│  • Delta 1: Canonical 8-Adhyāya State Machine (align_mistral_sutras)   │
│  • Delta 2: Fuzzy SequenceMatcher against Aṣṭādhyāyī Sūtrapāṭha        │
│  • Delta 3: Typst Template for Devanāgarī, IAST & Apparatus Layout     │
│  • Delta 4: RelaxNG-validated TEI-P5 XML & EPUB 3 Serialization        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The Böhtlingk Delta in Detail

### 3.1 Delta 1: Canonical Sūtra State Machine (`scripts/align_mistral_sutras.py`)
The work strictly follows the structural framework of the Aṣṭādhyāyī:
* **Canonical Structure:** 8 Adhyāyas with exactly 4 Pādas each (32 Pādas total) comprising 3,983 Aṣṭādhyāyī Sūtras plus 14 introductory Śiva-Sūtras (3,997 Sūtras total).
* **Automatic Pāda & Adhyāya Rollover:** When the end of a Pāda is reached, the state machine enforces the canonical transition (`state["adhyaya"] += 1, state["pada"] = 1`), even if the printed colophon is faint or damaged.
* **Corrigenda Isolation:** Böhtlingk's addenda and corrections (pp. 477–478) following the final Sūtra 8.4.68 (`अ अ`) are isolated and do not contaminate the commentary apparatus.

### 3.2 Delta 2: Fuzzy Canonical Matching against Ground Truth
Worn metal type occasionally caused OCR misidentifications in Devanāgarī numerals (e.g. ८ misread as ६, hence `६५` instead of `८५`):
* **SequenceMatcher Alignment:** When a Sūtra number diverges, the normalized Devanāgarī line is matched against the expected text in `data/sutras.json`.
* **Correction Threshold:** With similarity >= 0.45, the Sūtra index is automatically corrected to the canonical reference.
* **Long Compounds:** Sūtras spanning up to 350 characters without heading markers (e.g. 5.4.77 with 185 characters) are reliably detected via danda delimiter patterns (`॥...॥`).

### 3.3 Delta 3: Modern Typographic Edition (`scripts/boethlingk1887_edition.typ`)
A specialized Typst template formats the multi-tier edition:
* **Per-Sūtra Hierarchy:**
  1. Devanāgarī heading with canonical index (`१.१.१`).
  2. Academic IAST transliteration (Bold).
  3. German translation (Italic).
  4. Indented commentary apparatus with Böhtlingk abbreviations (`∠±`, `Kāç.`, `RV.`).
* **Book Design:** ISO B5 (176 x 250 mm), font stack (*Noto Serif Devanagari* + *Libertinus Serif*), running headers, and 47 hierarchical PDF bookmarks.
* **Compilation:** Executed via `python3 scripts/build_typeset_edition.py` in ~8.9 seconds.

### 3.4 Delta 4: Standardized TEI-P5 XML & EPUB 3
* **TEI-P5 XML (`data/tei/boehtlingk1887_p5.xml`):** 100% schema-valid against TEI All RelaxNG (`schemas/tei_all.rng`), featuring 3,997 `<tei:entry>` elements and 478 `<tei:pb>` page breaks linked to Heidelberg IIIF endpoints.
* **EPUB 3 (`boethlingk1887.epub`):** Reflowable e-book with embedded fonts ensuring diacritic preservation on e-readers.

---

## 4. Validation Results

All 8 Adhyāyas and the introductory Śiva-Sūtras were validated 1:1 against the canonical ground-truth database:

| Section | Book Pages | Sūtras (Actual / Target) | Duplicates | Gaps | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Śiva-Sūtrāṇi** | 1 | 14 / 14 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 1** | 2–43 | 351 / 351 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 2** | 43–75 | 268 / 268 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 3** | 75–148 | 631 / 631 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 4** | 149–221 | 635 / 635 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 5** | 221–282 | 555 / 555 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 6** | 283–374 | 736 / 736 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 7** | 375–428 | 438 / 438 | 0 | 0 | **100.0% Validated** |
| **Adhyāya 8** | 429–478 | 369 / 369 | 0 | 0 | **100.0% Validated** |
| **Total** | **478 Pages** | **3,997 / 3,997** | **0** | **0** | **100.0% Gap-free** |

---

## 5. Core Artifacts & Downloads

| Artifact | Format / File | Size | Link |
| :--- | :--- | :--- | :--- |
| **Sandwich PDF** | `boehtlingk1887.perfect_sandwich.pdf` | 248.85 MB (478 pp.) | [Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) |
| **Typeset Edition** | `boethlingk1887_typeset_edition.pdf` | 7.62 MB (737 pp.) | [Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition_v2.pdf) |
| **Master Dataset** | `data/ashtadhyayi_complete_boethlingk1887.json` | 2.85 MB | [GitHub Repository](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) |
| **TEI-P5 XML** | `data/tei/boehtlingk1887_p5.xml` | 2.90 MB | [GitHub Repository](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) |
| **EPUB 3** | `boethlingk1887.epub` | 1.47 MB | [Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) |
| **QA Viewer** | `viewer.html` | 39 KB | [View in Browser](https://github.com/birchville-org/boethlingk/blob/main/viewer.html) |
