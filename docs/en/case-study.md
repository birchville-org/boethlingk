# The Böhtlingk Delta: Methodology & Rationale for a Dedicated Edition Project

> **Scholarly edition, canonical sūtra alignment, and 1:1 facsimile typesetting of Otto von Böhtlingk's *Pâṇini's Grammatik* (Leipzig 1887).**
>
> 🔗 **Project Repository:** [github.com/birchville-org/boethlingk](https://github.com/birchville-org/boethlingk)  
> 🔗 **Central Processing Pipeline:** [AlexandriaSandwich](https://birchville-org.github.io/AlexandriaSandwich/en/)  
> 📦 **All Downloads:** [Edition Artifacts & Downloads](artifacts.md)

---

## 1. Rationale for a Dedicated Edition Project

Why does a complex philological work such as Otto von Böhtlingk's *Pâṇini's Grammatik* (2nd edition, Leipzig 1887) require a dedicated edition project rather than a generic pass through the [AlexandriaSandwich](https://birchville-org.github.io/AlexandriaSandwich/en/) digitization pipeline?

AlexandriaSandwich is engineered as a universal, stateless processing engine: it converts historical scans into clean, searchable 1:1 sandwich PDFs and raw text layers. For landmark, multi-script reference works, however, pure generic automation reaches fundamental architectural limits.

The establishment of `boethlingk` as an **autonomous edition satellite project** rests on four core pillars:

### A. Protecting the Core Pipeline from the "Monolith Trap" (*YAGNI Principle*)
Attempting to hardcode the complex grammar rules of the Aṣṭādhyāyī (3,997 sūtras, 32 pādas, historical colophons, bilingual commentary apparatus) into AlexandriaSandwich would make the central platform bloated and unmaintainable. AlexandriaSandwich remains lean, robust, and universal for 90% of standard books, while all domain-specific philological logic resides cleanly inside the edition satellite.

### B. Preserving Historical 1:1 Citation Parity
Since 1887, global Sanskrit scholarship has cited Pāṇini using the page numbers of Haessel's Leipzig editio princeps ("Böhtlingk p. 42"). A standard reflowing typesetter breaks pages arbitrarily, destroying historical page citations. The `boethlingk` project guarantees **strict 1:1 page congruence across all 476 original pages** with 0 overflow pages through adaptive volumetric typography.

### C. Canonical Hierarchy vs. Generic Prose
Böhtlingk's grammar is not running narrative text, but a formal hierarchical rule system:
* 14 introductory Śiva-Sūtras (phonological matrix)
* 3,983 Aṣṭādhyāyī sūtras across 8 books (Adhyāyas) and 32 quarters (Pādas)
* Historical three-script typography (Devanāgarī, German Antiqua, IAST transliteration with Vedic accents)
* Corrigenda and appendices (pp. 477–480)

This architecture requires deterministic state machines and ground-truth validation far beyond standard OCR.

### D. Continuous Scholarly Curation & Versioning
A critical digital edition is not a one-off export, but a permanent research instrument. Textual nuances, Devanāgarī ligatures, and IAST diacritics must be collated, corrected, and versioned collaboratively via **Git branches and pull requests**.

---

## 2. Architecture: AlexandriaSandwich (Platform) vs. Böhtlingk (Edition)

The separation of concerns between the processing platform and the edition satellite is clearly delineated:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ALEXANDRIASANDWICH (GENERIC CORE PIPELINE)                 │
│  • IIIF scan ingestion (UB Heidelberg: boehtlingk1887)                 │
│  • Fold & margin cleaning / Content-Aware Margin Masking (#f0e8d6)     │
│  • Multimodal AI OCR (mistral-ocr-latest) & word bounding boxes        │
│  • Generic sandwich PDF layer assembly (invisible vector text)         │
│  🔗 Documentation: https://birchville-org.github.io/AlexandriaSandwich/│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Bounding boxes, layout & clean scans
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   THE BÖHTLINGK DELTA (EDITION LAYER)                  │
│  1. Canonical sūtra state machine (8 Adhyāyas / 32 Pādas / 3,997 s.)   │
│  2. Philological ground-truth alignment & compound segmentation        │
│  3. 1:1 Facsimile typeset with adaptive volumetric typography (Typst)  │
│  4. STIX Two Text font stack for native IAST small caps                │
│  5. Sūtra-level TEI-P5 XML modeling & browser-based QA viewer          │
└────────────────────────────────────────────────────────────────────────┘
```

> ℹ️ **Pipeline Documentation:**  
> All generic image optimization, OCR confidence thresholds, and sandwich assembly workflows are documented in the [AlexandriaSandwich Methodological Wiki](https://birchville-org.github.io/AlexandriaSandwich/en/WIKI_VERFAHREN/) and the [Triage & Economic Model](https://birchville-org.github.io/AlexandriaSandwich/en/EVOLUTION_WORKFLOW/#3-the-triage-economic-model-core-pipeline-vs-edition-satellites).

---

## 3. The Methodological Delta in Detail

The specific edition delta of `boethlingk` comprises 5 technical and philological breakthroughs:

### 3.1 Delta 1: Canonical Sūtra State Machine (`scripts/align_mistral_sutras.py`)
* **Deterministic Rollover:** The state machine enforces canonical pāda transitions (`adhyaya += 1, pada = 1`), even when historical colophons in the scan are degraded or missing.
* **Corrigenda Isolation:** Böhtlingk's additions and corrections (pp. 477–480) following the concluding sūtra 8.4.68 (`अ अ`) are isolated and prevented from polluting the preceding commentary.

### 3.2 Delta 2: Fuzzy Ground-Truth Matching & Compound Splitting
* **Numeral Disambiguation:** Historical lead-type Devanāgarī numerals are frequently confused by OCR models (e.g. ۸ vs. ६). The matcher resolves discrepancies against the canonical Aṣṭādhyāyī database (threshold >= 0.45), restoring correct sūtra counts automatically.
* **Compound Recognition:** Overlong sūtras without markdown headings (up to 350 characters, e.g. 5.4.77) are parsed via danda boundaries (`॥...॥`) and separated cleanly from the German translation.

### 3.3 Delta 3: Adaptive Volumetric Typography (`boethlingk1887_facsimile_dense.typ`)
Rather than reducing font sizes across the whole book, a 6-tier typographic engine ([`data/calibrated_dense_profiles.json`](https://github.com/birchville-org/boethlingk/blob/main/data/calibrated_dense_profiles.json)) adaptively regulates font sizes and leading:

| Level | Pages | Devanāgarī | Translation / Leading | Commentary / Leading | Sūtra Spacing | Typical Page Characteristics |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **5** | 6 | 11.8 pt | 9.6 pt / 0.45em | 8.4 pt / 0.42em | 0.95em | 1–4 short sūtras, minimal text |
| **4** | 102 | 11.4 pt | 9.3 pt / 0.42em | 8.1 pt / 0.38em | 0.70em | 3–6 sūtras (e.g. p. 8), medium text |
| **3** | 239 | 10.8 pt | 8.9 pt / 0.37em | 7.7 pt / 0.32em | 0.38em | 6–8 sūtras, standard density (~50%) |
| **2** | 95 | 10.4 pt | 8.6 pt / 0.33em | 7.4 pt / 0.27em | 0.20em | 8–10 sūtras, text-heavy |
| **1** | 31 | 10.0 pt | 8.4 pt / 0.30em | 7.2 pt / 0.25em | 0.12em | 10–12 sūtras (e.g. pp. 3, 70, 378) |
| **0** | 2 | 9.6 pt | 8.1 pt / 0.26em | 6.9 pt / 0.23em | 0.06em | Extreme pages 282 & 286 (11 dense sūtras) |

* **Result:** Over 73% of all pages enjoy high typographic comfort (Levels 3–5). The type area is fully utilized, producing **exactly 0 overflow pages across all 476 original pages**.
* **Opening Tableau (Page 1):** The 14 Śiva-Sūtras are set in a balanced two-column tableau with Devanāgarī and italic IAST transliteration, followed by Böhtlingk's authentic introduction.

### 3.4 Delta 4: STIX Two Text Font Stack for Native IAST Small Caps
Standard serifs (such as *Libertinus Serif*) provide OpenType `smcp` only for basic Latin characters. Extended IAST glyphs (`ā`, `ī`, `ū`, `ṛ`, `ṣ`, `ś`, `ṇ`, `ṃ`, `ḥ`) fail and fall back to minuscules (**PĀṇINI**).
* `boethlingk` standardizes on **STIX Two Text** + **Noto Serif Devanagari**.
* Delivers genuine, optically balanced small caps for all scholarly Indological diacritics (**PĀṆINI**, **MAHĀBHĀṢYA**, **BHAṬṬOJI DĪKṢITA**).

### 3.5 Delta 5: Structured Philological Editions & Standalone QA Viewer
* **Master Dataset:** [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) as single source of truth (3,997 sūtra objects).
* **TEI-P5 XML:** [`data/tei/boehtlingk1887_p5.xml`](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) (100% valid against TEI All RelaxNG) with 478 `<pb>` tags linked to Heidelberg IIIF manifests.
* **QA Viewer ([`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)):** Browser-based split-pane editor featuring IIIF facsimile on the left, editable sūtra fields on the right, and silent auto-repair on save via the File System Access API.

---

## 4. Validation Results

All 8 Adhyāyas and the opening Śiva-Sūtras are validated 1:1 against the canonical reference database:

| Section | Book Pages | Sūtras (Actual / Expected) | Duplicates | Gaps | Validation Status |
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
| **Total** | **478 Pages** | **3,997 / 3,997** | **0** | **0** | **100.0% Complete** |

---

## 5. Artifact Catalog & Downloads

For detailed format specifications and direct download links for all generated outputs:

👉 **[Go to Edition Artifacts & Downloads (artifacts.md)](artifacts.md)**  
👉 **[Official GitHub Releases Page (Latest)](https://github.com/birchville-org/boethlingk/releases/latest)**
