# 📖 Pāṇinis Grammatik (Otto von Böhtlingk, Leipzig 1887)

> **Wissenschaftliche Digitalisierung, kanonisches Alignment, TEI-P5-Edition und 1:1 Sandwich-PDF der *Grammatik des Pāṇini* (Otto von Böhtlingk, 2. Auflage, Leipzig 1887).**

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![TEI P5](https://img.shields.io/badge/TEI--P5-RelaxNG%20valid-green)
![Sandwich PDF](https://img.shields.io/badge/PDF-1%3A1%20Sandwich-orange)
![Alignment](https://img.shields.io/badge/Sūtras-3.997%20(100%25)-brightgreen)

> ℹ️ **Case Study:** Dieses Projekt ist eine Referenz-Fallstudie zur Open-Source-Digitalisierungs-Pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**.

Dieses Projekt umfasst die vollständige historische Erschließung, multimodale KI-Vollerfassung (Mistral OCR), das lückenlose kanonische Alignment gegen den Aṣṭādhyāyī Sūtrapāṭha sowie die Erstellung standardkonformer digitaler Editionsartefakte für Otto von Böhtlingks maßgebliche Pāṇini-Ausgabe von 1887 auf Basis der Digitalisate der Universitätsbibliothek Heidelberg.

---

## ✨ Projektergebnisse & Kernartefakte

1. **Kanonisch validierter Master-Datensatz (100,0 %):**
   * Datei: [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) (2,83 MB)
   * 3.997 Sūtras lückenlos (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras, 0 Duplikate, 0 Fehlstellen).
   * Enthält Devanāgarī, wissenschaftliche IAST-Transliteration, deutsche Übersetzung und fortlaufenden Kommentar.

2. **Schema-valide TEI-P5 XML-Edition:**
   * Datei: [`data/tei/boehtlingk1887_p5.xml`](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) (2,90 MB)
   * 100 % valide gegen das offizielle TEI All RelaxNG Schema (`schemas/tei_all.rng`).
   * 478 `<pb>`-Seitenumbrüche mit direkter Verknüpfung zu den IIIF-Vollbildern der UB Heidelberg.
   * 50 Corrigenda-Einträge der Seiten 477–478 in `<back>`.

3. **Durchsuchbares 1:1 Sandwich-PDF:**
   * Datei: `data/output/boehtlingk1887_sandwich.pdf` (278,16 MB, 478 Seiten)
   * Visuell: Unverändertes Originalscan-Faksimile (1:1 Pixelauflösung).
   * Textebene: Unsichtbare Vektor-Textebene (PDF Rendering Mode 3) mit 14.267 Textblöcken auf exakten Pixelkoordinaten.
   * 42 hierarchische PDF-Bookmarks (Śiva-Sūtras, 8 Adhyāyas, 32 Pādas, Nachträge).

4. **Autarker QA-Viewer:**
   * Datei: [`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)
   * Split-Pane-Editor nach Payer-Standard mit Faksimile-Zoom/Pan, Snippet-Toolbar und lokalem Silent Auto-Repair beim Speichern.

---

## 🏛️ Pipeline-Architektur

```text
[UB Heidelberg Faksimiles] 
       │ (Buchseiten 1 bis 478, JPG)
       ▼
[Schritt 1: Lokales Image Caching] ──► data/img_cache/7_3A000000XXX_...jpg
       │
       ▼
[Schritt 2: Multimodale KI-OCR] ────► mistral-ocr-latest (Mistral Python SDK)
       │                              ├── data/mistral/*.mistral.md   (Layout-Markdown)
       │                              └── data/mistral/*.mistral.json (Bounding-Box Geometrie)
       ▼
[Schritt 3: Kanonisches Alignment] ──► scripts/align_mistral_sutras.py
       │                              ├── Heuristische Sūtra-Segmentierung (#, ##, ॥...॥)
       │                              ├── SequenceMatcher-Abgleich gegen data/sutras.json
       │                              ├── 4-Pāda-pro-Adhyāya Statusmaschine
       │                              └── Kolophon- und Rauschfilterung
       ▼
[Schritt 4: Konsolidierung] ─────────► data/ashtadhyayi_complete_boethlingk1887.json
       │                              (3.997 Sūtras = 100,0 % lückenlos & 0 Duplikate)
       ▼
[Schritt 5: TEI- & PDF-Assembly] ────► data/tei/boehtlingk1887_p5.xml
                                      data/output/boehtlingk1887_sandwich.pdf
```

---

## 🚀 Schnellstart

### TEI-P5 XML generieren und validieren
```bash
uv run --with lxml python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### 1:1 Sandwich-PDF kompilieren
```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

---

## 📖 Dokumentationsübersicht

* [Wissenschaftliche Fallstudie (Verfahrensdokumentation)](case-study.md)
* [Datenarchitektur & Drei-Layer-Modell](data-architecture.md)
* [Pipeline-Entscheidungen](pipeline-decisions.md)
* [Konventionen & IIIF-Spezifikation](conventions.md)
* [Wiki-Übersicht](wiki-home.md)
