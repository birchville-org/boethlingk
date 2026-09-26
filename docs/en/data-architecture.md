# Data Architecture — boethlingk

## Project Structure

```text
boethlingk/
├── data/
│   ├── ashtadhyayi_complete_boethlingk1887.json  Canonical Master dataset (3,997 Sūtras)
│   ├── sutras.json                              Aṣṭādhyāyī canonical reference database
│   ├── shiva_sutras.json                        14 Śiva-Sūtras reference
│   ├── mistral/                                 Mistral OCR Markdown & Bounding-Box JSON (478 pages)
│   ├── tei/                                     TEI-P5 XML Master edition (boehtlingk1887_p5.xml)
│   ├── img_cache/                               Local cache of Heidelberg IIIF scans
│   └── output/                                  Output directory for 1:1 Sandwich PDF
│
├── docs/                                        Bilingual documentation (de / en)
│   ├── de/                                      German documentation
│   └── en/                                      English documentation
│
├── extern/                                      Comparative reference editions (Books I–VIII)
├── schemas/                                     RelaxNG Schema (tei_all.rng)
├── scripts/                                     Pipeline scripts (OCR, Alignment, TEI, PDF)
├── viewer.html                                  Standalone QA Viewer (Payer Standard)
└── viewer_screenshot.png                        QA Viewer interface demonstration
```

---

## Three-Layer Model

```text
Layer 1 — Facsimile Image Base
  Source:  IIIF Image API, Heidelberg University Library
  URL:     https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/...
  Access:  Direct URL / cached in data/img_cache/
  Purpose: Visual base in TEI (<pb facs="..."/>) and visual background in 1:1 Sandwich PDF

Layer 2 — Multimodal AI OCR & Geometry
  Source:  Mistral OCR (mistral-ocr-latest)
  Storage: data/mistral/*.mistral.json and *.mistral.md
  Content: Word bounding boxes, DPI dimensions, hierarchical markdown
  Quality: Full multi-script recognition across Devanāgarī, German Antiqua, and IAST

Layer 3 — Canonical TEI/XML & Master JSON Edition
  Storage: data/tei/boehtlingk1887_p5.xml & data/ashtadhyayi_complete_boethlingk1887.json
  Content: Sūtra-anchored digital edition with IIIF links, commentary, translations, and corrigenda
  Status:  100.0% schema-valid against TEI All RelaxNG
```

---

## Processing Pipeline

```text
[IIIF Facsimiles]
       │
       ▼
[Stage 1: Local Cache] ─────────► data/img_cache/
       │
       ▼
[Stage 2: Mistral OCR] ─────────► data/mistral/ (*.md, *.json)
       │
       ▼
[Stage 3: Canonical Alignment] ──► scripts/align_mistral_sutras.py
       │                           (Fuzzy match vs. data/sutras.json)
       ▼
[Stage 4: Master Consolidation] ─► data/ashtadhyayi_complete_boethlingk1887.json
       │
       ▼
[Stage 5: Multi-Artifact Build]
       ├── TEI-P5 XML:          data/tei/boehtlingk1887_p5.xml
       ├── 1:1 Sandwich PDF:    data/output/boehtlingk1887_sandwich.pdf
       └── QA Viewer:           viewer.html
```
