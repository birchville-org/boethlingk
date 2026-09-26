# Welcome to the Böhtlingk Pāṇini Project Wiki

> ℹ️ **Case Study:** The `boethlingk` project is a comprehensive reference case study for the book digitization pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**. It demonstrates OCR processing of complex multi-script typography, canonical alignment, and the production of 1:1 sandwich PDFs and TEI-P5 XML editions.

This wiki documents the scholarly preservation, complete AI OCR digitization, canonical consolidation, and digital edition of **Otto von Böhtlingk's Pâṇini's Grammatik (Leipzig 1887)** based on facsimiles from Heidelberg University Library.

---

## 📖 Core Documentation

👉 **[[Scholarly Case Study: Complete Digitization, TEI-P5 Edition & 1:1 Sandwich PDF|Case-Study-Boethlingk-Panini-1887-en]]**

The comprehensive documentation covers:
1. **Initial Situation & Problem Statement:** Limits of previous Tesseract OCR PDFs on multi-script layouts (Devanāgarī, Antiqua, IAST).
2. **The Implemented Solution:** Complete AI capture of all 478 book pages with `mistral-ocr-latest`.
3. **Canonical Alignment:** Gapless matching against the Aṣṭādhyāyī Sūtrapāṭha (3,997 Sūtras, 0 duplicates, 0 gaps).
4. **The 1:1 Sandwich PDF:** Lossless image reproduction with an invisible vector text layer (PDF Text Render Mode 3).
5. **Scholarly TEI-P5 Edition:** 100% schema-valid XML edition with direct IIIF facsimile links.
6. **QA Viewer:** Web-based split-pane editor with facsimile zoom and silent auto-repair on save.

---

## 🚀 Quick Access to Project Artifacts

| Artifact | Repository Path | Description |
| :--- | :--- | :--- |
| **TEI-P5 XML** | [`data/tei/boehtlingk1887_p5.xml`](https://github.com/marcodem/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) | Schema-valid archival preservation edition |
| **Sandwich PDF** | `data/output/boehtlingk1887_sandwich.pdf` | Searchable 1:1 Sandwich PDF (278 MB, 478 pages) |
| **Master Dataset** | [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/marcodem/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) | Structured JSON dataset covering all 3,997 Sūtras |
| **QA Viewer** | [`viewer.html`](https://github.com/marcodem/boethlingk/blob/main/viewer.html) | Standalone split-pane editor conforming to Payer Standard |
| **Code Repository** | [marcodem/boethlingk](https://github.com/marcodem/boethlingk) | Complete pipeline scripts and documentation |
