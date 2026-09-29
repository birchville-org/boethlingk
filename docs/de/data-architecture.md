# 🏛️ Datenarchitektur — boethlingk

> Dieses Dokument beschreibt die Verzeichnisstruktur, das Drei-Layer-Datenmodell und die Verarbeitungspipelines der Referenz-Fallstudie `boethlingk`.

---

## 1. Projekt- und Verzeichnisstruktur

```text
boethlingk/
├── data/
│   ├── ashtadhyayi_complete_boethlingk1887.json  # Kanonischer Master-Datensatz (Single Source of Truth, 3.997 Sūtras)
│   ├── ashtadhyayi_grouped_edition.json          # Für den Typst-Buchsatz vorformatierte Edition
│   ├── sutras.json                              # Kanonische Aṣṭādhyāyī-Referenzdatenbank
│   ├── shiva_sutras.json                        # 14 Śiva-Sūtras Referenz
│   ├── corrigenda.json                          # 50 Corrigenda-Einträge der Seiten 477–478
│   ├── mistral/                                 # 478 Seiten Mistral OCR Markdown (*.md) & Geometrie (*.json)
│   ├── tei/                                     # TEI-P5 XML-Master (boehtlingk1887_p5.xml)
│   ├── img_cache/                               # Lokaler Cache der 484 Heidelberger IIIF-Originalscans
│   └── output/                                  # Generierte Zielartefakte (Sandwich-PDF, Typst-PDF, EPUB)
│
├── docs/                                        # Zweisprachige MkDocs-Dokumentation
│   ├── de/                                      # Deutsche Dokumentation (Default)
│   └── en/                                      # Englische Dokumentation
│
├── schemas/                                     # RelaxNG Schema-Definitionen (tei_all.rng)
├── scripts/                                     # Automatisierungs- & Build-Skripte
│   ├── download_scans.py                        # Batch-Download der IIIF-Scans von UB Heidelberg
│   ├── mistral_ocr.py                           # Mistral OCR API-Client (mistral-ocr-latest)
│   ├── batch_ocr_runner.py                      # Multi-Seiten Orchestrierung für OCR
│   ├── align_mistral_sutras.py                  # Kanonisches Alignment & Fuzzy Matching
│   ├── build_sandwich_pdf.py                    # 1:1 Sandwich-PDF Assembler
│   ├── build_typeset_edition.py                 # Typst-Vektorbuchsatz-Compiler
│   ├── generate_tei_p5.py                       # TEI-P5 XML-Generator & RelaxNG-Validator
│   └── export_epub.py                           # Reflowable EPUB 3 E-Book Generator
│
├── viewer.html                                  # Autarker QA-Viewer (Payer Global Web Editor Standard)
├── viewer_screenshot.png                        # Benutzeroberflächen-Demonstration
└── mkdocs.yml                                   # Konfiguration der Dokumentationsseite
```

---

## 2. Das Drei-Layer-Datenmodell

```text
Layer 1 — Faksimile-Bildbasis
  Quelle:   IIIF Image API, Universitätsbibliothek Heidelberg
  URL:      https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/...
  Ablage:   data/img_cache/ (lokaler Cache zur schnellen Verarbeitung)
  Zweck:    Visuelle Hintergrundschicht im 1:1 Sandwich-PDF und Bildverankerung im TEI (<pb facs="..."/>)

Layer 2 — Multimodale KI-OCR & Layoutgeometrie
  Quelle:   Mistral OCR (Modell: mistral-ocr-latest)
  Ablage:   data/mistral/*.mistral.json & *.mistral.md
  Inhalt:   Wort-Bounding-Boxes mit DPI-Abmessungen, Hierarchien und semantisches Markdown
  Qualität: Vollständige Erkennung historischer Dreischriftigkeit (Devanāgarī, deutsche Antiqua, IAST)

Layer 3 — Kanonische Master-JSON & TEI-P5-XML-Edition
  Ablage:   data/ashtadhyayi_complete_boethlingk1887.json & data/tei/boehtlingk1887_p5.xml
  Inhalt:   Strukturierte Sūtra-Objekte mit kanonischer Devanāgarī, IAST, deutscher Übersetzung und Kommentar
  Status:   100,0 % lückenlos (3.997 Sūtras) und 100 % valide gegen TEI All RelaxNG
```

---

## 3. End-to-End Verarbeitungs-Pipeline

```text
[IIIF-Faksimiles UB Heidelberg]
       │
       ▼
[Stufe 1: Lokales Image Caching] ──► data/img_cache/*.jpg
       │
       ▼
[Stufe 2: Multimodale KI-OCR] ─────► data/mistral/ (*.md, *.json via mistral-ocr-latest)
       │
       ▼
[Stufe 3: Kanonisches Alignment] ──► scripts/align_mistral_sutras.py
       │                              (SequenceMatcher-Abgleich gegen data/sutras.json)
       ▼
[Stufe 4: Master-Konsolidierung] ──► data/ashtadhyayi_complete_boethlingk1887.json
       │                              (Single Source of Truth, 3.997 Sūtras)
       ▼
[Stufe 5: Multi-Artefakt-Build]
       ├── TEI-P5 XML:          data/tei/boehtlingk1887_p5.xml
       ├── 1:1 Sandwich-PDF:    data/output/boehtlingk1887_sandwich.pdf
       ├── Typst-Neuausgabe:    data/output/boethlingk1887_typeset_edition.pdf
       ├── Reflowable EPUB 3:   data/output/boethlingk1887.epub
       └── QA-Viewer:           viewer.html
```

---

## 4. Kennzahlen des Datenbestands

| Metrik | Wert | Bemerkung |
| :--- | :--- | :--- |
| **Erfasste Buchseiten** | 478 Seiten | S. 1 (Śiva-Sūtras), S. 2–476 (Aṣṭādhyāyī), S. 477–478 (Nachträge) |
| **Gesamte Sūtra-Zahl** | 3.997 Sūtras | 14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras (100,0 % lückenlos) |
| **Duplikate / Fehlstellen** | 0 / 0 | Vollständig abgeglichen gegen kanonischen Sūtrapāṭha |
| **Sandwich-PDF Textblöcke** | 14.267 Blöcke | Pixelgenaue unsichtbare Vektor-Textebene (PDF Render Mode 3) |
| **Typst-Buchumfang** | 737 Seiten | Neu gesetzter Vektorsatz in ISO B5 |
| **TEI-Validierung** | 0 Fehler | 100 % schema-konform gegen RelaxNG (`tei_all.rng`) |
| **OCR-Gesamtkosten** | 1,912 $ | 478 Seiten x 0,004 $ via Mistral AI API |
