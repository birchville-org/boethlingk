<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--md-default-bg-color--light); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;">
  <img src="assets/birchville_logo.png" alt="Birchville Coat of Arms" style="height: 2.4rem; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18));">
  <div>
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--md-accent-fg-color); font-weight: 700;">Birchville Scholarly Synthesis</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--md-default-fg-color);">Canonical Editions of Classical Indological Reference Works</div>
  </div>
</div>

# 📖 Pāṇini's Grammar (Otto von Böhtlingk, Leipzig 1887)

**Scholarly digitization, canonical alignment, TEI-P5 edition, and 1:1 sandwich PDF of *Pāṇini's Grammar* (Otto von Böhtlingk, 2nd edition, Leipzig 1887).**

---

## ⚡ Quick Access & Downloads

<div class="quick-access-grid">
  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📚</span>
        <span class="quick-card-title">Sandwich PDF (1:1)</span>
      </div>
      <div class="quick-card-body">
        478-page high-resolution scan facsimile with OCR text layer (14,267 text blocks) and 42 bookmarks.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf" class="quick-btn quick-btn-primary" target="_blank" rel="noopener">
        <span>⬇️</span> Sandwich PDF (278 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📄</span>
        <span class="quick-card-title">Typst Vector Typeset</span>
      </div>
      <div class="quick-card-body">
        737-page modern vector book edition (ISO B5) with all 3,997 Sūtras, translation, commentary, and running headers.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>⬇️</span> Book Edition (6.3 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🏛️</span>
        <span class="quick-card-title">Academic Case Study</span>
      </div>
      <div class="quick-card-body">
        End-to-end methodology report documenting the AlexandriaSandwich pipeline and canonical alignment.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="case-study.md" class="quick-btn quick-btn-outline">
        <span>➔</span> Read Case Study
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">💻</span>
        <span class="quick-card-title">Source Code & Pipeline</span>
      </div>
      <div class="quick-card-body">
        Canonical JSON master dataset, RelaxNG-validated TEI-P5 XML, and build automation on GitHub.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>➔</span> GitHub Repository
      </a>
    </div>
  </div>
</div>

---

## 🌟 About the Project

This project provides end-to-end historical digitization, multimodal AI OCR (`mistral-ocr-latest`), seamless canonical alignment against the Aṣṭādhyāyī Sūtrapāṭha, and standards-compliant digital edition artifacts for Otto von Böhtlingk's landmark 1887 edition, based on digital facsimiles from Heidelberg University Library.

> ℹ️ **Case Study:** This project serves as an end-to-end reference case study for the open-source book digitization pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**.

---

## 🏛️ Project Outcomes & Core Artifacts

- **Searchable 1:1 Sandwich PDF** (`boehtlingk1887_sandwich.pdf` · 278.2 MB)  
  478-page high-resolution scan facsimile of the Heidelberg exemplar with an invisible vector text layer (14,267 text blocks placed at exact coordinates) and 42 hierarchical PDF bookmarks.  
  [:octicons-download-16: Release Download (278 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) · [:octicons-tag-16: GitHub Release](https://github.com/birchville-org/boethlingk/releases/latest)

- **Modern Typeset Book PDF (Typst Edition)** (`boethlingk1887_typeset_edition.pdf` · 6.3 MB)  
  737-page crisp vector book edition (ISO B5) with all 3,997 Sūtras (Devanāgarī, IAST, translation, commentary), running headers, and table of contents.  
  [:octicons-download-16: Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf) · [:octicons-mark-github-16: Build Script](https://github.com/birchville-org/boethlingk/blob/main/scripts/build_typeset_edition.py)

- **Canonically Validated Master Dataset (JSON)** (`data/ashtadhyayi_complete_boethlingk1887.json` · 2.8 MB)  
  3,997 complete Sūtras (14 Śiva-Sūtras + 3,983 Aṣṭādhyāyī-Sūtras, 0 duplicates, 0 gaps) with Devanāgarī, academic IAST transliteration, German translation, and philological commentary.  
  [:octicons-mark-github-16: File on GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

- **Schema-Valid TEI-P5 XML Edition** (`data/tei/boehtlingk1887_p5.xml` · 2.9 MB)  
  100% valid against the official TEI All RelaxNG schema (`schemas/tei_all.rng`) with 478 `<pb>` page break elements linked directly to Heidelberg University Library IIIF image endpoints.  
  [:octicons-mark-github-16: File on GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml)

- **Reflowable EPUB 3 eBook with Font Embedding** (`boethlingk1887.epub` · 1.5 MB)  
  Standardized EPUB 3 with semantic XHTML5, responsive layout, and embedded fonts (*Noto Serif Devanagari*, *Linux Libertine O*) ensuring complete diacritic integrity on mobile e-readers.  
  [:octicons-download-16: Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) · [:octicons-mark-github-16: Export Script](https://github.com/birchville-org/boethlingk/blob/main/scripts/export_epub.py)

- **Standalone QA Viewer** (`viewer.html`)  
  Payer-standard split-pane editor featuring facsimile zoom/pan, snippet toolbar, and local silent auto-repair on save.  
  [:octicons-eye-16: Viewer in Repository](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)

---

## 🏛️ Pipeline Architecture

```text
[Heidelberg University Library Facsimiles] 
       │ (Pages 1 to 478, JPG)
       ▼
[Step 1: Local Image Caching] ──► data/img_cache/7_3A000000XXX_...jpg
       │
       ▼
[Step 2: Multimodal AI OCR] ────► mistral-ocr-latest (Mistral Python SDK)
       │                              ├── data/mistral/*.mistral.md   (Layout Markdown)
       │                              └── data/mistral/*.mistral.json (Bounding Box Geometry)
       ▼
[Step 3: Canonical Alignment] ──► scripts/align_mistral_sutras.py
       │                              ├── Heuristic Sūtra segmentation (#, ##, ॥...॥)
       │                              ├── SequenceMatcher alignment against data/sutras.json
       │                              ├── 4-Pāda per Adhyāya state machine
       │                              └── Colophon & noise elimination
       ▼
[Step 4: Consolidation] ────────► data/ashtadhyayi_complete_boethlingk1887.json
       │                              (3,997 Sūtras = 100.0% gap-free & 0 duplicates)
       ▼
[Step 5: TEI, Sandwich & ───────► data/tei/boehtlingk1887_p5.xml
         Typst Assembly]               data/output/boehtlingk1887_sandwich.pdf
                                       data/output/boethlingk1887_typeset_edition.pdf
```

---

## 🚀 Quickstart

### Generate and Validate TEI-P5 XML
```bash
uv run --with lxml python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### Compile 1:1 Sandwich PDF
```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

### Compile Typeset Book PDF (Typst)
```bash
python3 scripts/build_typeset_edition.py
```

---

## 📖 Documentation Overview

* [Academic Case Study (Pipeline Documentation)](case-study.md)
* [Data Architecture & Three-Layer Model](data-architecture.md)
* [Conventions & IIIF Specification](conventions.md)
* [Wiki Index](wiki-home.md)

---

## 📜 License & Provenance

- **Historical Original**: Otto von Böhtlingk (1815–1904), *Pâṇini's Grammatik*, 2nd edition, Leipzig 1887 (Public Domain).
- **Digital Edition, TEI-P5 & Pipeline**: [MIT License](https://github.com/birchville-org/boethlingk/blob/main/LICENSE) (Copyright (c) 2026 Marco Demarmels / Birchville Foundation).
- **Referenced Projects**:
  - [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich) — Hybrid OCR & Book Digitization Pipeline
  - [macdonell](https://github.com/birchville-org/macdonell) — A Vedic Grammar for Students (1916) 1:1 Typeset Edition
  - [sanskritkurs-payer](https://github.com/birchville-org/sanskritkurs-payer) — Digital Payer Sanskrit Course
