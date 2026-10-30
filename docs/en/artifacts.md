# 📦 Edition Artifacts & Downloads

This edition project generates a coherent family of digital artifacts designed for research, teaching, long-term archival preservation, and philological practice. All binary artifacts (PDFs, EPUB, XML) are distributed via the official GitHub releases.

> ⬇️ **Central Release Downloads:**  
> All current release artifacts are available directly on the GitHub Releases page:  
> 👉 **[github.com/birchville-org/boethlingk/releases/latest](https://github.com/birchville-org/boethlingk/releases/latest)**

---

## 🏛️ Digital Artifact Overview

The artifacts address diverse research workflows – ranging from exact historical citation verification to computational linguistics:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             SINGLE SOURCE OF TRUTH (CANONICAL MASTER DATASET)          │
│                ashtadhyayi_complete_boethlingk1887.json                │
│                 (3,997 Sūtras · Devanāgarī, IAST, German)              │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│  FACSIMILE   │             │ 1:1 SANDWICH │             │   TEI-P5     │
│   TYPESET    │             │   SCAN-PDF   │             │  XML-EDITION │
│ 1:1 Parity   │             │ Margin-Mask  │             │   RelaxNG    │
└──────────────┘             └──────────────┘             └──────────────┘
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│  BOOK TYPESET│             │   EPUB 3     │             │  QA-VIEWER   │
│ EDITION (v2) │             │  E-READER    │             │   Payer-UI   │
│ Reflowable B5│             │ Font-Embed   │             │  Split-Pane  │
└──────────────┘             └──────────────┘             └──────────────┘
```

---

## 📄 Detailed Artifact Description

### 1. Dense Facsimile Edition (1:1 Page Parity)
* **Filename:** `boethlingk1887_facsimile_dense.pdf` (8.58 MB · 484 pages)
* **What is it?**  
  A modern vector typeset edition (ISO B5) with **strict 1:1 page parity** against the historical 1887 Leipzig print by Haessel. Every text page (pp. 1–476) starts and ends on the exact same sūtras as Böhtlingk's original (0 overflow pages).
* **Key Features:**
  * **Typography:** Set in *STIX Two Text* combined with *Noto Serif Devanagari*. Provides native, handcrafted OpenType small caps for all IAST diacritics (**PĀṆINI**, **MAHĀBHĀṢYA**, **BHAṬṬOJI DĪKṢITA**).
  * **Adaptive Typography:** A 6-tier density engine dynamically scales font sizes and leading, ensuring light pages fill the type area elegantly while dense pages (such as p. 8) fit without page breaks.
  * **Śiva-Sūtras:** Page 1 presents the 14 canonical sound groups in a spacious 2-column layout.
  * **Navigation:** Reconstructed original running headers, outer margin reference numbers, 48 hierarchical PDF bookmarks, and native roman/arabic page labels.
* **Intended Audience:** Indologists and Sanskrit scholars requiring exact citation parity without dealing with scan noise.
* **Download:** [Release Asset](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf)

---

### 2. Modernized Book Typeset Edition
* **Filename:** `boethlingk1887_typeset_edition.pdf` (8.81 MB · 512 pages)
* **What is it?**  
  A typographically modernized book edition in ISO B5 format, free from 19th-century line and page constraints.
* **Key Features:** Generous line spacing, clear visual hierarchy between sūtra header, IAST transliteration, German translation, and commentary.
* **Intended Audience:** Scholars and students engaging in continuous reading and linguistic study of the Aṣṭādhyāyī.
* **Download:** [Release Asset](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf)

---

### 3. Cleaned 1:1 Sandwich PDF (Scan Facsimile)
* **Filename:** `boehtlingk1887.perfect_sandwich.pdf` / `boehtlingk1887_sandwich.pdf` (248.8 MB · 478 pages)
* **What is it?**  
  High-resolution Heidelberg University Library scans paired with an invisible, geometrically aligned OCR vector text layer.
* **Key Features:**
  * **Content-Aware Margin Masking:** Page margins, gutters, and scanner shadows neutralized (`#f0e8d6`) without altering the historical print area.
  * **Invisible Text Layer:** 14,267 text blocks on exact pixel coordinates (PDF Rendering Mode 3) for search, highlight, and copy-paste.
  * **Bookmarks:** 42 hierarchical PDF bookmarks covering all adhyāyas and pādas.
* **Intended Audience:** Archivists and philologists verifying original 1887 print layout and physical details.
* **Download:** [Release Asset (249 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf)

---

### 4. Canonical Master Dataset (JSON)
* **Filename:** `data/ashtadhyayi_complete_boethlingk1887.json` (2.85 MB)
* **What is it?**  
  The structured *Single Source of Truth* of the edition, containing all 3,997 sūtras (14 Śiva-Sūtras + 3,983 Aṣṭādhyāyī-Sūtras) fully validated with 0 duplicates and 0 gaps.
* **Fields per Sūtra:**
  * Canonical reference (`ref`, e.g. `"1.1.1"`), adhyāya, pāda, and sūtra number.
  * Devanāgarī (`canonical_devanagari`) and IAST transliteration (`canonical_iast`).
  * German translation (`translation`) and philological commentary (`commentary`).
  * Historical book page mapping (`page`).
* **Intended Audience:** NLP developers, computational linguists, and dictionary projects.
* **Download:** [Release Asset (2.85 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/ashtadhyayi_complete_boethlingk1887.json)
* **Source:** [View on GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

---

### 5. Schema-Valid TEI-P5 XML Edition
* **Filename:** `data/tei/boehtlingk1887_p5.xml` (2.90 MB)
* **What is it?**  
  Complete XML encoding conforming to the *Text Encoding Initiative* (TEI-P5) guidelines, 100% valid against `schemas/tei_all.rng`.
* **Key Features:**
  * Sūtra entries marked up as `<entry>`.
  * 478 `<pb>` page break tags linking to Heidelberg University IIIF images.
  * Böhtlingk's original corrigenda (pp. 477–480) structured in `<back>`.
* **Intended Audience:** Academic repositories and digital humanities collections.
* **Source:** [View on GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml)

---

### 6. Reflowable EPUB 3 eBook
* **Filename:** `boethlingk1887.epub` (1.47 MB)
* **What is it?**  
  Standardized EPUB 3 eBook for mobile reading.
* **Key Features:** Embedded *Noto Serif Devanagari* font for proper rendering of complex ligatures and IAST diacritics on mobile e-readers (Apple Books, Tolino, Kobo).
* **Download:** [Release Asset](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub)

---

### 7. Standalone QA Viewer
* **Filename:** `viewer.html` (39 KB)
* **What is it?**  
  A browser-based split-pane editor conforming to the Payer standard for direct local proofreading via the File System Access API.
* **Source:** [View on GitHub](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)

---

## 📊 Summary Artifact Matrix

| Artifact | Primary File | Format | Size | Main Purpose | Download / Access |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dense Facsimile** | `boethlingk1887_facsimile_dense.pdf` | PDF (Vector) | 8.58 MB (484 pp.) | 1:1 Citation Parity (STIX Two Text) | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf) |
| **Book Typeset** | `boethlingk1887_typeset_edition.pdf` | PDF (Vector) | 8.81 MB (512 pp.) | Continuous Reading Layout | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf) |
| **1:1 Sandwich PDF** | `boehtlingk1887_sandwich.pdf` | PDF (Scan+OCR) | 248.8 MB (478 pp.) | Historical Facsimile Verification | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) |
| **Master Dataset** | `ashtadhyayi_complete_boethlingk1887.json` | JSON | 2.85 MB (3,997 sūtras) | Single Source of Truth / NLP | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/ashtadhyayi_complete_boethlingk1887.json) |
| **TEI-P5 Edition** | `boehtlingk1887_p5.xml` | XML (TEI-P5) | 2.90 MB | Digital Humanities / Archive | [GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) |
| **EPUB 3 eBook** | `boethlingk1887.epub` | EPUB 3 | 1.47 MB | Mobile Reading (E-Reader) | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) |
| **QA Viewer** | `viewer.html` | HTML5 / JS | 39 KB | Local Visual Correction | [Viewer](https://github.com/birchville-org/boethlingk/blob/main/viewer.html) |
