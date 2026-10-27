# Das Böhtlingk-Delta & Philologische Fallstudie

> **Wissenschaftliche Edition, kanonisches Sūtra-Alignment und typografischer 1:1-Faksimile-Neusatz von Otto von Böhtlingks *Grammatik des Pāṇini* (Leipzig 1887).**
>
> 🔗 **Projekt-Repository:** [github.com/birchville-org/boethlingk](https://github.com/birchville-org/boethlingk)  
> 🔗 **Zentrale Verfahrenspipeline:** [AlexandriaSandwich Verfahrensdokumentation](https://birchville-org.github.io/AlexandriaSandwich/de/WIKI_VERFAHREN/)  
> 📦 **Alle Downloads:** [Editions-Artefakte & Downloads](artifacts.md)

---

## 1. Ausgangslage & Abgrenzung zur Hauptpipeline

Otto von Böhtlingks monumentale Ausgabe *Pâṇini's Grammatik* (2. Auflage, Leipzig 1887, Verlag von H. Haessel) ist das weltweit maßgebliche philologische Referenzwerk für das altindische grammatische System der Aṣṭādhyāyī. Das Werk vereint auf 478 Buchseiten drei Schriftsysteme:
1. **Sanskrit in Devanāgarī:** Historischer 19.-Jh.-Bleisatz mit komplexen Ligaturen und Virāmas.
2. **Deutsch in historischer Antiqua:** Fachwissenschaftliche Übersetzung und grammatischer Apparat.
3. **IAST-Transliteration:** Lateinschrift mit multiplen kombinierten Diakritika (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṃ`, `ḥ`, `ṅ`, `ñ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`) und vedischen Akzenten.

> ℹ️ **Verfahrensabgrenzung:**  
> Alle generischen Schritte der Bilddigitalisierung, des IIIF-Cachings, der multimodalen KI-OCR (`mistral-ocr-latest`), des Content-Aware Margin Maskings (`#f0e8d6`) sowie der Erzeugung von 1:1 Sandwich-PDFs werden von der übergeordneten **[AlexandriaSandwich-Hauptpipeline](https://birchville-org.github.io/AlexandriaSandwich/de/WIKI_VERFAHREN/)** bereitgestellt.  
>  
> Dieses Dokument beschreibt **ausschließlich das spezifische Editions-Delta** des Projekts `boethlingk`: die kanonische Sūtra-Segmentierung, die philologische Korrektur, die 1:1-Seitenparität im Neusatz sowie die TEI-P5-Modellierung.

---

## 2. Architektur: Pipeline vs. Editions-Delta

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ALEXANDRIASANDWICH (GENERISCHE HAUPTPIPELINE)              │
│  • IIIF-Scan-Ingestion (UB Heidelberg: boehtlingk1887)                 │
│  • Multimodale KI-OCR (mistral-ocr-latest) & Bounding-Box-Geometrie    │
│  • Content-Aware Margin Masking (Falz- & Ränderbereinigung #f0e8d6)    │
│  • Sandwich-PDF-Schichtung (unsichtbare Vektorschrift-Ebene)           │
│  • Lokale VLM-Benchmarks & n8n-Workflow-Automatisierung                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Layout, Geometrie & Rohfaksimiles
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   DAS BÖHTLINGK-DELTA (EDITIONS-SCHICHT)               │
│  • Delta 1: Kanonische 8-Adhyāya-Statusmaschine (align_mistral_sutras) │
│  • Delta 2: Fuzzy-SequenceMatcher gegen Aṣṭādhyāyī-Ground-Truth        │
│  • Delta 3: 1:1 Faksimile-Neusatz mit adaptiver Typografie (Typst)     │
│  • Delta 4: STIX Two Text Fontstack für native IAST-Kapitälchen        │
│  • Delta 5: TEI-P5-XML auf Sūtra-Ebene & reflowable EPUB 3             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Das Böhtlingk-Delta im Detail

### 3.1 Delta 1: Kanonische Sūtra-Statusmaschine (`scripts/align_mistral_sutras.py`)
Das Werk folgt der strikten kanonischen Gliederung der Aṣṭādhyāyī:
* **Kanonische Struktur:** 8 Adhyāyas zu je exakt 4 Pādas (32 Pādas gesamt) mit 3.983 Aṣṭādhyāyī-Sūtras plus 14 vorgeschalteten Śiva-Sūtras (**3.997 Sūtras gesamt**).
* **Deterministischer Pāda- & Adhyāya-Rollover:** Erreicht die Erkennung das Ende eines Pādas, erzwingt die Statusmaschine den deterministischen Übergang (`state["adhyaya"] += 1, state["pada"] = 1`), selbst wenn der historische Kolophon im Scan verwischt oder unvollständig erkannt wurde.
* **Corrigenda-Isolation:** Nachträge und Korrekturen Böhtlingks (S. 477–480) nach dem Schlusssūtra 8.4.68 (`अ अ`) werden isoliert erfasst und kontaminieren nicht den Kommentarapparat.

### 3.2 Delta 2: Fuzzy Canonical Matching gegen die Ground-Truth
Aufgrund historisch vergilbter Typen verwechselte die OCR gelegentlich Devanāgarī-Ziffern (z. B. ८ als ६, also `६५` statt `८५`):
* **SequenceMatcher-Abgleich:** Weicht eine Sūtra-Nummer ab, vergleicht der Algorithmus den normalisierten Devanāgarī-Text mit dem erwarteten Sūtra aus der Referenzdatenbank `data/sutras.json`.
* **Korrekturschwelle:** Bei einer Ähnlichkeit >= 0,45 wird der Sūtra-Zähler automatisch auf die kanonische Zählung korrigiert.
* **Lange Sanskrit-Komposita:** Sūtras mit bis zu 350 Zeichen ohne führendes `#`-Zeichen (z. B. 5.4.77 mit 185 Zeichen) werden über Danda-Muster (`॥...॥`) zuverlässig als Sūtra-Kopf erkannt und sauber von der Übersetzung getrennt.

### 3.3 Delta 3: 1:1 Faksimile-Neusatz mit adaptiver Typografie (`boethlingk1887_facsimile_dense.typ`)
Im Unterschied zur allgemeinen Typst-Buchausgabe rekonstruiert die Faksimile-Ausgabe den historischen Leipziger Satzspiegel mit **exakter 1:1-Seitenkongruenz**:
* **1:1-Seitenparität:** Jede Originalseite (S. 1 bis 476) beginnt und endet am selben Sūtra wie bei Böhtlingk 1887 (**0 Seiten Überlauf** bei 484 Gesamtseiten). Sämtliche Zitate nach Seitenzahlen stimmen 1:1 überein.
* **Adaptive Typografie (6-Stufen-Modell):** Um zu verhindern, dass leichte Seiten oben zusammengequetscht wirken und textstarke Seiten überlaufen, steuert ein 6-stufiges Profil (`scripts/prepare_facsimile_dense_data.py`) Durchschuss, Schriftgrad und Sūtra-Spatien dynamisch:
  * *Level 0 (Extremste Dichte: nur S. 282 & 286 mit 11 dichten Sūtras):* Body 8,1 pt, Petit 6,9 pt, Spatium 0,06 em.
  * *Level 1 (Hohe Dichte: z. B. S. 3, 70, 378 mit 10–12 Sūtras):* Body 8,4 pt, Petit 7,2 pt, Spatium 0,12 em.
  * *Level 2 (Kompakt: textstarke Seiten):* Body 8,6 pt, Petit 7,4 pt, Spatium 0,20 em.
  * *Level 3 (Standard: 6–8 Sūtras, ~50 % des Werkes):* Body 8,9 pt, Petit 7,7 pt, Spatium 0,38 em.
  * *Level 4 (Großzügig: z. B. S. 8 mit 3–6 Sūtras):* Body 9,3 pt, Petit 8,1 pt, Spatium 0,70 em (hoher Durchschuss, füllt den Satzspiegel zu über 80 %).
  * *Level 5 (Maximaler Komfort: 1–4 kurze Sūtras):* Body 9,6 pt, Petit 8,4 pt, Spatium 0,95 em.
* **Zweispaltiges Śiva-Sūtra-Tableau (Seite 1):** Die 14 kanonischen Eröffnungs-Sūtras stehen in einem großzügigen, zweispaltigen Tableau mit Devanāgarī (12,5 pt fett) und kursiver IAST-Umschrift.
* **Originale Kolumnentitel:** Lebende Kolumnentitel im Kopf (`I. Adhyāya. 1. Pāda.` / `1, 1, 7.`) und Sūtra-Nummern am Außenrand.

### 3.4 Delta 4: STIX Two Text Fontstack für native IAST-Kapitälchen
Standard-Schriften (wie *Libertinus Serif* oder *Times*) unterstützen das OpenType-Feature `smcp` nur für das Basis-Lateinalphabet. Bei IAST-Sonderzeichen (`ṇ`, `ṭ`, `ṣ`, `ṛ`) fallen sie unschön auf Minuskeln zurück (**PĀṇINI**).
* Die Neuausgabe setzt konsequent auf **STIX Two Text** + **Noto Serif Devanagari**.
* STIX Two Text implementiert vollwertige, handgezeichnete OpenType-Kapitälchen für alle IAST-Diakritika (**PĀṆINI**, **MAHĀBHĀṢYA**, **BHAṬṬOJI DĪKṢITA**) mit perfekter Grauwert-Balance.

### 3.5 Delta 5: Standardisierte TEI-P5- und EPUB 3-Serialisierung
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

## 5. Bereitgestellte Artefakte & Download-Verweise

Eine vollständige Beschreibung aller erzeugten Ausgabedateien (Faksimile-Neusatz, Typst-Buchausgabe, Sandwich-PDF, Master-JSON, TEI-P5-XML und EPUB 3) mit Zweck, Format und direkten Downloadlinks finden Sie im dedizierten Katalog:

👉 **[Zur Artefakt-Übersicht & Download-Katalog (artifacts.md)](artifacts.md)**  
👉 **[Zentrale GitHub-Release-Seite (Latest)](https://github.com/birchville-org/boethlingk/releases/latest)**
