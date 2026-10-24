# Fallstudie: Pāṇinis Grammatik (Otto von Böhtlingk, 1887)

> **Digitale Edition, kanonischer Sūtra-Abgleich und Typst-Vektorneusatz von 3.997 Sūtras auf 478 Buchseiten.**
>
> 🔗 **Projekt-Repository:** [github.com/birchville-org/boethlingk](https://github.com/birchville-org/boethlingk)  
> 🔗 **Hauptpipeline:** [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)

---

## 1. Ausgangslage & Einordnung

Otto von Böhtlingks Ausgabe *Pâṇini's Grammatik* (2. Auflage, Leipzig 1887) ist das weltweit maßgebliche philologische Referenzwerk für das grammatische System der Aṣṭādhyāyī. Das Werk vereint auf 478 Buchseiten drei disparate Schriftsysteme:

1. **Sanskrit in Devanāgarī:** Historischer Bleisatz mit komplexen Ligaturen und Virāmas.
2. **Deutsch in 19.-Jh.-Antiqua:** Fachübersetzung und grammatischer Erläuterungsapparat.
3. **IAST-Transliteration:** Lateinschrift mit multiplen kombinierten Diakritika (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṃ`, `ḥ`, `ṅ`, `ñ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`) und vedischen Akzenten.

Dieses Projekt dient als **Referenz-Fallstudie** für die Open-Source-Buchdigitalisierungs-Pipeline [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich).

---

## 2. Hauptpipeline vs. Böhtlingk-Delta

Alle generischen Aufgaben der Digitalisierung und Bildverarbeitung werden von der zentralen **AlexandriaSandwich-Hauptpipeline** bereitgestellt. Das Projekt `boethlingk` konzentriert sich ausschließlich auf das **semantische und philologische Delta**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│               ALEXANDRIASANDWICH (GENERISCHE HAUPTPIPELINE)            │
│  • IIIF-Scan-Ingestion (UB Heidelberg)                                 │
│  • Multimodale KI-OCR (mistral-ocr-latest) & Bounding-Box-Geometrie    │
│  • Content-Aware Margin Masking (Hintergrund-Farbton #f0e8d6)          │
│  • Geometrisches Layout-Profiling (layout.profile.json)                │
│  • 1:1 Sandwich-PDF Assemblierung & QA-Viewer-Bereitstellung           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Bounding-Boxes, Layout & Faksimiles
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   DAS BÖHTLINGK-DELTA (EDITIONS-SCHICHT)               │
│  • Delta 1: Kanonische 8-Adhyāya-Statusmaschine (align_mistral_sutras) │
│  • Delta 2: Fuzzy SequenceMatcher gegen Aṣṭādhyāyī Sūtrapāṭha           │
│  • Delta 3: Typst-Satzschablone für Devanāgarī, IAST & Kommentarapparat│
│  • Delta 4: RelaxNG-geprüfte TEI-P5-XML- und EPUB 3-Serialisierung    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Das Böhtlingk-Delta im Detail

### 3.1 Delta 1: Kanonische Sūtra-Statusmaschine (`scripts/align_mistral_sutras.py`)
Das Werk folgt der strikten kanonischen Gliederung der Aṣṭādhyāyī:
* **Struktur:** 8 Adhyāyas zu je exakt 4 Pādas (32 Pādas gesamt) mit 3.983 Aṣṭādhyāyī-Sūtras plus 14 vorgeschalteten Śiva-Sūtras (3.997 Sūtras gesamt).
* **Automatischer Pāda- & Adhyāya-Rollover:** Erreicht die Erkennung das Ende eines Pādas, erzwingt die Statusmaschine den deterministischen Übergang (`state["adhyaya"] += 1, state["pada"] = 1`), selbst wenn der historische Kolophon verwischt oder unvollständig erkannt wurde.
* **Corrigenda-Isolation:** Nachträge und Korrekturen Böhtlingks (S. 477–478) nach dem Schlusssūtra 8.4.68 (`अ अ`) werden isoliert erfasst und kontaminieren nicht den Kommentarapparat.

### 3.2 Delta 2: Fuzzy Canonical Matching gegen die Ground-Truth
Aufgrund vergilbter Typen verwechselte die OCR gelegentlich Devanāgarī-Ziffern (z. B. ८ als ६, also `६५` statt `८५`):
* **SequenceMatcher-Abgleich:** Weicht eine Sūtra-Nummer ab, vergleicht der Algorithmus den normalisierten Devanāgarī-Text mit dem erwarteten Sūtra aus `data/sutras.json`.
* **Korrekturschwelle:** Bei einer Ähnlichkeit >= 0,45 wird der Sūtra-Zähler automatisch auf die kanonische Zählung korrigiert.
* **Lange Komposita:** Sūtras mit bis zu 350 Zeichen ohne führendes `#`-Zeichen (z. B. 5.4.77 mit 185 Zeichen) werden über Danda-Muster (`॥...॥`) zuverlässig als Sūtra-Kopf erkannt.

### 3.3 Delta 3: Typografischer Neusatz (`scripts/boethlingk1887_edition.typ`)
Für die typografische Neuausgabe wurde eine spezifische Typst-Schablone realisiert:
* **Gliederung pro Sūtra:**
  1. Devanāgarī-Kopf mit kanonischer Zählung (`१.१.१`).
  2. Wissenschaftliche IAST-Transliteration (Halbfett).
  3. Deutsche Übersetzung (Kursiv).
  4. Eingerückter Kleindruck-Kommentar mit philologischem Apparat (`∠±`, `Kāç.`, `RV.`).
* **Buchgestaltung:** ISO B5 (176 x 250 mm), Schriftenverbund (*Noto Serif Devanagari* + *Libertinus Serif*), lebende Kolumnentitel und 47 hierarchische PDF-Bookmarks.
* **Kompilierung:** Ausführung via `python3 scripts/build_typeset_edition.py` in ~8,9 Sekunden.

### 3.4 Delta 4: Standardisierte TEI-P5- und EPUB 3-Editionen
* **TEI-P5 XML (`data/tei/boehtlingk1887_p5.xml`):** 100 % valide gegen TEI All RelaxNG (`schemas/tei_all.rng`), 3.997 `<tei:entry>`-Elemente und 478 `<tei:pb>`-Seitenumbrüche mit direkter Verlinkung zu den Heidelberger IIIF-Faksimiles.
* **EPUB 3 (`boethlingk1887.epub`):** Reflowable E-Book mit Schrifteinbettung für vollständige diakritische Lesbarkeit auf mobilen Geräten.

---

## 4. Validierungsergebnisse

Alle 8 Adhyāyas und die einleitenden Śiva-Sūtras wurden 1:1 gegen die kanonische Referenzdatenbank validiert:

| Bereich | Buchseiten | Sūtras (Ist / Soll) | Duplikate | Fehlstellen | Validierungsstatus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Śiva-Sūtrāṇi** | 1 | 14 / 14 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 1** | 2–43 | 351 / 351 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 2** | 43–75 | 268 / 268 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 3** | 75–148 | 631 / 631 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 4** | 149–221 | 635 / 635 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 5** | 221–282 | 555 / 555 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 6** | 283–374 | 736 / 736 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 7** | 375–428 | 438 / 438 | 0 | 0 | **100,0 % validiert** |
| **Adhyāya 8** | 429–478 | 369 / 369 | 0 | 0 | **100,0 % validiert** |
| **Gesamt** | **478 Seiten** | **3.997 / 3.997** | **0** | **0** | **100,0 % lückenlos** |

---

## 5. Kernartefakte & Bezugsquellen

| Artefakt | Format / Datei | Umfang | Bezugsquelle |
| :--- | :--- | :--- | :--- |
| **Sandwich-PDF** | `boehtlingk1887.perfect_sandwich.pdf` | 248,85 MB (478 S.) | [Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) |
| **Typst-Buchsatz** | `boethlingk1887_typeset_edition.pdf` | 7,62 MB (737 S.) | [Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition_v2.pdf) |
| **Master-Datensatz** | `data/ashtadhyayi_complete_boethlingk1887.json` | 2,85 MB | [GitHub Repository](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) |
| **TEI-P5 XML** | `data/tei/boehtlingk1887_p5.xml` | 2,90 MB | [GitHub Repository](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) |
| **EPUB 3** | `boethlingk1887.epub` | 1,47 MB | [Release Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) |
| **QA-Viewer** | `viewer.html` | 39 KB | [Im Browser öffnen](https://github.com/birchville-org/boethlingk/blob/main/viewer.html) |
