# 📖 Pāṇini's Grammar (Otto von Böhtlingk, Leipzig 1887)

> **Scholarly digitization, canonical alignment, TEI-P5 edition, and 1:1 sandwich PDF of *Pāṇini's Grammar* (Otto von Böhtlingk, 2nd edition, Leipzig 1887).**

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![TEI P5](https://img.shields.io/badge/TEI--P5-RelaxNG%20valid-green)
![Sandwich PDF](https://img.shields.io/badge/PDF-1%3A1%20Sandwich-orange)
![EPUB 3](https://img.shields.io/badge/eBook-EPUB%203-purple)
![Alignment](https://img.shields.io/badge/Sūtras-3%2C997%20(100%25)-brightgreen)

> ℹ️ **Case Study:** This project serves as an end-to-end reference case study for the open-source book digitization pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**.

This project provides end-to-end historical digitization, multimodal AI OCR (`mistral-ocr-latest`), seamless canonical alignment against the Aṣṭādhyāyī Sūtrapāṭha, and standards-compliant digital edition artifacts for Otto von Böhtlingk's landmark 1887 edition, based on digital facsimiles from Heidelberg University Library.

---

## ✨ Project Outcomes & Core Artifacts

1. **Canonically Validated Master Dataset (100.0%):**
   * File: [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) (2.83 MB)
   * 3,997 complete Sūtras (14 Śiva-Sūtras + 3,983 Aṣṭādhyāyī-Sūtras, 0 duplicates, 0 gaps).
   * Includes Devanāgarī, academic IAST transliteration, German translation, and philological commentary.

2. **Schema-Valid TEI-P5 XML Edition:**
   * File: [`data/tei/boehtlingk1887_p5.xml`](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) (2.90 MB)
   * 100% valid against the official TEI All RelaxNG schema (`schemas/tei_all.rng`).
   * 478 `<pb>` page break elements directly linked to Heidelberg University Library IIIF image endpoints.
   * 50 Corrigenda entries from pages 477–478 embedded in `<back>`.

3. **Searchable 1:1 Sandwich PDF:**
   * Download: [Release Asset (`boehtlingk1887_sandwich.pdf`)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) (278.16 MB, 478 pages)
   * Visual layer: Untouched historical facsimiles (1:1 pixel resolution).
   * Text layer: Invisible vector text layer (PDF Rendering Mode 3) with 14,267 text blocks placed at exact pixel coordinates.
   * 42 hierarchical PDF bookmarks (Śiva-Sūtras, 8 Adhyāyas, 32 Pādas, Corrigenda).

4. **Modern Typeset Book PDF (Typst Edition):**
   * Download: [Release Asset (`boethlingk1887_typeset_edition.pdf`)](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf) (6.28 MB, 737 pages)
   * Visuals & Readability: Crisp, modern vector book typesetting (ISO B5) free from historical scan noise and paper yellowing.
   * Modern Typography: Classic Leipzig layout with modern font rendering – Antiqua (*Baskerville*, *Times New Roman*) paired with native Devanāgarī (*Devanagari MT*, *Kohinoor Devanagari*) and flawless IAST diacritics.
   * Structure & Apparatus: 14 Śiva-Sūtras, all 3,983 Sūtras (Devanāgarī, IAST, translation, commentary), dynamic running headers, table of contents, and integrated corrigenda.
   * Script: Built in ~1–2 seconds via [`scripts/build_typeset_edition.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/build_typeset_edition.py) using the Typst typesetting system.

5. **Reflowable EPUB 3 eBook with Font Embedding:**
   * Download: [Release Asset (`boethlingk1887.epub`)](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) (1.45 MB)
   * Optimized for mobile e-readers: Standardized EPUB 3 with semantic XHTML5, responsive layout, and hierarchical table of contents (8 Adhyāyas, 32 Pādas).
   * Embedded fonts: *Noto Serif Devanagari* (Regular/Bold) and *Linux Libertine O* (Regular/Bold/Italic) ensure flawless rendering of all IAST diacritics and Devanagari ligatures on mobile devices and e-readers (Tolino, Apple Books, Kobo).
   * Script: Generated via [`scripts/export_epub.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/export_epub.py).

6. **Standalone QA Viewer:**
   * File: [`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)
   * Payer-standard split-pane editor featuring facsimile zoom/pan, snippet toolbar, and local silent auto-repair on save.

---

## 🏛️ Pipeline Architecture

```text
[Heidelberg University Library Facsimiles] 
       │ (Pages 1 to 478, JPG)
       ▼
[Stage 1: Local Image Caching] ──► data/img_cache/7_3A000000XXX_...jpg
       │
       ▼
[Stage 2: Multimodal AI OCR] ───► mistral-ocr-latest (Mistral Python SDK)
       │                           ├── data/mistral/*.mistral.md   (Layout Markdown)
       │                           └── data/mistral/*.mistral.json (Bounding Box Geometry)
       ▼
[Stage 3: Canonical Alignment] ─► scripts/align_mistral_sutras.py
       │                           ├── Heuristic Sūtra segmentation (#, ##, ॥...॥)
       │                           ├── SequenceMatcher validation against data/sutras.json
       │                           ├── 4-Pāda-per-Adhyāya state machine
       │                           └── Colophon and noise filtering
       ▼
[Stage 4: Consolidation] ──────► data/ashtadhyayi_complete_boethlingk1887.json
       │                           (3,997 Sūtras = 100.0% coverage & 0 duplicates)
       ▼
[Stage 5: TEI, Sandwich & ─────► data/tei/boehtlingk1887_p5.xml
          Typst Assembly]        data/output/boehtlingk1887_sandwich.pdf
                                 data/output/boethlingk1887_typeset_edition.pdf
```

---

## 🚀 Quickstart

### Generate and validate TEI-P5 XML
```bash
uv run --with lxml python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### Build 1:1 Sandwich PDF
```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

### Compile Modern Typeset Book PDF (Typst)
```bash
python3 scripts/build_typeset_edition.py
```

---

## 📖 Documentation Index

* [Scholarly Case Study & Pipeline Methodology](case-study.md)
* [Data Architecture & Three-Layer Model](data-architecture.md)
* [Architectural Pipeline Decisions](pipeline-decisions.md)
* [Conventions & IIIF Specification](conventions.md)
* [Wiki Overview](wiki-home.md)
