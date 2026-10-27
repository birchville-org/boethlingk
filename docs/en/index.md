<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--md-default-bg-color--light); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;">
  <img src="assets/birchville_logo.png" alt="Birchville Coat of Arms" style="height: 2.4rem; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18));">
  <div>
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--md-accent-fg-color); font-weight: 700;">Birchville Scholarly Synthesis</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--md-default-fg-color);">Canonical Editions of Classical Philological Reference Works</div>
  </div>
</div>

# 📖 Pāṇini's Grammar (Otto von Böhtlingk, Leipzig 1887)

**Scholarly digitization, canonical alignment, TEI-P5 edition, and typographical 1:1 facsimile typeset of Otto von Böhtlingk's *Pâṇini's Grammatik* (2nd edition, Leipzig 1887).**

---

## ⚡ Quick Access & Downloads

<div class="quick-access-grid">
  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🏛️</span>
        <span class="quick-card-title">1:1 Facsimile Typeset</span>
      </div>
      <div class="quick-card-body">
        Modern vector typeset in STIX Two Text with <strong>exact 1:1 page parity</strong> (476 text pages without overflow), adaptive typography, native IAST small caps, and 48 PDF bookmarks.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf" class="quick-btn quick-btn-primary" target="_blank" rel="noopener">
        <span>⬇️</span> Facsimile PDF (8.6 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📚</span>
        <span class="quick-card-title">1:1 Sandwich PDF</span>
      </div>
      <div class="quick-card-body">
        478-page high-resolution scan facsimile from Heidelberg University Library with Content-Aware Margin Masking (#f0e8d6), invisible OCR text layer (14,267 text blocks), and 42 bookmarks.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>⬇️</span> Sandwich PDF (249 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📦</span>
        <span class="quick-card-title">All Artifacts & Downloads</span>
      </div>
      <div class="quick-card-body">
        Detailed catalog of all digital edition artifacts (facsimile typeset, book edition, EPUB 3, TEI-P5 XML, master JSON, QA viewer) with format descriptions and release links.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="artifacts/" class="quick-btn quick-btn-outline">
        <span>➔</span> Open Artifact Catalog
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🔍</span>
        <span class="quick-card-title">The Böhtlingk Delta</span>
      </div>
      <div class="quick-card-body">
        Specific procedural extensions beyond the generic AlexandriaSandwich pipeline: sūtra state machine, fuzzy matching, adaptive typography, and TEI-P5 modeling.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="case-study/" class="quick-btn quick-btn-outline">
        <span>➔</span> Read Edition Delta
      </a>
    </div>
  </div>
</div>

---

## 🌟 About the Project & Pipeline Demarcation

This project encompasses the complete historical processing, multimodal AI transcription (Mistral OCR), gapless canonical alignment against the Aṣṭādhyāyī Sūtrapāṭha, and the generation of standardized digital edition artifacts for Otto von Böhtlingk's landmark 1887 Pāṇini edition based on scans from the Heidelberg University Library.

> ℹ️ **Relation to the AlexandriaSandwich Pipeline:**  
> All generic steps of image processing, IIIF caching, multimodal AI OCR (`mistral-ocr-latest`), Content-Aware Margin Masking (`#f0e8d6`), and 1:1 sandwich PDF assembly are powered by the core book digitization pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**.  
>  
> For the comprehensive description of the underlying pipeline architecture, please refer to:  
> 👉 **[AlexandriaSandwich Pipeline Documentation](https://birchville-org.github.io/AlexandriaSandwich/en/WIKI_VERFAHREN/)**  
>  
> This repository `boethlingk` focuses exclusively on the **specific philological and typographical edition delta** (canonical state machine, 1:1 page parity, STIX Two Text font stack, TEI-P5 encoding).

---

## 🏛️ Digital Edition Artifacts at a Glance

All print-ready and archival release files are available on the official GitHub Releases page:

* **1:1 Dense Facsimile Typeset (Vector PDF):** `boethlingk1887_facsimile_dense.pdf` (8.58 MB · 484 pp.)  
  Exact 1:1 page parity with the historical 1887 Leipzig print, adaptive typography, and STIX Two Text font stack with native IAST small caps (**PĀṆINI**, **MAHĀBHĀṢYA**).  
  [:octicons-download-16: Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf)

* **Modernized Book Edition (Vector PDF):** `boethlingk1887_typeset_edition.pdf` (8.81 MB · 512 pp.)  
  Reflowable book layout in ISO B5 format optimized for continuous study.  
  [:octicons-download-16: Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf)

* **1:1 Sandwich PDF (Scan Facsimile):** `boehtlingk1887_sandwich.pdf` (248.8 MB · 478 pp.)  
  High-resolution Heidelberg scans with Content-Aware Margin Masking and invisible OCR text layer (14,267 text blocks).  
  [:octicons-download-16: Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf)

* **Canonical Master Dataset (JSON):** `data/ashtadhyayi_complete_boethlingk1887.json` (2.85 MB)  
  3,997 sūtras complete (14 Śiva-Sūtras + 3,983 Aṣṭādhyāyī sūtras, 0 duplicates, 0 gaps) with Devanāgarī, IAST, translation, and commentary.  
  [:octicons-mark-github-16: View on GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

* **Schema-Valid TEI-P5 XML Edition:** `data/tei/boehtlingk1887_p5.xml` (2.90 MB)  
  100% valid against TEI All RelaxNG (`schemas/tei_all.rng`) with 478 `<pb>` tags linked to Heidelberg IIIF manifests.  
  [:octicons-mark-github-16: View on GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml)

* **Reflowable EPUB 3 eBook:** `boethlingk1887.epub` (1.47 MB)  
  Mobile e-book with embedded fonts (*Noto Serif Devanagari*) and hierarchical table of contents.  
  [:octicons-download-16: Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub)

* **Standalone QA Viewer:** `viewer.html` (39 KB)  
  Browser-based split-pane editor conforming to the Payer standard for direct local proofreading.  
  [:octicons-eye-16: View on GitHub](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)

👉 **Comprehensive Artifact Details:** [Edition Artifacts & Downloads](artifacts.md)

---

## 📖 Documentation Directory

* [📦 Edition Artifacts & Downloads](artifacts.md) – Comprehensive catalog of all release files with direct links
* [🔍 The Böhtlingk Delta & Methodology](case-study.md) – Methodological differentiation and edition satellite rationale
* [🛠️ QA & Correction Workflow](qa-workflow.md) – Single Source of Truth & local proofreading in the QA viewer
* [🏛️ Data Architecture](data-architecture.md) – Three-layer data model
* [📜 Copyright & Provenance](copyright-and-provenance.md) – Heidelberg University Library source credits
* [📐 Conventions](conventions.md) – Transliteration and encoding standards
