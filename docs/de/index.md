<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--md-default-bg-color--light); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;">
  <img src="assets/birchville_logo.png" alt="Birchville Wappen" style="height: 2.4rem; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18));">
  <div>
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--md-accent-fg-color); font-weight: 700;">Birchville Scholarly Synthesis</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--md-default-fg-color);">Kanonische Editionen klassischer philologischer Referenzwerke</div>
  </div>
</div>

# 📖 Pāṇinis Grammatik (Otto von Böhtlingk, Leipzig 1887)

**Wissenschaftliche Digitalisierung, kanonisches Alignment, TEI-P5-Edition und 1:1 Sandwich-PDF der *Grammatik des Pāṇini* (Otto von Böhtlingk, 2. Auflage, Leipzig 1887).**

---

## ⚡ Schnellzugriff & Downloads

<div class="quick-access-grid">
  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📚</span>
        <span class="quick-card-title">Sandwich-PDF (1:1)</span>
      </div>
      <div class="quick-card-body">
        478 Seiten historisches Originalscan-Faksimile mit Content-Aware Margin Masking, OCR-Textebene (14.267 Textblöcke) und 42 Lesezeichen.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf" class="quick-btn quick-btn-primary" target="_blank" rel="noopener">
        <span>⬇️</span> Sandwich-PDF (249 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📄</span>
        <span class="quick-card-title">Typst-Vektorsatz v2</span>
      </div>
      <div class="quick-card-body">
        Moderner Vektorbuchsatz (ISO B5) mit allen 3.997 Sūtras, Übersetzung, Kommentar, 47 TOC-Lesezeichen und lebenden Kolumnentiteln.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition_v2.pdf" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>⬇️</span> Buchausgabe v2 (7,6 MB)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🏛️</span>
        <span class="quick-card-title">Wissenschaftliche Fallstudie</span>
      </div>
      <div class="quick-card-body">
        End-to-End-Verfahrensdokumentation der AlexandriaSandwich-Pipeline und des kanonischen Alignments.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="case-study/" class="quick-btn quick-btn-outline">
        <span>➔</span> Fallstudie lesen
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">💻</span>
        <span class="quick-card-title">Quellcode & Pipeline</span>
      </div>
      <div class="quick-card-body">
        Kanonischer JSON-Masterdatensatz, RelaxNG-validiertes TEI-P5 XML und Build-Skripte auf GitHub.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/boethlingk" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>➔</span> GitHub Repository
      </a>
    </div>
  </div>
</div>

---

## 🌟 Über das Projekt

Dieses Projekt umfasst die vollständige historische Erschließung, multimodale KI-Vollerfassung (Mistral OCR), das lückenlose kanonische Alignment gegen den Aṣṭādhyāyī Sūtrapāṭha sowie die Erstellung standardkonformer digitaler Editionsartefakte für Otto von Böhtlingks maßgebliche Pāṇini-Ausgabe von 1887 auf Basis der Digitalisate der Universitätsbibliothek Heidelberg.

> ℹ️ **Case Study:** Dieses Projekt ist eine Referenz-Fallstudie zur Open-Source-Digitalisierungs-Pipeline **[AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich)**.

---

## 🏛️ Projektergebnisse & Kernartefakte

- **Durchsuchbares 1:1 Sandwich-PDF** (`boehtlingk1887.perfect_sandwich.pdf` / `boehtlingk1887_sandwich.pdf` · 249 MB)  
  478 Seiten hochauflösendes Scan-Faksimile mit Content-Aware Margin Masking, unsichtbarer Vektor-Textebene (14.267 Textblöcke auf exakten Pixelkoordinaten) und 42 hierarchischen PDF-Bookmarks.  
  [:octicons-download-16: Release-Download (249 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boehtlingk1887_sandwich.pdf) · [:octicons-tag-16: GitHub Release](https://github.com/birchville-org/boethlingk/releases/latest)

- **Neu gesetztes Buch-PDF (Typst-Edition v2)** (`boethlingk1887_typeset_edition_v2.pdf` · 7,6 MB)  
  737 Seiten gestochen scharfer, moderner Vektorbuchsatz (ISO B5) mit allen 3.997 Sūtras (Devanāgarī, IAST, Übersetzung, Kommentar), lebenden Kolumnentiteln und 47 PDF-Bookmarks.  
  [:octicons-download-16: Release-Download (7,6 MB)](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887_typeset_edition_v2.pdf) · [:octicons-mark-github-16: Build-Skript](https://github.com/birchville-org/boethlingk/blob/main/scripts/build_typeset_edition.py)

- **Kanonisch validierter Master-Datensatz (JSON)** (`data/ashtadhyayi_complete_boethlingk1887.json` · 2,8 MB)  
  3.997 Sūtras lückenlos (14 Śiva-Sūtras + 3.983 Aṣṭādhyāyī-Sūtras, 0 Duplikate, 0 Fehlstellen) mit Devanāgarī, IAST-Transliteration, Übersetzung und fortlaufendem Kommentar.  
  [:octicons-mark-github-16: Datei auf GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

- **Schema-valide TEI-P5 XML-Edition** (`data/tei/boehtlingk1887_p5.xml` · 2,9 MB)  
  100 % valide gegen das offizielle TEI All RelaxNG Schema (`schemas/tei_all.rng`) mit 478 `<pb>`-Seitenumbrüchen mit Verknüpfung zu den IIIF-Vollbildern der UB Heidelberg.  
  [:octicons-mark-github-16: Datei auf GitHub](https://github.com/birchville-org/boethlingk/blob/main/data/tei/boehtlingk1887_p5.xml)

- **Reflowable EPUB 3 eBook mit Schrifteinbettung** (`boethlingk1887.epub` · 1,5 MB)  
  Standardisiertes EPUB 3 mit responsivem Layout, hierarchischem Inhaltsverzeichnis und Schrifteinbettung (*Noto Serif Devanagari*, *Linux Libertine O*).  
  [:octicons-download-16: Release-Download](https://github.com/birchville-org/boethlingk/releases/latest/download/boethlingk1887.epub) · [:octicons-mark-github-16: Export-Skript](https://github.com/birchville-org/boethlingk/blob/main/scripts/export_epub.py)

- **Autarker QA-Viewer** (`viewer.html`)  
  Split-Pane-Editor nach Payer-Standard mit Faksimile-Zoom/Pan, Snippet-Toolbar und lokalem Silent Auto-Repair beim Speichern.  
  [:octicons-eye-16: Viewer im Repository](https://github.com/birchville-org/boethlingk/blob/main/viewer.html)

---

## 🏛️ Pipeline-Architektur

```text
[UB Heidelberg Faksimiles] 
       │ (Buchseiten 1 bis 478, JPG)
       ▼
[Schritt 1: Lokales Image Caching] ──► data/img_cache/7_3A000000XXX_...jpg
       │
       ▼
[Schritt 2: Multimodale KI-OCR] ────► mistral-ocr-latest (Mistral Python SDK)
       │                              ├── data/mistral/*.mistral.md   (Layout-Markdown)
       │                              └── data/mistral/*.mistral.json (Bounding-Box Geometrie)
       ▼
[Schritt 3: Kanonisches Alignment] ──► scripts/align_mistral_sutras.py
       │                              ├── Heuristische Sūtra-Segmentierung (#, ##, ॥...॥)
       │                              ├── SequenceMatcher-Abgleich gegen data/sutras.json
       │                              ├── 4-Pāda-pro-Adhyāya Statusmaschine
       │                              └── Kolophon- und Rauschfilterung
       ▼
[Schritt 4: Konsolidierung] ─────────► data/ashtadhyayi_complete_boethlingk1887.json
       │                              (3.997 Sūtras = 100,0 % lückenlos & 0 Duplikate)
       ▼
[Schritt 5: TEI-, Sandwich- & ───────► data/tei/boehtlingk1887_p5.xml
            Typst-Assembly]            data/output/boehtlingk1887_sandwich.pdf
                                       data/output/boethlingk1887_typeset_edition.pdf
```

---

## 🚀 Schnellstart

### TEI-P5 XML generieren und validieren
```bash
uv run --with lxml python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### 1:1 Sandwich-PDF kompilieren
```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

### Neu gesetztes Buch-PDF kompilieren (Typst)
```bash
python3 scripts/build_typeset_edition.py
```

---

## 📖 Dokumentationsübersicht

* [Wissenschaftliche Fallstudie (Verfahrensdokumentation)](case-study.md)
* [Datenarchitektur & Drei-Layer-Modell](data-architecture.md)
* [Konventionen & IIIF-Spezifikation](conventions.md)
* [Wiki-Übersicht](wiki-home.md)

---

## 📜 Lizenz & Urheberschaft

- **Historisches Originalwerk**: Otto von Böhtlingk (1815–1904), *Pâṇini's Grammatik*, 2. Auflage, Leipzig 1887 (Public Domain).
- **Digitaler Neusatz, TEI-P5 & Pipeline**: [MIT License](https://github.com/birchville-org/boethlingk/blob/main/LICENSE) (Copyright (c) 2026 Marco Demarmels / Birchville Foundation).
- **Referenzprojekte**:
  - [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich) — Hybrid-OCR und Buchdigitalisierung
  - [macdonell](https://github.com/birchville-org/macdonell) — A Vedic Grammar for Students (1916) 1:1 Neusatz
  - [sanskritkurs-payer](https://github.com/birchville-org/sanskritkurs-payer) — Digitaler Payer-Sanskritkurs
