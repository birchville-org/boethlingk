> 🌐 **Sprache / Language:** [🇩🇪 Deutsch](Home) | [🇬🇧 English](Home-en)

# Willkommen im Wiki des Böhtlingk-Pāṇini-Projekts

Dieses Wiki dokumentiert die wissenschaftliche Erschließung, OCR-Vollerfassung, kanonische Konsolidierung und Edition von **Otto von Böhtlingks Pâṇini's Grammatik (Leipzig 1887)** auf Basis der Digitalisate der Universitätsbibliothek Heidelberg.

---

## 📖 Hauptdokumentation

👉 **[[Wissenschaftliche Fallstudie: Vollständige Digitalisierung, TEI-P5-Edition & 1:1 Sandwich-PDF|Case-Study-Boethlingk-Panini-1887]]**

Die ausführliche Dokumentation umfasst:
1. **Ausgangslage & Problemstellung:** Grenzen bisheriger Tesseract-OCR-PDFs bei historischer Dreischriftigkeit (Devanāgarī, Fraktur/Antiqua, IAST).
2. **Die Implementierte Lösung:** Vollerfassung aller 478 Buchseiten mit `mistral-ocr-latest`.
3. **Kanonisches Alignment:** Lückenloser Abgleich gegen den Aṣṭādhyāyī Sūtrapāṭha (3.997 Sūtras, 0 Duplikate, 0 Lücken).
4. **Das 1:1 Sandwich-PDF:** Verlustfreie Bildreproduktion mit unsichtbarer Vektortext-Ebene (PDF Text Render Mode 3).
5. **Wissenschaftliche TEI-P5-Edition:** 100 % schema-valide XML-Edition mit IIIF-Verknüpfungen.
6. **QA-Viewer:** Webbasierter Split-Pane-Editor mit Faksimile-Zoom und Silent Auto-Repair beim Speichern.

---

## 🚀 Schnellzugriff auf Projektergebnisse

| Artefakt | Pfad im Repository | Beschreibung |
| :--- | :--- | :--- |
| **TEI-P5 XML** | [`data/tei/boehtlingk1887_p5.xml`](https://github.com/marcodem/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml) | Schema-valide Langzeitarchivierungs-Edition |
| **Sandwich-PDF** | `data/output/boehtlingk1887_sandwich.pdf` | Durchsuchbares 1:1 Sandwich-PDF (278 MB, 478 Seiten) |
| **Master-Datensatz** | [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/marcodem/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json) | Strukturierte JSON-Daten aller 3.997 Sūtras |
| **QA-Viewer** | [`viewer.html`](https://github.com/marcodem/boethlingk/blob/main/viewer.html) | Autarker Split-Pane-Editor nach QA-Viewer-Standard |
| **Code-Repository** | [marcodem/boethlingk](https://github.com/marcodem/boethlingk) | Vollständige Pipeline-Skripte und Dokumentation |
| **Online-Docs** | [marcodem.github.io/boethlingk](https://marcodem.github.io/boethlingk/) | Mehrsprachige MkDocs-Dokumentation |
