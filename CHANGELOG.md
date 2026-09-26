# 📓 Changelog: Pāṇini's Grammatik (Böhtlingk 1887)

Alle wesentlichen Änderungen und Meilensteine dieses Projekts werden in dieser Datei dokumentiert.

## [1.0.0] - 2026-09-26

### Added
* **Kanonischer Master-Datensatz (100,0 % Abdeckung):**
  * `data/ashtadhyayi_complete_boethlingk1887.json` (2,83 MB) mit allen 3.997 Sūtras (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras).
  * 0 Duplikate, 0 Fehlstellen; vollständige Erfassung von Devanāgarī, wissenschaftlicher IAST-Transliteration, deutscher Übersetzung und fortlaufendem philologischem Kommentar.
* **Schema-valide TEI-P5 XML-Edition:**
  * `data/tei/boehtlingk1887_p5.xml` (2,90 MB), 100 % valide gegen TEI All RelaxNG (`schemas/tei_all.rng`).
  * 478 `<pb>`-Seitenumbrüche mit direkter IIIF-Faksimile-Verknüpfung zur UB Heidelberg.
  * 50 Corrigenda-Einträge der Seiten 477–478 im `<back>`-Bereich strukturiert eingebunden.
* **Durchsuchbares 1:1 Sandwich-PDF:**
  * `data/output/boehtlingk1887_sandwich.pdf` (278,16 MB, 478 Seiten).
  * Pixelgenaue Erhaltung der Heidelberger Primärscans (1:1 Bildebene) mit unsichtbarer Vektor-Textebene (PDF Render Mode 3, Arial Unicode / Identity-H).
  * 14.267 Textblöcke auf exakten Pixelkoordinaten sowie 42 hierarchische PDF-Bookmarks (Śiva-Sūtras, 8 Adhyāyas, 32 Pādas, Nachträge).
* **Autarker QA-Viewer (`viewer.html`):**
  * Webbasierter Split-Pane-Editor nach Payer Global Web Editor Standard.
  * Faksimile-Zoom und Pan, Snippet-Toolbar für Dandas und IAST-Diakritika, lokaler Export via File System Access API und Silent Auto-Repair beim Speichern.
* **Multimodale KI-Pipeline & Alignment:**
  * Mistral OCR Client (`scripts/mistral_ocr.py`) und Batch-Runner (`scripts/batch_ocr_runner.py`) für `mistral-ocr-latest`.
  * Kanonisches Alignment (`scripts/align_mistral_sutras.py`) mit Fuzzy SequenceMatcher und 4-Pāda-Statusmaschine.
  * PDF-Assembler (`scripts/build_sandwich_pdf.py`) und TEI-Generator (`scripts/generate_tei_p5.py`).
* **Zweisprachige Dokumentation & Wiki (DE & EN):**
  * Strukturierte Dokumentation unter `docs/de/` und `docs/en/`.
  * MkDocs-Material-Setup (`mkdocs.yml`) mit `mkdocs-static-i18n` und GitHub Pages Deployment (`.github/workflows/docs.yml`).
  * Zweisprachiges GitHub Wiki (`wiki/`) mit nativer Seitenleisten-Navigation.
  * Ausführliche wissenschaftliche Fallstudie zur Referenz-Pipeline [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich).
