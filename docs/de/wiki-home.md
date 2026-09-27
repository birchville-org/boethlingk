# Willkommen im Wiki des Böhtlingk-Pāṇini-Projekts

> ℹ️ **Case Study:** Das Projekt `boethlingk` ist eine vollständige Referenz-Fallstudie zur Buch-Digitalisierungs-Pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**. Es demonstriert die OCR-Verarbeitung historischer Dreischriftigkeit, kanonisches Alignment und die Erstellung von 1:1 Sandwich-PDFs und TEI-P5-XML-Editionen.

Dieses Wiki dokumentiert die wissenschaftliche Erschließung, OCR-Vollerfassung, kanonische Konsolidierung und Edition von **Otto von Böhtlingks Pâṇini's Grammatik (Leipzig 1887)** auf Basis der Digitalisate der Universitätsbibliothek Heidelberg.

---

## 📖 Hauptdokumentation

* 👉 **[Wissenschaftliche Fallstudie: Vollständige Digitalisierung, TEI-P5-Edition & 1:1 Sandwich-PDF](case-study.md)**
* 👉 **[QA- & Korrektur-Workflow (Single Source of Truth & QA-Viewer)](qa-workflow.md)**
* 👉 **[Urheberrecht, Gemeinfreiheit & Provenienz (UB Heidelberg Scans)](copyright-and-provenance.md)**

Die ausführliche Dokumentation umfasst:
1. **Ausgangslage & Problemstellung:** Grenzen bisheriger Tesseract-OCR-PDFs bei historischer Dreischriftigkeit (Devanāgarī, Fraktur/Antiqua, IAST).
2. **Die Implementierte Lösung:** Vollerfassung aller 478 Buchseiten mit `mistral-ocr-latest`.
3. **Kanonisches Alignment:** Lückenloser Abgleich gegen den Aṣṭādhyāyī Sūtrapāṭha (3.997 Sūtras, 0 Duplikate, 0 Lücken).
4. **Das 1:1 Sandwich-PDF:** Verlustfreie Bildreproduktion mit unsichtbarer Vektortext-Ebene (PDF Text Render Mode 3).
5. **Wissenschaftliche TEI-P5-Edition:** 100 % schema-valide XML-Edition mit IIIF-Verknüpfungen.
6. **QA-Viewer:** Webbasierter Split-Pane-Editor mit Faksimile-Zoom und Silent Auto-Repair beim Speichern.
7. **Rechtliche Grundlagen & Provenienz:** Gemeinfreiheit nach § 64 UrhG, 2D-Digitalisate nach § 68 UrhG und Bereinigung von Bibliotheksstempeln.

---

## 🚀 Schnellzugriff auf Projektergebnisse

| Artefakt | Pfad im Repository | Beschreibung |
| :--- | :--- | :--- |
| **TEI-P5 XML** | [`data/tei/boehtlingk1887_p5.xml`](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) | Schema-valide Langzeitarchivierungs-Edition |
| **Typst-Neuausgabe** | [Release Asset (6,28 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf) | Neu gesetzte, bereinigte Gesamtausgabe (737 Seiten) |
| **Sandwich-PDF** | [Release Asset (278 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) | Durchsuchbares 1:1 Sandwich-PDF (478 Seiten) |
| **Master-Datensatz** | [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) | Strukturierte JSON-Daten aller 3.997 Sūtras |
| **QA-Viewer** | [`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html) | Autarker Split-Pane-Editor nach QA-Viewer-Standard |
| **Code-Repository** | [birchville-org/boethlingk](https://github.com/birchville-org/boethlingk) | Vollständige Pipeline-Skripte und Dokumentation |
