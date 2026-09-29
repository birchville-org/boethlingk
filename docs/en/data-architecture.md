# 🏛️ Data Architecture — boethlingk

> This document describes the directory structure, the three-layer data model, and the processing pipelines of the `boethlingk` reference case study.

---

## 1. Project Structure

```text
boethlingk/
├── data/
│   ├── ashtadhyayi_complete_boethlingk1887.json  # Canonical Master dataset (Single Source of Truth, 3,997 Sūtras)
│   ├── ashtadhyayi_grouped_edition.json          # Pre-grouped dataset for Typst typesetting
│   ├── sutras.json                              # Aṣṭādhyāyī canonical reference database
│   ├── shiva_sutras.json                        # 14 Śiva-Sūtras reference
│   ├── corrigenda.json                          # 50 Corrigenda items from pages 477–478
│   ├── mistral/                                 # 478 pages Mistral OCR Markdown (*.md) & Bounding-Box JSON (*.json)
│   ├── tei/                                     # TEI-P5 XML Master edition (boehtlingk1887_p5.xml)
│   ├── img_cache/                               # Local cache of 484 Heidelberg IIIF scans
│   └── output/                                  # Output directory for Sandwich PDF, Typst PDF, and EPUB
│
├── docs/                                        # Bilingual MkDocs documentation
│   ├── de/                                      # German documentation (default)
│   └── en/                                      # English documentation
│
├── schemas/                                     # RelaxNG Schema (tei_all.rng)
├── scripts/                                     # Automation & pipeline scripts
│   ├── download_scans.py                        # Batch-fetch scans from Heidelberg IIIF API
│   ├── mistral_ocr.py                           # Mistral OCR client (mistral-ocr-latest)
│   ├── batch_ocr_runner.py                      # Multi-page OCR orchestration
│   ├── align_mistral_sutras.py                  # Canonical alignment & fuzzy matching
│   ├── build_sandwich_pdf.py                    # 1:1 Sandwich PDF assembler
│   ├── build_typeset_edition.py                 # Typst book edition compiler
│   ├── generate_tei_p5.py                       # TEI-P5 XML generator & RelaxNG validator
│   └── export_epub.py                           # Reflowable EPUB 3 generator
│
├── viewer.html                                  # Standalone QA Viewer (Payer Standard)
├── viewer_screenshot.png                        # Interface demonstration
└── mkdocs.yml                                   # MkDocs configuration
```

---

## 2. Three-Layer Model

```text
Layer 1 — Facsimile Image Base
  Source:  IIIF Image API, Heidelberg University Library
  URL:     https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/...
  Storage: data/img_cache/ (local cache for rapid offline processing)
  Purpose: Visual background in 1:1 Sandwich PDF and image anchor in TEI (<pb facs="..."/>)

Layer 2 — Multimodal AI OCR & Geometry
  Source:  Mistral OCR (model: mistral-ocr-latest)
  Storage: data/mistral/*.mistral.json & *.mistral.md
  Content: Word bounding boxes, DPI dimensions, hierarchical markdown
  Quality: Full multi-script recognition across Devanāgarī, German Antiqua, and IAST

Layer 3 — Canonical TEI/XML & Master JSON Edition
  Storage: data/ashtadhyayi_complete_boethlingk1887.json & data/tei/boehtlingk1887_p5.xml
  Content: Structured Sūtra objects with canonical Devanāgarī, IAST, German translation, and commentary
  Status:  100.0% gapless (3,997 Sūtras) and 100% schema-valid against TEI All RelaxNG
```

---

## 3. Processing Pipeline

```text
[IIIF Facsimiles Heidelberg]
       │
       ▼
[Stage 1: Local Cache] ─────────► data/img_cache/*.jpg
       │
       ▼
[Stage 2: Mistral OCR] ─────────► data/mistral/ (*.md, *.json via mistral-ocr-latest)
       │
       ▼
[Stage 3: Canonical Alignment] ──► scripts/align_mistral_sutras.py
       │                           (SequenceMatcher matching vs. data/sutras.json)
       ▼
[Stage 4: Master Consolidation] ─► data/ashtadhyayi_complete_boethlingk1887.json
       │                           (Single Source of Truth, 3,997 Sūtras)
       ▼
[Stage 5: Multi-Artifact Build]
       ├── TEI-P5 XML:          data/tei/boehtlingk1887_p5.xml
       ├── 1:1 Sandwich PDF:    data/output/boehtlingk1887_sandwich.pdf
       ├── Typst Edition:       data/output/boethlingk1887_typeset_edition.pdf
       ├── Reflowable EPUB 3:   data/output/boethlingk1887.epub
       └── QA Viewer:           viewer.html
```

---

## 4. Key Metrics

| Metric | Value | Remarks |
| :--- | :--- | :--- |
| **Digitized Book Pages** | 478 pages | P. 1 (Śiva-Sūtras), pp. 2–476 (Aṣṭādhyāyī), pp. 477–478 (Addenda) |
| **Total Sūtras** | 3,997 Sūtras | 14 Śiva-Sūtras + 3,983 Aṣṭādhyāyī Sūtras (100.0% gapless) |
| **Duplicates / Missing** | 0 / 0 | Fully verified against canonical Sūtrapāṭha |
| **Sandwich PDF Text Blocks** | 14,267 blocks | Pixel-accurate invisible vector text layer (PDF Render Mode 3) |
| **Typst Edition Pages** | 737 pages | Modern typeset vector edition in ISO B5 |
| **TEI Validation** | 0 errors | 100% valid against RelaxNG (`tei_all.rng`) |
| **Total OCR Cost** | $1.912 | 478 pages x $0.004 via Mistral AI API |
