> 🌐 **Sprache / Language:** [🇩🇪 Deutsch](QA-and-Correction-Workflow) | [🇬🇧 English](QA-and-Correction-Workflow-en)

# 🛠️ QA- & Korrektur-Workflow

Dieser Leitfaden beschreibt, wie OCR-Leseungenauigkeiten, Tippfehler in Kommentaren oder diakritische Korrekturen im Projekt `boethlingk` kollationiert, korrigiert und synchron in alle digitalen Editions-Artefakte (Typst-Buch-PDF, TEI-P5-XML und Sandwich-PDF) übernommen werden.

---

## 🏛️ Das Architekturprinzip: Single Source of Truth

Alle Korrekturen erfolgen **ausschließlich an einer einzigen zentralen Stelle**:
👉 [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

Manuelle Änderungen in generierten Ausgabedateien (wie XML oder PDF) sind strikt zu vermeiden, da diese Dateien bei jedem Build-Lauf automatisiert und deterministisch überschrieben werden.

```text
                               ┌────────────────────────┐
                               │     Korrektur in       │
                               │   Master-JSON-Datei    │
                               └───────────┬────────────┘
                                           │
                     ┌─────────────────────┼─────────────────────┐
                     ▼                     ▼                     ▼
        scripts/build_typeset_edition.py   │          scripts/generate_tei_p5.py
                     │                     │                     │
                     ▼                     │                     ▼
        [boethlingk1887_typeset.pdf]       │           [boehtlingk1887_p5.xml]
              (Modernes Buch-PDF)          │            (Archiv-XML & RelaxNG)
                                           ▼
                              scripts/build_sandwich_pdf.py
                                           │
                                           ▼
                             [boehtlingk1887_sandwich.pdf]
                                  (1:1 Faksimile-PDF)
```

---

## 🔍 Weg 1: Visuelle Kollationierung mit dem QA-Viewer (Empfohlen)

Für den visuellen Abgleich von Text und Faksimile enthält das Repository den interaktiven Editor [`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html).

### 1. Lokalen Server starten
Aufgrund von Browser-Sicherheitsrichtlinien (CORS) bei lokalen Dateien starten Sie einen lokalen Webserver im Projektverzeichnis:
```bash
python3 -m http.server 8000
```
Öffnen Sie im Browser: `http://localhost:8000/viewer.html`

### 2. Bedienung & Editor-Funktionen
- **Linker Bereich (Faksimile-Inspektion):** Zeigt den hochauflösenden Scan der Universitätsbibliothek Heidelberg. Mit Mausrad / Touchpad zoomen und bei gedrückter Maustaste verschieben.
- **Rechter Bereich (Sūtra-Felder):** Die Daten des aktuellen Sūtras sind direkt editierbar:
  - `canonical_devanagari`: Devanāgarī-Sūtratext
  - `canonical_iast`: Wissenschaftliche Transliteration
  - `translation`: Deutsche Übersetzung von Otto Böhtlingk (1887)
  - `commentary`: Philologischer Kommentar und Belegstellen
- **Snippet-Toolbar:** Schaltflächen zum schnellen Einfügen von Dandas (`॥`) und IAST-Diakritika (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`, `ṃ`, `ḥ`).
- **Navigation:** Mit den Pfeiltasten oder den Schaltflächen *Vorheriges / Nächstes Sūtra* durch das Werk navigieren.

### 3. Speichern mit Silent Auto-Repair
- Drücken Sie `Cmd+S` (Mac) bzw. `Ctrl+S` (Windows/Linux) oder klicken Sie auf **„Speichern (JSON)“**.
- Der QA-Viewer führt ein unaufdringliches *Silent Auto-Repair* durch (Bereinigung von typografischen Fehlzeichen) und speichert den Datensatz direkt über die *File System Access API* in `data/ashtadhyayi_complete_boethlingk1887.json`.

---

## ⌨️ Weg 2: Gezielte Bearbeitung im Code-Editor

Wenn Ihnen die Sūtra-Nummer (z. B. `1.1.4`) oder eine konkrete Textstelle bereits bekannt ist:

1. Öffnen Sie `data/ashtadhyayi_complete_boethlingk1887.json` in VS Code oder Ihrem bevorzugten Editor.
2. Suchen Sie nach `"ref": "1.1.4"`.
3. Passen Sie die Werte direkt an:
   ```json
   {
     "ref": "1.1.4",
     "adhyaya": 1,
     "pada": 1,
     "sutra_num": 4,
     "page": 2,
     "canonical_devanagari": "न धातुलोप आर्धधातुके",
     "canonical_iast": "na dhātulopa ārdhadhātuke",
     "translation": "Wenn ein ārdhadhātuka genanntes Suffix...",
     "commentary": "Beispiele लोलुव, मरीमज..."
   }
   ```
4. Datei speichern.

---

## ⚡ Schritt 3: Ausgabe-Artefakte neu kompilieren

Nach dem Speichern der Korrektur führen Sie im Terminal die Build-Skripte aus:

### 1. Typst-Buchausgabe neu bauen (Dauer: ca. 0,9 Sekunden)
```bash
python3 scripts/build_typeset_edition.py
```
Erzeugt die vollständige, druckreife 737-seitige Vektor-Ausgabe unter:  
👉 `data/output/boethlingk1887_typeset_edition.pdf`

### 2. TEI-P5-XML-Edition generieren & validieren (Dauer: ca. 3 Sekunden)
```bash
python3 scripts/generate_tei_p5.py
```
Aktualisiert die XML-Edition unter `data/tei/boehtlingk1887_p5.xml` und validiert sie automatisch gegen das offizielle TEI RelaxNG-Schema (`schemas/tei_all.rng`).

### 3. (Optional) 1:1 Sandwich-PDF aktualisieren
```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

---

## 🚀 Schritt 4: Prüfen, Committen & Pull Request (Kuratierungs-Workflow)

Das Projekt `boethlingk` wird als **wissenschaftlich kuratierte Edition** (Curated Edition, geleitet von Marco Demarmels / birchville-org) geführt. Um die kanonische Integrität der 3.997 Sūtras und die Konformität der TEI-P5-XML-Edition dauerhaft zu gewährleisten, fließen Textkorrekturen, philologische Präzisierungen und Ergänzungen verbindlich über **Branch- und Pull-Request-Verfahren (PR)** ein.

### 1. Lokale Integritätsprüfung ausführen
Vor jedem Commit ist sicherzustellen, dass weder Sūtras versehentlich modifiziert oder gelöscht wurden noch das TEI-P5-Schema verletzt wird:

```bash
# a) Master-JSON-Integrität prüfen (exakt 14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras = 3.997):
python3 -c "
import json
with open('data/ashtadhyayi_complete_boethlingk1887.json', encoding='utf-8') as f:
    d = json.load(f)
assert len(d['shiva_sutras']) == 14
assert len(d['sutras']) == 3983
print('Integrität: 100% OK')
"

# b) TEI-P5-XML neu erzeugen und gegen das offizielle RelaxNG-Schema validieren:
python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### 2. Feature-Branch erstellen & Änderungen committen
Korrekturen niemals direkt auf `main` committen, sondern in einem thematischen Feature-Branch isolieren:

```bash
# Neuen Feature-Branch anlegen (Konvention: fix/sutra-<ref> oder corr/<thema>)
git checkout -b fix/sutra-1.1.4

# Geänderte Master-Daten und generierte TEI-P5-Datei stagen
git add data/ashtadhyayi_complete_boethlingk1887.json data/tei/boehtlingk1887_p5.xml

# Aussagekräftigen Commit erstellen
git commit -m "fix(sutra): correct reading and commentary for sutra 1.1.4"
```

### 3. Branch pushen & Pull Request (PR) eröffnen
Den Branch auf das Remote-Repository (bzw. den eigenen Fork) übertragen:

```bash
git push -u origin fix/sutra-1.1.4
```

Anschließend auf GitHub einen **Pull Request** gegen den Branch `main` eröffnen:
* **Über das GitHub Web-Interface:** Nach dem Push erscheint automatisch der Dialog *„Compare & pull request“*.
* **Alternativ über das GitHub CLI (`gh`):**
  ```bash
  gh pr create \
    --title "fix(sutra): Korrektur Lesart und Kommentar zu Sūtra 1.1.4" \
    --body "Philologischer Abgleich mit Faksimile UB Heidelberg Seite 3: Textkorrektur im Kommentar zu Sūtra 1.1.4."
  ```

> 💡 **Best Practice für Pull Requests:**
> - **Betroffene Sūtra-Nummer (`ref`)** und Buchseitennummer im Titel oder Text nennen (z. B. `Sūtra 1.1.4, S. 3`).
> - **Faksimile-Referenz:** Link zum entsprechenden IIIF-Faksimile der Universitätsbibliothek Heidelberg beifügen.
> - **Begründung:** Kurze Erläuterung der Korrektur (z. B. Beseitigung eines OCR-Fehlers bei IAST-Diakritika oder Devanāgarī-Ligaturen).

### 4. Automatische CI-Validierung im Pull Request
Bei jeder Eröffnung oder Aktualisierung eines Pull Requests führt die GitHub Actions CI-Pipeline (`.github/workflows/ci.yml`) automatische Validierungen durch:
* **Master Dataset Integrity:** Überprüfung aller 3.997 Sūtras auf Vollständigkeit und Eindeutigkeit (0 Duplikate, 0 Lücken).
* **TEI-P5 RelaxNG Validation:** Vollständige Schemaprüfung des generierten XML-Dokuments gegen `schemas/tei_all.rng`.

Ein Merge ist nur zulässig, wenn alle CI-Prüfungen erfolgreich („grün“) durchlaufen.

### 5. Kuratierung, Review & Merge
Als Projektkurator prüft **Marco Demarmels** jede eingereichte Korrektur philologisch und technisch:
1. **Philologische Verifikation:** Stimmt die Korrektur exakt mit der Druckfassung Böhtlingks (Leipzig 1887) überein?
2. **Kanonische Konsistenz:** Bleiben Sūtra-Zählung, Pāda-Zuordnung und Textstruktur gewahrt?
3. **Freigabe & Merge:** Nach Bestätigung wird der Pull Request in den kanonischen `main`-Branch übernommen und neue Release-Artefakte werden bei Bedarf bereitgestellt.

*(Hinweis: Direkte Commits und Pushes auf `main` sind ausschließlich dem Projektkurator für administrative Releases und Bereitstellungs-Pipelines vorbehalten.)*
