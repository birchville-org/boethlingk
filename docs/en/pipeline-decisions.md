# Pipeline Decisions — boethlingk

## 1. IIIF-First Strategy: External Image Source
* **Decision:** Scans originate directly from Heidelberg University Library's stable IIIF Image API server (877 pages).
* **Rationale:** Direct URL referencing avoids multi-gigabyte repository bloat while providing arbitrary on-demand zoom and crop coordinates for TEI `<pb facs="..."/>` and QA viewing.

## 2. Multimodal AI OCR (`mistral-ocr-latest`) over Traditional Engines
* **Decision:** Replace classical engines (Tesseract, Kraken) with Mistral OCR API (`mistral-ocr-latest`).
* **Rationale:** Historical 1887 typography mixes Devanāgarī, German Antiqua, and academic IAST transliteration with accents. Tesseract and standard OCR produce unusable gibberish on mixed scripts, whereas Mistral OCR achieved full character and layout fidelity at minimal cost ($1.912 total).

## 3. Canonical Alignment via SequenceMatcher & State Machine
* **Decision:** Enforce automatic canonical validation against the Aṣṭādhyāyī Sūtrapāṭha database (`data/sutras.json`).
* **Rationale:** Scan artifacts and historical print wear cause numeral misreadings. Fuzzy matching (similarity threshold >= 0.45) and strict 4-Pāda-per-Adhyāya state rollover guaranteed 100.0% gapless Sūtra coverage (3,997 / 3,997) with 0 duplicates.

## 4. 1:1 Sandwich PDF Assembly (AlexandriaSandwich Standard)
* **Decision:** Produce a 1:1 archival Sandwich PDF where original high-resolution facsimiles serve as the visual background, layered with an invisible vector font layer (PDF Rendering Mode 3).
* **Rationale:** Preserves historical authenticity down to the pixel while enabling instant text selection, search, and copy-paste in standard PDF readers.

## 5. Formal TEI-P5 XML Edition
* **Decision:** Generate an XML edition validated against TEI All RelaxNG (`schemas/tei_all.rng`).
* **Rationale:** Guarantees digital humanities interoperability, persistent citation integrity, and long-term digital preservation.
