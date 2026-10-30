# 📦 Editions-Artefakte & Downloads

Dieses Editionsprojekt erzeugt eine aufeinander abgestimmte Familie digitaler Artefakte für Forschung, Lehre, Langzeitarchivierung und Praxis. Alle Binär-Artefakte (PDFs, EPUB, XML) werden über die offiziellen GitHub-Releases bereitgestellt.

> ⬇️ **Zentraler Release-Download:**  
> Alle aktuellen Artefakte stehen auf der GitHub-Release-Seite bereit:  
> 👉 **[github.com/birchville-org/boethlingk/releases/latest](https://github.com/birchville-org/boethlingk/releases/latest)**

---

## 🏛️ Übersicht der digitalen Artefakte

Die Artefakte decken unterschiedliche Nutzungsszenarien ab – vom exakten historischen Zitatnachweis bis hin zur computerlinguistischen Weiterverarbeitung:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             SINGLE SOURCE OF TRUTH (KANONISCHER MASTER-DATENSATZ)      │
│                ashtadhyayi_complete_boethlingk1887.json                │
│                 (3.997 Sūtras · Devanāgarī, IAST, Deutsch)             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│  FAKSIMILE-  │             │ 1:1 SANDWICH │             │   TEI-P5     │
│   NEUSATZ    │             │   SCAN-PDF   │             │  XML-EDITION │
│ 1:1 Parität  │             │ Margin-Mask  │             │   RelaxNG    │
└──────────────┘             └──────────────┘             └──────────────┘
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│  TYPST-BUCH  │             │   EPUB 3     │             │  QA-VIEWER   │
│ AUSGABE (v2) │             │  E-READER    │             │   Payer-UI   │
│  Fließlayout │             │ Font-Embed   │             │  Split-Pane  │
└──────────────┘             └──────────────┘             └──────────────┘
```

---

## 📄 Die Artefakte im Detail

### 1. Dichte Faksimile-Neuausgabe (1:1-Seitenparität)
* **Dateiname:** `boethlingk1887_facsimile_dense.pdf` (8,58 MB · 484 Seiten)
* **Was ist es?**  
  Ein vollständiger, moderner Vektorneusatz (ISO B5) mit **exakter 1:1-Seitenparität** zum historischen Leipziger Originaldruck von 1887. Jede Buchseite (S. 1–476) beginnt und endet am selben Sūtra wie bei Böhtlingk (0 Seiten Überlauf).
* **Typografische Besonderheiten:**
  * **Schriftstack:** *STIX Two Text* kombiniert mit *Noto Serif Devanagari*. Bietet native, fehlerfreie OpenType-IAST-Kapitälchen (**PĀṆINI**, **MAHĀBHĀṢYA**, **BHAṬṬOJI DĪKṢITA**) mit echten Versal-Diakritika.
  * **Adaptive Typografie:** Ein 6-Stufen-Dichtemodell skaliert Schriftgrad und Durchschuss dynamisch an die Textlast an, sodass leichte Seiten den Satzspiegel füllen und textstarke Seiten (wie S. 8) ohne Überlauf stehen.
  * **Śiva-Sūtras:** Die Eröffnungsseite (S. 1) präsentiert die 14 kanonischen Lautgruppen in einem wohlproportionierten zweispaltigen Tableau.
  * **Orientierung:** Authentische lebende Kolumnentitel und originale Rand-Sūtranummern. 48 hierarchische PDF-Lesezeichen und native römische/arabische Page-Labels.
* **Einsatzbereich:** Ideal für Indologen, die historische Zitate („Böhtlingk S. X“) exakt verifizieren möchten, ohne mit vergilbten Scans arbeiten zu müssen.
* **Download:** [Release-Asset](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf)

---

### 2. Modernisierte Typst-Buchausgabe
* **Dateiname:** `boethlingk1887_typeset_edition.pdf` (8,81 MB · 512 Seiten)
* **Was ist es?**  
  Eine typografisch modernisierte Buchausgabe mit fließendem Satz im ISO B5-Format, frei von den historischen Zeilen- und Seitenbegrenzungen des 19. Jahrhunderts.
* **Besonderheiten:** Großzügiger Zeilendurchschuss, klare optische Hierarchie zwischen Sūtra-Kopf, IAST-Transliteration, Übersetzung und Petit-Kommentar.
* **Einsatzbereich:** Für das kontinuierliche philologische und linguistische Studium der Aṣṭādhyāyī am Bildschirm oder als Buchausdruck.
* **Download:** [Release-Asset](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf)

---

### 3. Bereinigtes 1:1 Sandwich-PDF (Scan-Faksimile)
* **Dateiname:** `boehtlingk1887.perfect_sandwich.pdf` / `boehtlingk1887_sandwich.pdf` (248,8 MB · 478 Seiten)
* **Was ist es?**  
  Ein hochauflösendes Faksimile der Originalscans der Universitätsbibliothek Heidelberg, kombiniert mit einer unsichtbaren, pixelgenauen OCR-Vektor-Textebene.
* **Besonderheiten:**
  * **Content-Aware Margin Masking:** Ränder, Buchfalze und Scannerschatten wurden farbtongetreu (`#f0e8d6`) neutralisiert, während der Druckspiegel zu 100 % unangetastet blieb.
  * **Unsichtbare Textebene:** 14.267 Textblöcke auf exakten Koordinaten (PDF Rendering Mode 3) für präzises Markieren, Suchen und Kopieren.
  * **Navigation:** 42 hierarchische PDF-Bookmarks für alle Adhyāyas und Pādas.
* **Einsatzbereich:** Für Archivare und Editionsphilologen, die die originale Druckgestalt einsehen und Zitate gegen das 1887er Bild abgleichen müssen.
* **Download:** [Release-Asset (249 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf)

---

### 4. Kanonischer Master-Datensatz (JSON)
* **Dateiname:** `data/ashtadhyayi_complete_boethlingk1887.json` (2,85 MB)
* **Was ist es?**  
  Die strukturierte *Single Source of Truth* des gesamten Werkes. Enthält alle 3.997 Sūtras (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras) lückenlos validiert ohne Duplikate oder Fehlstellen.
* **Datenfelder pro Sūtra:**
  * Kanonische Referenz (`ref`, z. B. `"1.1.1"`), Adhyāya, Pāda, Sūtra-Nummer.
  * Devanāgarī-Text (`canonical_devanagari`) und wissenschaftliche IAST-Umschrift (`canonical_iast`).
  * Deutsche Fachübersetzung (`translation`) und philologischer Kommentar (`commentary`).
  * Buchseiten-Zuordnung (`page`) zur 1887er Originalausgabe.
* **Einsatzbereich:** Für NLP-Entwickler, Sanskrit-Korpuslinguisten und digitale Wörterbuchprojekte.
* **Download:** [Release-Asset (2,85 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/ashtadhyayi_complete_boethlingk1887.json)
* **Quelle:** [Im Repository ansehen](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

---

### 5. Schema-valide TEI-P5 XML-Edition
* **Dateiname:** `data/tei/boehtlingk1887_p5.xml` (2,90 MB)
* **Was ist es?**  
  Eine vollständige XML-Auszeichnung nach den Richtlinien der *Text Encoding Initiative* (TEI-P5), 100 % valide gegen das offizielle Schema `schemas/tei_all.rng`.
* **Besonderheiten:**
  * Jedes Sūtra ist als semantischer `<entry>` ausgezeichnet.
  * 478 `<pb>`-Tags enthalten direkte IIIF-Vollbild-Links zu den Scans der UB Heidelberg.
  * Böhtlingks originale Druckfehlerkorrekturen (S. 477–480) sind strukturiert in `<back>` erfasst.
* **Einsatzbereich:** Langzeitarchivierung in Universitätsbibliotheken und Einspeisung in TEI-Repositorien.
* **Quelle:** [Im Repository ansehen](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml)

---

### 6. Reflowable EPUB 3 eBook
* **Dateiname:** `boethlingk1887.epub` (1,47 MB)
* **Was ist es?**  
  Ein responsives E-Book im standardisierten EPUB 3-Format für komfortables mobiles Nachschlagen.
* **Besonderheiten:**
  * Schrifteinbettung (*Noto Serif Devanagari*) garantiert saubere Ligaturen und Diakritika auf allen Lesegeräten.
  * Vollständig gegliedertes Inhaltsverzeichnis (8 Adhyāyas, 32 Pādas).
* **Einsatzbereich:** Für E-Reader (Apple Books, Tolino, Kobo) und Tablets unterwegs.
* **Download:** [Release-Asset](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub)

---

### 7. Autarker QA-Viewer
* **Dateiname:** `viewer.html` (39 KB)
* **Was ist es?**  
  Ein browserbasierter Split-Pane-Editor nach dem Birchville-Payer-Standard.
* **Besonderheiten:** Links Zoom/Pan des Originalscans, rechts direkt editierbare Sūtra-Felder mit lokalem *Silent Auto-Repair* beim Speichern über die File System Access API.
* **Einsatzbereich:** Für die visuelle Kollationierung und Nachkorrektur direkt auf der lokalen Festplatte ohne Cloud-Abhängigkeit.
* **Quelle:** [Im Repository ansehen](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)

---

## 📊 Artefakt-Matrix im Überblick

| Artefakt | Primäre Datei | Format | Umfang | Hauptzweck | Download / Zugriff |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Dichte Faksimile-Ausgabe** | `boethlingk1887_facsimile_dense.pdf` | PDF (Vektor) | 8,58 MB (484 S.) | 1:1-Zitierfähigkeit (STIX Two Text) | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf) |
| **Buchausgabe** | `boethlingk1887_typeset_edition.pdf` | PDF (Vektor) | 8,81 MB (512 S.) | Fortlaufendes Lese-Layout | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf) |
| **1:1 Sandwich-PDF** | `boehtlingk1887_sandwich.pdf` | PDF (Scan+OCR) | 248,8 MB (478 S.) | Historische Quellenprüfung | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) |
| **Master-Datensatz** | `ashtadhyayi_complete_boethlingk1887.json` | JSON | 2,85 MB (3.997 Sūtras) | Single Source of Truth / NLP | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/ashtadhyayi_complete_boethlingk1887.json) |
| **TEI-P5 Edition** | `boehtlingk1887_p5.xml` | XML (TEI-P5) | 2,90 MB | Digital Humanities / Archiv | [GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) |
| **EPUB 3 eBook** | `boethlingk1887.epub` | EPUB 3 | 1,47 MB | Mobiles Nachschlagen (E-Reader) | [Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) |
| **QA-Viewer** | `viewer.html` | HTML5 / JS | 39 KB | Lokale visuelle Korrektur | [Viewer](https://github.com/birchville-org/boethlingk/blob/main/viewer.html) |
