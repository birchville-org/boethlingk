# The Böhtlingk Delta & Philological Case Study

> **Scholarly edition, canonical sūtra alignment, and typographical 1:1 facsimile typeset of Otto von Böhtlingk's *Pâṇini's Grammatik* (Leipzig 1887).**
>
> 🔗 **Project Repository:** [github.com/birchville-org/boethlingk](https://github.com/birchville-org/boethlingk)  
> 🔗 **Central Pipeline Engine:** [AlexandriaSandwich Pipeline Documentation](https://birchville-org.github.io/AlexandriaSandwich/en/WIKI_VERFAHREN/)  
> 📦 **All Downloads:** [Edition Artifacts & Downloads](artifacts.md)

---

## 1. Context & Scope Separation

Otto von Böhtlingk's monumental edition *Pâṇini's Grammatik* (2nd edition, Leipzig 1887, Verlag von H. Haessel) remains the world's authoritative philological reference work for the grammatical system of Pāṇini's Aṣṭādhyāyī. Across 478 printed pages, the work integrates three distinct writing systems:
1. **Sanskrit in Devanāgarī:** Historical 19th-century movable metal type with complex ligatures and virāmas.
2. **German in historical Antiqua:** Scholarly translation and grammatical commentary.
3. **IAST Transliteration:** Roman script with combined diacritics (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṃ`, `ḥ`, `ṅ`, `ñ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`) and Vedic accent marks.

> ℹ️ **Pipeline Demarcation:**  
> All generic steps of digitization, IIIF image caching, multimodal Document AI OCR (`mistral-ocr-latest`), Content-Aware Margin Masking (`#f0e8d6`), and 1:1 sandwich PDF assembly are handled by the parent **[AlexandriaSandwich Pipeline](https://birchville-org.github.io/AlexandriaSandwich/en/WIKI_VERFAHREN/)**.  
>  
> This document describes **strictly the specific edition delta** developed in the `boethlingk` project: canonical sūtra segmentation, philological correction, 1:1 page parity in vector typesetting, and TEI-P5 modeling.

---

## 2. Architecture: Pipeline vs. Edition Delta

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ALEXANDRIASANDWICH (GENERIC MAIN PIPELINE)                 │
│  • IIIF scan ingestion (UB Heidelberg: boehtlingk1887)                 │
│  • Multimodal AI OCR (mistral-ocr-latest) & bounding-box geometry     │
│  • Content-Aware Margin Masking (gutter & edge cleanup #f0e8d6)        │
│  • Sandwich PDF layer assembly (invisible vector text layer)           │
│  • Local VLM benchmarks & n8n workflow automation                      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Layout, geometry & clean scans
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   THE BÖHTLINGK DELTA (EDITION LAYER)                  │
│  • Delta 1: Canonical 8-Adhyāya state machine (align_mistral_sutras)   │
│  • Delta 2: Fuzzy SequenceMatcher against Aṣṭādhyāyī ground truth      │
│  • Delta 3: 1:1 Facsimile typeset with adaptive typography (Typst)     │
│  • Delta 4: STIX Two Text font stack for native IAST small caps        │
│  • Delta 5: Sūtra-level TEI-P5 XML & reflowable EPUB 3 serialization   │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 The Triage & Economic Model (Platform vs. Edition Satellites)

The architectural division between generic platform and specialized edition is both strategic and economically sound:
1. **Avoiding the Monolith Trap:** If `alex.birchville.org` attempted to incorporate bespoke parsers for singular monumental works (such as Böhtlingk's Pāṇini, the Rigveda, or multi-volume dictionaries), the core engine would become fragile and unmaintainable.
2. **Economic Triage:** For 80–90% of standard books, AlexandriaSandwich delivers searchable sandwich PDFs automatically at near-zero marginal cost.
3. **Decision Fork on Sub-Threshold Results:** When automated output is insufficient, a structured review takes place:
   * **Path A (Generic Bug):** The core pipeline is improved; all future scans benefit.
   * **Path B (Genuine Special Case):** Spin-off as a dedicated edition satellite (such as `boethlingk`), which consumes AlexandriaSandwich artifacts as its digital primary layer while handling domain-specific curation, 1:1 facsimile typesetting, and TEI-P5 modeling autonomously.
4. **Full Documentation:** See [AlexandriaSandwich Triage & Economic Model](https://birchville-org.github.io/AlexandriaSandwich/en/EVOLUTION_WORKFLOW/#3-the-triage-economic-model-core-pipeline-vs-edition-satellites).

---

## 3. The Böhtlingk Delta in Detail

### 3.1 Delta 1: Canonical Sūtra State Machine (`scripts/align_mistral_sutras.py`)
The work strictly adheres to the canonical structure of the Aṣṭādhyāyī:
* **Canonical Structure:** 8 Adhyāyas of exactly 4 Pādas each (32 Pādas total) comprising 3,983 Aṣṭādhyāyī sūtras plus 14 preceding Śiva-Sūtras (**3,997 sūtras total**).
* **Deterministic Rollover:** Upon reaching the end of a pāda, the state machine enforces the canonical transition (`state["adhyaya"] += 1, state["pada"] = 1`), even if historical colophons in the scan are degraded or missing.
* **Corrigenda Isolation:** Böhtlingk's additions and corrections (pp. 477–480) following the concluding sūtra 8.4.68 (`अ अ`) are isolated and indexed into a dedicated corrigenda dataset.

### 3.2 Delta 2: Fuzzy Canonical Matching Against Ground Truth
Due to aged and worn 19th-century lead types, OCR models occasionally misrecognized Devanāgarī digits:
* **SequenceMatcher Alignment:** When a sūtra number is ambiguous, the algorithm computes character-level similarity between the normalized Devanāgarī text and the expected sūtra from `data/sutras.json`.
* **Correction Threshold:** At similarity >= 0.45, sūtra counters are automatically realigned to canonical numbering.
* **Long Sanskrit Compounds:** Sūtras spanning up to 350 characters without markdown heading tokens (e.g. 5.4.77) are detected via danda boundaries (`॥...॥`) and separated cleanly from German translations.

### 3.3 Delta 3: 1:1 Facsimile Typeset with Adaptive Typography (`boethlingk1887_facsimile_dense.typ`)
Unlike generic reflowable editions, this facsimile edition reconstructs the historical 1887 Leipzig layout with **strict 1:1 page parity**:
* **1:1 Page Parity:** Every original page (pp. 1–476) begins and ends on the exact same sūtras as Böhtlingk 1887 (**0 overflow pages** across 484 total pages). All historical page citations match directly.
* **Adaptive Typography (6-Tier Engine):** To prevent sparse pages from clustering at the top and dense pages from breaking over, a 6-tier profile (`scripts/prepare_facsimile_dense_data.py`) dynamically controls font size, leading, and sūtra spacing:
  * *Level 0 (Extreme density: only pp. 282 & 286 with 11 dense sūtras):* Body 8.1 pt, commentary 6.9 pt, spacing 0.06 em.
  * *Level 1 (High density: e.g. pp. 3, 70, 378 with 10–12 sūtras):* Body 8.4 pt, commentary 7.2 pt, spacing 0.12 em.
  * *Level 2 (Compact: text-heavy pages):* Body 8.6 pt, commentary 7.4 pt, spacing 0.20 em.
  * *Level 3 (Standard: 6–8 sūtras, ~50% of the book):* Body 8.9 pt, commentary 7.7 pt, spacing 0.38 em.
  * *Level 4 (Spacious comfort: e.g. p. 8 with 3–6 sūtras):* Body 9.3 pt, commentary 8.1 pt, spacing 0.70 em (generous leading, filling >80% of type area).
  * *Level 5 (Max comfort: 1–4 short sūtras):* Body 9.6 pt, commentary 8.4 pt, spacing 0.95 em.
* **Two-Column Śiva-Sūtra Tableau (Page 1):** The 14 opening canonical sound groups are arranged in a spacious, balanced two-column tableau with Devanāgarī (12.5 pt bold) and italic IAST transliteration.
* **Original Headers & Margins:** Reconstructed running headers (`I. Adhyāya. 1. Pāda.` / `1, 1, 7.`) and outer margin sūtra numbers.

### 3.4 Delta 4: STIX Two Text Font Stack for Native IAST Small Caps
Standard serif typefaces (such as *Libertinus Serif* or *Times*) implement OpenType `smcp` only for basic Latin characters. Extended IAST glyphs with diacritics (`ṇ`, `ṭ`, `ṣ`, `ṛ`) fail and fall back to lowercase minuscules (**PĀṇINI**).
* The edition standardizes on **STIX Two Text** + **Noto Serif Devanagari**.
* STIX Two Text provides complete, handcrafted OpenType small caps for all IAST characters (**PĀṆINI**, **MAHĀBHĀṢYA**, **BHAṬṬOJI DĪKṢITA**) with uniform stroke weight and optical balance.

### 3.5 Delta 5: Standardized TEI-P5 and EPUB 3 Serialization
* **TEI-P5 XML (`data/tei/boehtlingk1887_p5.xml`):** 100% valid against TEI All RelaxNG (`schemas/tei_all.rng`), encoding 3,997 `<tei:entry>` elements and 478 `<tei:pb>` page breaks linked to Heidelberg IIIF manifests.
* **EPUB 3 (`boethlingk1887.epub`):** Reflowable e-book with embedded fonts for reliable mobile reading.

---

## 4. Validation Results

All 8 Adhyāyas and the introductory Śiva-Sūtras were validated 1:1 against the canonical reference database:

| Section | Book Pages | Sūtras (Actual / Expected) | Duplicates | Missing | Validation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Śiva-Sūtrāṇi** | 1 | 14 / 14 | 0 | 0 | **100.0% validated** |
| **Adhyāya 1** | 2–43 | 351 / 351 | 0 | 0 | **100.0% validated** |
| **Adhyāya 2** | 43–75 | 268 / 268 | 0 | 0 | **100.0% validated** |
| **Adhyāya 3** | 75–148 | 631 / 631 | 0 | 0 | **100.0% validated** |
| **Adhyāya 4** | 149–221 | 635 / 635 | 0 | 0 | **100.0% validated** |
| **Adhyāya 5** | 221–282 | 555 / 555 | 0 | 0 | **100.0% validated** |
| **Adhyāya 6** | 283–374 | 736 / 736 | 0 | 0 | **100.0% validated** |
| **Adhyāya 7** | 375–428 | 438 / 438 | 0 | 0 | **100.0% validated** |
| **Adhyāya 8** | 429–478 | 369 / 369 | 0 | 0 | **100.0% validated** |
| **Total** | **478 Pages** | **3,997 / 3,997** | **0** | **0** | **100.0% complete** |

---

## 5. Artifact Directory & Downloads

For a complete catalog of all produced output files (facsimile typeset, book edition, sandwich PDF, master JSON, TEI-P5 XML, EPUB 3) with full descriptions and direct download links:

👉 **[Go to Edition Artifacts & Downloads (artifacts.md)](artifacts.md)**  
👉 **[Official GitHub Releases Page (Latest)](https://github.com/birchville-org/boethlingk/releases/latest)**
