<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--md-default-bg-color--light); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;">
  <img src="assets/birchville_logo.png" alt="Birchville Wappen" style="height: 2.4rem; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18));">
  <div>
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--md-accent-fg-color); font-weight: 700;">Birchville Scholarly Synthesis</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--md-default-fg-color);">Kanonische Editionen klassischer philologischer Referenzwerke</div>
  </div>
</div>

# 📖 Pāṇinis Grammatik (Otto von Böhtlingk, Leipzig 1887)

**Wissenschaftliche Digitalisierung, kanonisches Alignment, TEI-P5-Edition und typografischer 1:1-Faksimile-Neusatz der *Grammatik des Pāṇini* (Otto von Böhtlingk, 2. Auflage, Leipzig 1887).**

---

## ⚡ Schnellzugriff & Downloads

<div class="quick-access-grid">
  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🏛️</span>
        <span class="quick-card-title">1:1 Faksimile-Neusatz</span>
      </div>
      <div class="quick-card-body">
        Moderner Vektorneusatz in STIX Two Text mit <strong>exakter 1:1-Seitenparität</strong> (476 Textseiten ohne Überlauf), adaptiver Typografie, nativen IAST-Kapitälchen und 48 PDF-Lesezeichen.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf" class="quick-btn quick-btn-primary" target="_blank" rel="noopener">
        <span>⬇️</span> Faksimile-PDF (8,6 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📚</span>
        <span class="quick-card-title">1:1 Sandwich-PDF</span>
      </div>
      <div class="quick-card-body">
        478 Seiten hochauflösendes Scan-Faksimile der UB Heidelberg mit Content-Aware Margin Masking (#f0e8d6), unsichtbarer OCR-Textebene (14.267 Textblöcke) und 42 Lesezeichen.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>⬇️</span> Sandwich-PDF (249 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📦</span>
        <span class="quick-card-title">Alle Artefakte & Downloads</span>
      </div>
      <div class="quick-card-body">
        Detaillierter Katalog aller digitalen Editions-Artefakte (Typst-Neusatz, EPUB 3, TEI-P5 XML, Master-JSON, QA-Viewer) mit Formatbeschreibungen und Release-Links.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="artifacts/" class="quick-btn quick-btn-outline">
        <span>➔</span> Artefakt-Katalog öffnen
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🔍</span>
        <span class="quick-card-title">Das Böhtlingk-Delta</span>
      </div>
      <div class="quick-card-body">
        Verfahrensunterschiede zur AlexandriaSandwich-Hauptpipeline: Sūtra-Statusmaschine, Fuzzy Matching, adaptive Typografie und TEI-P5-Strukturierung.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="case-study/" class="quick-btn quick-btn-outline">
        <span>➔</span> Editions-Delta lesen
      </a>
    </div>
  </div>
</div>

---

## 🌟 Über das Projekt & Verfahrensabgrenzung

Dieses Projekt umfasst die vollständige historische Erschließung, multimodale KI-Vollerfassung (Mistral OCR), das lückenlose kanonische Alignment gegen den Aṣṭādhyāyī Sūtrapāṭha sowie die Erstellung standardkonformer digitaler Editionsartefakte für Otto von Böhtlingks maßgebliche Pāṇini-Ausgabe von 1887 auf Basis der Digitalisate der Universitätsbibliothek Heidelberg.

> ℹ️ **Verfahrens-Verbindung zur AlexandriaSandwich-Pipeline:**  
> Alle generischen Schritte der Bildverarbeitung, des IIIF-Cachings, der multimodalen KI-OCR (`mistral-ocr-latest`), des Content-Aware Margin Maskings (`#f0e8d6`) sowie der Erzeugung von 1:1 Sandwich-PDFs basieren auf der zentralen Buch-Digitalisierungs-Pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**.  
>  
> Für die detaillierte Beschreibung des allgemeinen Verfahrens verweisen wir auf die zentrale Dokumentation:  
> 👉 **[AlexandriaSandwich Verfahrensdokumentation](https://birchville-org.github.io/AlexandriaSandwich/de/WIKI_VERFAHREN/)**  
>  
> Das vorliegende Repository `boethlingk` konzentriert sich ausschließlich auf das **spezifische philologische und typografische Editions-Delta** (kanonische Statusmaschine, 1:1-Seitenparität, STIX Two Text Schriftstack, TEI-P5-Auszeichnung).

---

## 🏛️ Die digitalen Editions-Artefakte im Überblick

Alle druck- und archivfertigen Ausgabedateien stehen über die offizielle GitHub-Release-Seite zum Download bereit:

* **1:1 Faksimile-Neusatz (Vektor-PDF):** `boethlingk1887_facsimile_dense.pdf` (8,58 MB · 484 Seiten)  
  Exakte 1:1-Seitenkongruenz mit dem Leipziger Original von 1887, adaptive Typografie, STIX Two Text Fontstack mit fehlerfreien IAST-Kapitälchen (**PĀṆINI**, **MAHĀBHĀṢYA**).  
  [:octicons-download-16: Release-Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_facsimile_dense.pdf)

* **Modernisierte Typst-Buchausgabe (Vektor-PDF):** `boethlingk1887_typeset_edition.pdf` (8,81 MB · 512 Seiten)  
  Fließendes Buchlayout im ISO B5-Format für das kontinuierliche philologische Studium.  
  [:octicons-download-16: Release-Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition.pdf)

* **1:1 Sandwich-PDF (Scan-Faksimile):** `boehtlingk1887_sandwich.pdf` (248,8 MB · 478 Seiten)  
  Hochauflösendes Heidelberg-Faksimile mit Content-Aware Margin Masking und unsichtbarer OCR-Textebene (14.267 Textblöcke).  
  [:octicons-download-16: Release-Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf)

* **Kanonischer Master-Datensatz (JSON):** `data/ashtadhyayi_complete_boethlingk1887.json` (2,85 MB)  
  3.997 Sūtras lückenlos (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras, 0 Duplikate, 0 Fehlstellen) mit Devanāgarī, IAST, Übersetzung und fortlaufendem Kommentar.  
  [:octicons-mark-github-16: Im Repository ansehen](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

* **Schema-valide TEI-P5 XML-Edition:** `data/tei/boehtlingk1887_p5.xml` (2,90 MB)  
  100 % valide gegen TEI All RelaxNG (`schemas/tei_all.rng`) mit 478 `<pb>`-Tags zu den Heidelberger IIIF-Faksimiles.  
  [:octicons-mark-github-16: Im Repository ansehen](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml)

* **Reflowable EPUB 3 eBook:** `boethlingk1887.epub` (1,47 MB)  
  Mobiles E-Book mit Schrifteinbettung (*Noto Serif Devanagari*) und voll gegliedertem Inhaltsverzeichnis.  
  [:octicons-download-16: Release-Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub)

* **Autarker QA-Viewer:** `viewer.html` (39 KB)  
  Split-Pane-Editor nach Payer-Standard für browserbasierte lokale Korrektur direkt auf der Festplatte.  
  [:octicons-eye-16: Im Repository ansehen](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)

👉 **Ausführliche Dokumentation aller Artefakte:** [Editions-Artefakte & Downloads](artifacts.md)

---

## 🏛️ Pipeline- & Editions-Architektur

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ALEXANDRIASANDWICH (GENERISCHE HAUPTPIPELINE)              │
│  [UB Heidelberg IIIF] ──► [Mistral KI-OCR] ──► [Margin Masking #f0e8d6]│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Bounding-Boxes, Layout & Faksimiles
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             BÖHTLINGK-DELTA (KANONISCHE EDITIONS-SCHICHT)              │
│  [Schritt 1: Kanonisches Alignment] ──► scripts/align_mistral_sutras.py│
│         │                               (8-Adhyāya-Statusmaschine)     │
│         ▼                                                              │
│  [Schritt 2: Master-Konsolidierung] ──► ashtadhyayi_complete_...json  │
│         │                               (3.997 Sūtras lückenlos)       │
│         ▼                                                              │
│  [Schritt 3: Editions-Assembly]     ──► boethlingk1887_facsimile_dense │
│                                         boehtlingk1887_p5.xml (TEI)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📖 Dokumentationsübersicht

* [📦 Editions-Artefakte & Downloads](artifacts.md) – Alle Ausgabedateien im Detail mit Release-Links
* [🔍 Das Böhtlingk-Delta & Methodik](case-study.md) – Methodische Differenzierung und Rechtfertigung des Editionsprojekts
* [🛠️ QA- & Korrektur-Workflow](qa-workflow.md) – Single Source of Truth & lokale Korrektur im QA-Viewer
* [🏛️ Datenarchitektur](data-architecture.md) – Das 3-Schichten-Datenmodell
* [📜 Urheberrecht & Provenienz](copyright-and-provenance.md) – Quellennachweise der UB Heidelberg
* [📐 Konventionen](conventions.md) – Transliterations- und Codierungsstandards
