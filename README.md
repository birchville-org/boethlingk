# Pāṇini's Grammatik (Otto von Böhtlingk, Leipzig 1887)

Wissenschaftliche Digitalisierung, kanonisches Alignment, TEI-P5-Edition und 1:1 Sandwich-PDF der *Grammatik des Pāṇini* (Otto von Böhtlingk, 2. Auflage, Leipzig 1887).

Digitalisat-Vorlage: Universitätsbibliothek Heidelberg ([Bibliotheca Palatina](https://digi.ub.uni-heidelberg.de/diglit/boehtlingk1887)).

---

## 1. Ergebnisse & Artefakte

- **Kanonisch validierter Master-Datensatz (100,0 %):**
  - [`data/ashtadhyayi_complete_boethlingk1887.json`](data/ashtadhyayi_complete_boethlingk1887.json) (2,83 MB)
  - Enthält alle 14 Śiva-Sūtras sowie alle 3.983 Aṣṭādhyāyī-Sūtras (insgesamt 3.997 Sūtras).
  - Devanāgarī, wissenschaftliche IAST-Transliteration, deutsche Übersetzung und fortlaufender philologischer Kommentar.

- **Schema-valide TEI-P5 XML-Edition:**
  - [`data/tei/boehtlingk1887_p5.xml`](data/tei/boehtlingk1887_p5.xml) (2,90 MB)
  - 100 % valide gegen TEI All RelaxNG Schema ([`schemas/tei_all.rng`](schemas/tei_all.rng)).
  - 478 `<pb>`-Seitenumbrüche mit direkter Verknüpfung zu den IIIF-Vollbildern der UB Heidelberg.
  - 50 Corrigenda-Einträge der Seiten 477–478 in `<back>`.

- **Durchsuchbares 1:1 Sandwich-PDF:**
  - [`data/output/boehtlingk1887_sandwich.pdf`](data/output/boehtlingk1887_sandwich.pdf) (278,16 MB, 478 Seiten)
  - Hintergrund: Verlustfreie Originalscans (1:1 Pixelauflösung).
  - Vordergrund: Unsichtbare Vektor-Textebene (PDF Rendering Mode 3, Unicode / Arial Unicode) auf exakten Pixelkoordinaten.
  - 42 hierarchische PDF-Bookmarks (Śiva-Sūtras, 8 Adhyāyas, 32 Pādas, Nachträge).

- **Interaktiver QA-Viewer:**
  - [`viewer.html`](viewer.html): Split-Pane-Editor mit Faksimile-Zoom/Pan, Snippet-Toolbar und lokalem Silent Auto-Repair beim Speichern.

---

## 2. Pipeline-Skripte (`scripts/`)

| Skript | Beschreibung |
| :--- | :--- |
| [`scripts/mistral_ocr.py`](scripts/mistral_ocr.py) | Client für die Mistral OCR API (`mistral-ocr-latest`). |
| [`scripts/batch_ocr_runner.py`](scripts/batch_ocr_runner.py) | Batch-Runner für OCR-Erfassung über mehrere Seiten. |
| [`scripts/align_mistral_sutras.py`](scripts/align_mistral_sutras.py) | Kanonischer Abgleich der OCR-Ergebnisse gegen die Aṣṭādhyāyī-Referenzdatenbank. |
| [`scripts/generate_tei_p5.py`](scripts/generate_tei_p5.py) | Erzeugt die TEI-P5 XML-Edition und validiert sie gegen RelaxNG. |
| [`scripts/build_sandwich_pdf.py`](scripts/build_sandwich_pdf.py) | Assembliert das 1:1 Sandwich-PDF aus Faksimiles und OCR-Koordinatenblöcken. |

---

## 3. Ausführung

```bash
# TEI-P5 XML generieren und validieren
uv run --with lxml python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng

# 1:1 Sandwich-PDF kompilieren
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

---

## 4. Dokumentation

Die ausführliche wissenschaftliche Fallstudie und Verfahrensdokumentation befindet sich unter:
- [docs/Case-Study-Boethlingk-Panini-1887.md](docs/Case-Study-Boethlingk-Panini-1887.md)
