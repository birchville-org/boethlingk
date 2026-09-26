# Pāṇini's Grammatik (Otto von Böhtlingk, Leipzig 1887)

Wissenschaftliche Digitalisierung, kanonisches Alignment, TEI-P5-Edition und 1:1 Sandwich-PDF der *Grammatik des Pāṇini* (Otto von Böhtlingk, 2. Auflage, Leipzig 1887).

Digitalisat-Vorlage: Universitätsbibliothek Heidelberg ([Bibliotheca Palatina](https://digi.ub.uni-heidelberg.de/diglit/boehtlingk1887)).

> ℹ️ **Hinweis:** Das Projekt `boethlingk` ist eine reale, vollständige Fallstudie (*Case Study*) zur Buch-Digitalisierungs-Pipeline [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich). Es demonstriert die automatisierte OCR-Verarbeitung historischer Dreischriftigkeit (Devanāgarī, Antiqua, IAST), kanonisches Alignment gegen Referenzdatenbanken sowie die Assemblierung von 1:1 Sandwich-PDFs und TEI-P5-XML-Editionen.

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

- **Durchsuchbares 1:1 Sandwich-PDF (278 MB, 478 Seiten):**
  - 📥 **Download:** [Release Asset (`boehtlingk1887_sandwich.pdf`)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf)
  - *(Hinweis: Da die PDF-Datei 278 MB umfasst, ist sie im Git-Repository ignoriert und wird über das GitHub-Release bereitgestellt oder kann lokal assembliert werden).*
  - Hintergrund: Verlustfreie Originalscans der UB Heidelberg (1:1 Pixelauflösung).
  - Vordergrund: Unsichtbare Vektor-Textebene (PDF Rendering Mode 3, Unicode / Arial Unicode) auf 14.267 Textblöcken.
  - 42 hierarchische PDF-Bookmarks (Śiva-Sūtras, 8 Adhyāyas, 32 Pādas, Nachträge).

- **Interaktiver QA-Viewer:**
  - [`viewer.html`](viewer.html): Split-Pane-Editor mit Faksimile-Zoom/Pan, Snippet-Toolbar und lokalem Silent Auto-Repair beim Speichern.

---

## 2. Schnelleinstieg: Nur die Daten nutzen

Für wissenschaftliche Analysen und Weiterverarbeitung sind die kuratierten Datensätze direkt ohne Pipeline-Ausführung nutzbar:

```python
import json

# Master-Datensatz einlesen (UTF-8)
with open("data/ashtadhyayi_complete_boethlingk1887.json", encoding="utf-8") as f:
    data = json.load(f)

shiva_sutras = data["shiva_sutras"]  # 14 Śiva-Sūtras
sutras = data["sutras"]              # 3.983 Aṣṭādhyāyī-Sūtras
print(f"Geladene Sūtras gesamt: {len(shiva_sutras) + len(sutras)}")  # 3997

# Erstes Aṣṭādhyāyī-Sūtra (1.1.1)
first_sutra = sutras[0]
print(f"Referenz:   {first_sutra['ref']}")
print(f"Devanāgarī: {first_sutra['canonical_devanagari']}")
print(f"IAST:       {first_sutra['canonical_iast']}")
print(f"Deutsch:    {first_sutra['translation']}")
print(f"Buchseite:  {first_sutra['page']}")
```

---

## 3. Installation & Voraussetzungen

- **Python:** `>= 3.12`
- **Paketmanager:** `uv` (empfohlen) oder Standard-`pip`

```bash
# Mit uv (automatische venv-Verwaltung):
uv sync

# Alternativ mit pip:
pip install -r requirements.txt
```

---

## 4. Pipeline: Von den Scans zum Ergebnis

Die vollständige Digitalisierungsstrecke gliedert sich in fünf aufeinander aufbauende Stufen:

```
[IIIF UB Heidelberg] ──> scripts/download_scans.py ──> [data/img_cache/]
                                                              │
[Mistral OCR API]    ──> scripts/batch_ocr_runner.py ──> [data/mistral/] (im Repo enthalten)
                                                              │
[Referenzdaten]      ──> scripts/align_mistral_sutras.py ──> [data/ashtadhyayi_complete_boethlingk1887.json]
                                                              │
                     ┌────────────────────────────────────────┴────────────────────────────────────────┐
                     ▼                                                                                 ▼
     scripts/generate_tei_p5.py                                                        scripts/build_sandwich_pdf.py
                     │                                                                                 │
                     ▼                                                                                 ▼
      [data/tei/boehtlingk1887_p5.xml]                                               [data/output/boehtlingk1887_sandwich.pdf]
```

### Schritt 1: Original-Scans herunterladen (IIIF)
Lädt die 478 Vollauflösungs-Faksimiles der UB Heidelberg in den lokalen Cache `data/img_cache/`:

```bash
python3 scripts/download_scans.py --start 1 --end 478 --concurrency 4
```

### Schritt 2: OCR-Extraktion (Optional)
> ℹ️ **Dieser Schritt ist optional!** Alle 478 OCR-Ergebnisse (JSON mit Bounding-Boxen und Markdown) sind bereits vollständig in [`data/mistral/`](data/mistral/) im Repository hinterlegt. Ein API-Key wird nur benötigt, wenn die OCR erneut über Mistral AI generiert werden soll.

```bash
# Nur nötig bei Neu-Generierung:
export MISTRAL_API_KEY="ihr_mistral_api_key"
python3 scripts/batch_ocr_runner.py 1 478
```

### Schritt 3: Kanonisches Alignment & Konsolidierung
Gleicht die OCR-Texte gegen die kanonische Sūtra-Referenzdatenbank ([`data/sutras.json`](data/sutras.json) und [`data/shiva_sutras.json`](data/shiva_sutras.json)) ab:

```bash
python3 scripts/align_mistral_sutras.py
```

### Schritt 4: TEI-P5 XML generieren und gegen RelaxNG validieren
Erstellt die TEI-P5-XML-Edition und validiert das Dokument automatisch gegen das TEI All RelaxNG Schema ([`schemas/tei_all.rng`](schemas/tei_all.rng)):

```bash
python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### Schritt 5: 1:1 Sandwich-PDF kompilieren
Kombiniert die Scans aus `data/img_cache/` mit den Bounding-Boxen aus `data/mistral/` zu einem durchsuchbaren Vektor-PDF:

```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

---

## 5. Externe Quellen & Lizenzen

- **Digitalisat & Primärquelle:** Otto von Böhtlingk, *Pâṇini's Grammatik*, 2. Auflage, Leipzig: Verlag von H. Haessel 1887. Gemeinfrei (Public Domain).
- **Faksimile-Vorlagen:** Universitätsbibliothek Heidelberg ([Bibliotheca Palatina](https://digi.ub.uni-heidelberg.de/diglit/boehtlingk1887)).
- **Englische Vergleichsausgabe (historische Referenz):** Srisa Chandra Vasu, *The Ashṭādhyāyī of Pāṇini*, Allahabad: The Panini Office 1891 (Bände I–VIII). Gemeinfrei (Public Domain).
- **Eigener Code & TEI-Encoding:** Lizenziert unter der [MIT-Lizenz](LICENSE).

---

## 6. Dokumentation & Wiki

- **Online-Dokumentation (GitHub Pages):** [birchville-org.github.io/boethlingk](https://birchville-org.github.io/boethlingk/)
  - Die Dateien unter [`docs/`](docs/) bilden den Quellbestand für MkDocs Material und die Web-Dokumentation.
- **GitHub Wiki:** [github.com/birchville-org/boethlingk/wiki](https://github.com/birchville-org/boethlingk/wiki)
  - Der Ordner [`wiki/`](wiki/) dient als lokaler Spiegel für das GitHub-Wiki-Repository.
  - 🇩🇪 [Startseite (DE)](https://github.com/birchville-org/boethlingk/wiki/Home) | [Wissenschaftliche Fallstudie (DE)](https://github.com/birchville-org/boethlingk/wiki/Case-Study-Boethlingk-Panini-1887)
  - 🇬🇧 [Home (EN)](https://github.com/birchville-org/boethlingk/wiki/Home-en) | [Scholarly Case Study (EN)](https://github.com/birchville-org/boethlingk/wiki/Case-Study-Boethlingk-Panini-1887-en)
