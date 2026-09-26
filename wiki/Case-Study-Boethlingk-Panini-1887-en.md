> 🌐 **Language / Sprache:** [🇬🇧 English](Case-Study-Boethlingk-Panini-1887-en) | [🇩🇪 Deutsch](Case-Study-Boethlingk-Panini-1887)

# Case Study & Pipeline Documentation: Pāṇini's Grammar (Otto von Böhtlingk, 1887)

> **Complete historical digitization, canonical alignment, and generation of searchable sandwich material for 3,997 Sūtras across 478 book pages.**
>
> *This project serves as a reference case study for the book digitization pipeline [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich).*

---

## 1. Objective & Problem Statement

### 1.1 The Source Work
Otto von Böhtlingk's edition *Pâṇini's Grammatik, herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen* (Leipzig, H. Haessel, 1887) is the globally authoritative philological reference work for the ancient Indian grammatical system of the Aṣṭādhyāyī.

### 1.2 Philological & Typographical Challenges
The volume unites three disparate writing systems and languages in dense proximity:
1. **Sanskrit in Devanāgarī:** Complex 19th-century lead type with historical ligatures, conjuncts, semi-vowels, and virāmas.
2. **German in Historical Antiqua:** Academic translation and grammatical commentary with period-specific typography.
3. **Scholarly Transliteration (IAST):** Latin script with extensive combined diacritics (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ḹ`, `ṃ`, `ḥ`, `ṅ`, `ñ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`) and accent marks (Udātta, Svarita).

Traditional local OCR engines (Tesseract, Kraken, ABBYY) degrade severely on this multi-script layout, exhibiting high character error rates and script confusion.

### 1.3 Digitization Targets
The goal of this project is to produce a multi-layer, archival-grade digital edition:
1. **1:1 Sandwich PDF:** Untouched, high-resolution original scans from Heidelberg University Library (pixel-accurate preservation) layered over an invisible, geometrically precise, searchable text layer.
2. **Structured Single Source of Truth (Master JSON):** Complete, gapless decomposition of the work into structured Sūtra objects (Sūtra number, canonical Devanāgarī, IAST, German translation, philological commentary, book page mapping).
3. **Standalone QA Viewer:** A lightweight web application following the *Payer Global Web Editor Standard* for visual verification and correction, featuring split-pane views, zooming, and silent auto-repair.
4. **TEI-XML Edition:** A standardized TEI-P5 corpus for digital humanities research and long-term preservation.

---

## 2. Implemented End-to-End Pipeline

```text
[Heidelberg University Library Facsimiles] 
       │ (Book pages 1 to 478, JPG)
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
       │                           ├── SequenceMatcher comparison against data/sutras.json
       │                           ├── 4-Pāda-per-Adhyāya state machine
       │                           └── Colophon and noise filtering
       ▼
[Stage 4: Consolidation] ──────► data/ashtadhyayi_complete_boethlingk1887.json
       │                           (3,997 Sūtras = 100.0% coverage & 0 duplicates)
       ▼
[Stage 5: Interactive QA Viewer] ► viewer.html (Split-pane, Zoom/Pan, Silent Auto-Repair)
```

---

## 3. Detailed Implementation Stages

### Stage 1: Primary Source Ingestion & Caching
* **Source:** Digital facsimiles from Heidelberg University Library (*Bibliotheca Palatina*, `boehtlingk1887`).
* **Main Text Scope:** Book pages 1 through 478 (Page 1 = Śiva-Sūtras, Pages 2–476 = Aṣṭādhyāyī 1.1.1 to 8.4.68, Pages 477–478 = Corrigenda / Addenda).
* **Storage:** 484 scans cached locally at `data/img_cache/7_3A000000XXX_jpg_full_max_0_default_jpg.jpg`.

### Stage 2: Multimodal AI Recognition (`mistral-ocr-latest`)
* **Tool:** Official Mistral SDK utilizing `mistral-ocr-latest` (`scripts/mistral_ocr.py`).
* **Batch Orchestration:** `scripts/batch_ocr_runner.py` automates page range processing with skip-on-existing and cost tracking.
* **Generated Artifacts:**
  * `.mistral.md`: Semantically structured markdown containing header hierarchies and body prose.
  * `.mistral.json`: Detailed response containing page dimensions, text blocks, and bounding-box coordinates for sandwich PDF layer alignment.
* **Cost:** 478 pages x $0.004 = exactly **$1.912** for the complete volume.

### Stage 3: Canonical Alignment & Heuristics (`scripts/align_mistral_sutras.py`)
Overcoming historical printing quirks, wear, and OCR misreadings required robust domain heuristics:
* **Fuzzy Canonical Matching:** When a detected Sūtra number drifts (e.g. OCR misinterprets the Devanāgarī numeral ८ as ६, yielding `६५` instead of `८५`), a `SequenceMatcher` algorithm compares the sanitized Devanāgarī line against the expected Sūtra from `data/sutras.json`. At similarity >= 0.45, the counter is corrected automatically.
* **Compensated Token Length:** Exceptionally long Sanskrit compounds (e.g. Sūtra 5.4.77 with 185 characters without a leading `#`) are recognized reliably as Sūtra headers via Danda patterns (`॥...॥`) up to 350 characters.
* **Pāda and Adhyāya Rollover:** Because the Aṣṭādhyāyī strictly consists of 8 Adhyāyas with exactly 4 Pādas each, the state machine automatically rolls over to the next Adhyāya after Pāda 4 (`state["adhyaya"] += 1, state["pada"] = 1`), even if the printed colophon was damaged or unrecognized.
* **Script Token Filtering:** Stray tokens (occasional Hebrew or Telugu glyphs generated from battered lead type) are purged before consolidation.
* **Corrigenda Isolation:** Text continuing after the final Sūtra 8.4.68 (`अ अ`) (Böhtlingk's *Nachträge und Verbesserungen*) is isolated and prevented from contaminating Sūtra 8.4.68's commentary.

---

## 4. Validation Results

All 8 Adhyāyas and the introductory Śiva-Sūtras were validated 1:1 against the canonical reference database:

| Section | Book Pages | Sūtras (Actual / Expected) | Duplicates | Missing Translations | Validation Status |
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
| **Total** | **478 Pages** | **3,997 / 3,997** | **0** | **0** | **100.0% Gapless** |

---

## 5. Sandwich PDF Assembly in AlexandriaSandwich

The complete sandwich PDF was compiled using [`scripts/build_sandwich_pdf.py`](https://github.com/marcodem/boethlingk/blob/main/scripts/build_sandwich_pdf.py):
* **Target File:** `data/output/boehtlingk1887_sandwich.pdf` (278.16 MB, 478 pages)
* **Visual Layer (Background):** 478 high-resolution primary scans from Heidelberg University Library embedded losslessly (1:1 pixel resolution).
* **Invisible Text Layer (Foreground):** PDF Text Rendering Mode 3 (*Neither fill nor stroke text*) with Unicode font mapping (*Arial Unicode* / *Identity-H*) places 14,267 text blocks at their exact bounding-box coordinates.
* **Hierarchical Table of Contents (Bookmarks):** All 8 Adhyāyas, 32 Pādas, Śiva-Sūtras, and addenda are embedded as interactive PDF bookmarks.
* **Result:** Readers experience the untouched visual historical 1887 facsimile, while text selection, search, and copy-paste (Devanāgarī, IAST, and German) access coordinates directly.

---

## 6. Scholarly TEI-P5 Edition

For archival preservation and digital humanities interoperability, a canonical XML edition was generated:
* **File:** `data/tei/boehtlingk1887_p5.xml` (2.90 MB)
* **Validation:** 100% schema-valid against TEI All RelaxNG (`schemas/tei_all.rng`).
* **Scope:** 3,997 `<tei:entry>` elements, 478 `<tei:pb>` page breaks linked directly to Heidelberg IIIF endpoints, 8 Adhyāya and 32 Pāda divisions, and 50 Corrigenda items in `<back>`.

---

## 7. QA Viewer (Payer Global Web Editor Standard)

For editorial proofing and local maintenance, [`viewer.html`](https://github.com/marcodem/boethlingk/blob/main/viewer.html) was implemented:
* **Split-Pane:** Left pane displays high-resolution facsimiles with smooth zoom/pan; right pane provides the Sūtra editor.
* **Snippet Toolbar:** Quick insertion for Dandas (`॥`, `।`, `ऽ`, `°`), IAST diacritics, and scholarly abbreviations (`∠±`, `∠_`, `v. l.`, `Kāç.`, `RV.`).
* **Silent Auto-Repair on Save:** On save (`⌘S`), pipes (`||`) silently convert to Dandas (`॥`), double whitespace normalizes, and stray symbols purge without intrusive alert modals (visual badge feedback: yellow = auto-repair, green = saved).
* **Local Storage & Export:** Revisions persist in browser local storage with direct file saving supported via the File System Access API (`showSaveFilePicker`).
