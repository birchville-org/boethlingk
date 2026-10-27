# Das Böhtlingk-Delta: Methodik & Rechtfertigung des Editionsprojekts

> **Wissenschaftliche Edition, kanonisches Sūtra-Alignment und typografischer 1:1-Faksimile-Neusatz von Otto von Böhtlingks *Grammatik des Pāṇini* (Leipzig 1887).**
>
> 🔗 **Projekt-Repository:** [github.com/birchville-org/boethlingk](https://github.com/birchville-org/boethlingk)  
> 🔗 **Zentrale Verfahrenspipeline:** [AlexandriaSandwich](https://birchville-org.github.io/AlexandriaSandwich/)  
> 📦 **Alle Downloads:** [Editions-Artefakte & Downloads](artifacts.md)

---

## 1. Rechtfertigung für ein eigenständiges Editionsprojekt

Warum reicht für ein Werk wie Otto von Böhtlingks *Pâṇini's Grammatik* (2. Auflage, Leipzig 1887) nicht der reguläre Durchlauf durch die generische Digitalisierungs-Pipeline [AlexandriaSandwich](https://birchville-org.github.io/AlexandriaSandwich/)?

AlexandriaSandwich ist als universelle, zustandslose Engine konzipiert: Sie transformiert historische Buchscans in bereinigte, durchsuchbare 1:1 Sandwich-PDFs und Rohtexte. Bei vielschichtigen, mehrsprachigen Referenzwerken der Philologie stößt eine rein vollautomatische Pipeline jedoch an methodische Grenzen.

Die Ausgründung von `boethlingk` als **eigenständiges Editions-Projekt (Satelliten-Architektur)** stützt sich auf vier tragende Säulen:

### A. Schutz der Hauptpipeline vor der „Monolith-Falle“ (*YAGNI-Prinzip*)
Würde man versuchen, die hochgradig spezifischen grammatischen Regeln der Aṣṭādhyāyī (3.997 Sūtras, 32 Pādas, historische Kolophone, zweisprachige Petit-Kommentare) direkt in die Kernskripte von AlexandriaSandwich einzubetten, würde die Plattform unwartbar überfrachtet. AlexandriaSandwich bleibt schlank, universell und robust für 90 % aller Standardbücher, während die philologische Domänenlogik vollständig im Editions-Satelliten isoliert ist.

### B. Wahrung der historischen 1:1-Zitierfähigkeit (Seitenparität)
Seit 1887 zitiert die weltweite Indologie Pāṇini nach den Original-Seitenzahlen des Leipziger Erstdrucks von Haessel („Böhtlingk S. 42“). Eine standardmäßige Neusatz-Pipeline bricht Text dynamisch um, wodurch die historische Seitenzählung sofort kollabiert. Das Projekt `boethlingk` garantiert durch ein spezielles volumetrisches Kalibrierungsverfahren **strikte 1:1-Seitenkongruenz auf allen 476 Originalseiten** bei 0 Überläufen.

### C. Kanonische Struktur vs. Prosa-Fließtext
Böhtlingks Werk ist kein fortlaufender Lesetext, sondern ein geschlossenes hierarchisches Regelsystem:
* 14 vorangestellte Śiva-Sūtras (Lautsystem)
* 3.983 Aṣṭādhyāyī-Sūtras in 8 Büchern (Adhyāyas) und 32 Abschnitten (Pādas)
* Historischer dreisprachiger Schriftsatz (Devanāgarī, deutsche Antiqua, wissenschaftliche IAST-Transliteration mit vedischen Akzenten)
* Nachträge und Berichtigungen (Corrigenda S. 477–480)

Diese Struktur erfordert deterministische Übergangs-Statusmaschinen und Ground-Truth-Validierungen, die weit über generische OCR hinausgehen.

### D. Dauerhafte wissenschaftliche Kuration & Versionierung
Eine wissenschaftliche Edition ist kein Einmal-Export, sondern ein dynamisches Forschungsinstrument. Typografische Unschärfen, Devanāgarī-Ligaturen oder IAST-Diakritika müssen im Laufe der wissenschaftlichen Nutzung kollationiert, korrigiert und über ein transparentes **Branch- und Pull-Request-Verfahren** in Git versioniert werden.

---

## 2. Architektur: AlexandriaSandwich (Plattform) vs. Böhtlingk (Edition)

Die Rollenteilung zwischen der übergeordneten Verarbeitungs-Engine und dem Editions-Satelliten ist präzise definiert:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ALEXANDRIASANDWICH (GENERISCHE HAUPTPIPELINE)              │
│  • IIIF-Scan-Ingestion (UB Heidelberg: boehtlingk1887)                 │
│  • Falz- & Ränderbereinigung / Content-Aware Margin Masking (#f0e8d6)  │
│  • Multimodale KI-OCR (mistral-ocr-latest) & Wort-Bounding-Boxes       │
│  • Generische Sandwich-PDF-Schichtung (unsichtbarer Vektortext)        │
│  🔗 Dokumentation: https://birchville-org.github.io/AlexandriaSandwich/ │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Bounding-Boxes, Layout & Rohfaksimiles
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   DAS BÖHTLINGK-DELTA (EDITIONS-SCHICHT)               │
│  1. Kanonische Sūtra-Statusmaschine (8 Adhyāyas / 32 Pādas / 3.997 S.) │
│  2. Philologischer Abgleich gegen Aṣṭādhyāyī-Ground-Truth              │
│  3. 1:1 Faksimile-Neusatz mit volumengesteuerter adaptiver Typografie  │
│  4. STIX Two Text Fontstack für native IAST-Kapitälchen                │
│  5. TEI-P5-XML auf Sūtra-Ebene & autarker Split-Pane-QA-Viewer         │
└────────────────────────────────────────────────────────────────────────┘
```

> ℹ️ **Verfahrens-Referenz:**  
> Alle generischen Schritte der Bildoptimierung, OCR-Schwellenwerte und Sandwich-Assemblierung sind in der [AlexandriaSandwich Verfahrensdokumentation](https://birchville-org.github.io/AlexandriaSandwich/de/WIKI_VERFAHREN/) sowie im [Triage- und Ökonomie-Modell](https://birchville-org.github.io/AlexandriaSandwich/de/EVOLUTION_WORKFLOW/#3-das-triage-okonomie-modell-core-pipeline-vs-editions-satelliten) beschrieben.

---

## 3. Das Methoden-Delta im Detail

Das spezifische Editions-Delta von `boethlingk` umfasst 5 wesentliche philologische und technische Entwicklungen:

### 3.1 Delta 1: Kanonische Sūtra-Statusmaschine (`scripts/align_mistral_sutras.py`)
* **Deterministischer Rollover:** Die Statusmaschine erzwingt beim Erreichen des Pāda-Endes den kanonischen Übergang (`adhyaya += 1, pada = 1`), selbst wenn historische Abschlusskolophone im Originalscan abgerieben oder beschädigt waren.
* **Corrigenda-Isolation:** Nachträge und Berichtigungen Böhtlingks (S. 477–480) nach dem Schlusssūtra 8.4.68 (`अ अ`) werden isoliert erfasst und kontaminieren nicht den vorangehenden Kommentar.

### 3.2 Delta 2: Fuzzy Ground-Truth-Matching & Komposita-Zerlegung
* **Ziffern-Desambiguierung:** Historische Bleisatz-Ziffern in Devanāgarī werden von OCR-Modellen häufig verwechselt (z. B. ۸ als ६). Der Matcher gleicht abweichende Ziffernfolgen mit dem normalisierten Text der Aṣṭādhyāyī-Referenzdatenbank ab (Schwellenwert >= 0,45) und stellt die korrekte Sūtra-Nummerierung automatisch wieder her.
* **Komposita-Erkennung:** Überlange Sūtras ohne Überschrifts-Tokens (bis zu 350 Zeichen, z. B. 5.4.77) werden über Danda-Muster (`॥...॥`) zuverlässig isoliert und sauber von der deutschen Übersetzung getrennt.

### 3.3 Delta 3: Volumengesteuerte adaptive Typografie (`boethlingk1887_facsimile_dense.typ`)
Statt einer pauschalen Verkleinerung aller Seiten steuert eine 6-stufige typografische Leiter ([`data/calibrated_dense_profiles.json`](https://github.com/birchville-org/boethlingk/blob/main/data/calibrated_dense_profiles.json)) Schriftgrade und Zeilendurchschuss adaptiv:

| Level | Seiten | Devanāgarī | Übersetzung / Durchschuss | Petit-Kommentar / Durchschuss | Sūtra-Abstand | Typische Seitentypen |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **5** | 6 | 11,8 pt | 9,6 pt / 0,45em | 8,4 pt / 0,42em | 0,95em | 1–4 kurze Sūtras, minimaler Text |
| **4** | 102 | 11,4 pt | 9,3 pt / 0,42em | 8,1 pt / 0,38em | 0,70em | 3–6 Sūtras (z. B. S. 8), mittlerer Text |
| **3** | 239 | 10,8 pt | 8,9 pt / 0,37em | 7,7 pt / 0,32em | 0,38em | 6–8 Sūtras, Standarddichte (~50 %) |
| **2** | 95 | 10,4 pt | 8,6 pt / 0,33em | 7,4 pt / 0,27em | 0,20em | 8–10 Sūtras, textstark |
| **1** | 31 | 10,0 pt | 8,4 pt / 0,30em | 7,2 pt / 0,25em | 0,12em | 10–12 Sūtras (z. B. S. 3, 70, 378) |
| **0** | 2 | 9,6 pt | 8,1 pt / 0,26em | 6,9 pt / 0,23em | 0,06em | Nur Extremseiten S. 282 & 286 (11 dichte Sūtras) |

* **Ergebnis:** Über 73 % aller Seiten laufen auf hohem Lesekomfort (Stufe 3–5). Der Satzspiegel wird harmonisch ausgefüllt, während auf allen 476 Originalseiten **exakt 0 Überläufe** entstehen.
* **Eröffnungs-Tableau (Seite 1):** Die 14 Śiva-Sūtras stehen in einem zweispaltigen Tableau mit Devanāgarī und IAST-Transliteration, gefolgt von Böhtlingks authentischer Einleitung.

### 3.4 Delta 4: STIX Two Text Fontstack für native IAST-Kapitälchen
Standard-Schriften (wie *Libertinus Serif*) besitzen unvollständige OpenType-Kapitälchen (`smallcaps`) für erweiterte IAST-Diakritika (`ā`, `ī`, `ū`, `ṛ`, `ṣ`, `ś`, `ṇ`, `ṃ`, `ḥ`), was in Kolumnentiteln und Überschriften zu fehlerhaften Minuskel-Fallbacks führt (**PĀṇINI**).
* `boethlingk` standardisiert verbindlich auf **STIX Two Text** + **Noto Serif Devanagari**.
* Bietet echte, optisch ausbalancierte Kapitälchen für sämtliche indologischen Transliterationszeichen (**PĀṆINI**, **MAHĀBHĀṢYA**, **BHAṬṬOJI DĪKṢITA**).

### 3.5 Delta 5: Strukturierte philologische Editionen & Autarker QA-Viewer
* **Master-Datensatz:** [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) als Single Source of Truth mit 3.997 vollständigen Sūtra-Objekten.
* **TEI-P5 XML:** [`data/tei/boehtlingk1887_p5.xml`](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) (100 % valide gegen TEI All RelaxNG) mit 478 `<pb>`-Tags zu den Heidelberger IIIF-Faksimiles.
* **QA-Viewer ([`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)):** Browserbasierter Split-Pane-Editor mit IIIF-Faksimile links, editierbaren Sūtra-Feldern rechts und *Silent Auto-Repair* beim Speichern über die File System Access API.

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

Eine vollständige Beschreibung aller erzeugten Ausgabedateien (Faksimile-Neusatz, Typst-Buchausgabe, Sandwich-PDF, Master-JSON, TEI-P5-XML und EPUB 3) mit Formatangaben und direkten Downloadlinks finden Sie im dedizierten Katalog:

👉 **[Zur Artefakt-Übersicht & Download-Katalog (artifacts.md)](artifacts.md)**  
👉 **[Zentrale GitHub-Release-Seite (Latest)](https://github.com/birchville-org/boethlingk/releases/latest)**
