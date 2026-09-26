# Datenarchitektur — boethlingk

## Projektstruktur

```
boethlingk/
├── pplx/                        Vorhandene Pipeline (Gleis A, unveraendert)
│   ├── panini_pipeline/
│   │   ├── fetch.py             IIIF-Client, ALTO-Parser, OcrLine-Objekte
│   │   ├── segment.py           Seitenstruktur-Erkennung (Sutra/Kommentar/etc.)
│   │   ├── render.py            HTML-Ausgabe via Jinja2
│   │   ├── rules/corrections.py OCR-Korrekturregeln (Deutsch/Sanskrit/Bohtlingk)
│   │   └── templates/           HTML-Templates + CSS
│   └── cache/                   Manifest + 30 gecachte OCR-Seiten (Text + Metadaten)
│
├── data/
│   ├── alto/                    ALTO-XML von Heidelberg (877 Dateien, Layer 2)
│   ├── tei/                     TEI-Master (Layer 3, Ziel)
│   ├── html/                    HTML-Ausgaben (Gleis A)
│   └── ground-truth/            Manuell korrigierte Passagen (optional)
│
├── scripts/
│   ├── fetch_alto.py            Batch-Abruf ALTO-XML (erledigt)
│   └── alto_to_tei.py           ALTO→TEI Transformation (Phase 4)
│
├── docs/
│   ├── conventions.md           ID-Schema, Dateinamen, Koordinaten
│   ├── data-architecture.md     Dieses Dokument
│   └── pipeline-decisions.md    Architekturentscheidungen mit Begruendung
│
└── .planning/                   GSD-Workflow (Roadmap, Plans, State)
```

## Drei-Layer-Modell

```
Layer 1 — Bildbasis
  Quelle:  IIIF Image API, UB Heidelberg
  URL:     https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/...
  Zugriff: per URL, kein lokaler Download
  Zweck:   Bildverankerung im TEI (pb/@facs), IIIF-Crop pro Zeile/Sutra

Layer 2 — ALTO-XML (koordinatenverankertes OCR)
  Quelle:  UB Heidelberg (Heidelberger OCR-Produktion)
  Ablage:  data/alto/alto_{NNNN}.xml  (877 Dateien)
  Inhalt:  TextLine-Elemente mit HPOS/VPOS/WIDTH/HEIGHT + Worttext
  Qualitat: Deutsch gut, Devanagari unbrauchbar (→ GRETIL als Ersatz)
  Umfang:  865 Seiten mit Text, 12 Leerseiten, 36.942 TextLines gesamt

Layer 3 — TEI/XML Mastertext
  Ablage:  data/tei/boehtlingk1887.tei.xml
  Inhalt:  Sutra-verankerte Edition (pb, milestone, seg, note)
  Quelle:  ALTO Layer 2 + GRETIL Sutra-Referenzdaten
  Status:  noch nicht erstellt (Phase 4)
```

## Transformationspipelines

```
Pipeline A — Gleis A (schnell, HTML):
  pplx/cache/manifest.json
    → fetch.py: OcrPage-Objekte (Text + Koordinaten)
    → segment.py: StructuredPage (Sutra/Kommentar/Fussnote/...)
    → corrections.py: bereinigter Text
    → render.py: HTML-Leseedition
    → data/html/book.html

Pipeline B — Gleis B (Mastertext, TEI):
  data/alto/alto_{NNNN}.xml
    → scripts/alto_to_tei.py: TEI-Fragmente pro Seite
    → GRETIL Sutra-DB: korrekter Devanagari/IAST-Text
    → data/tei/boehtlingk1887.tei.xml

Pipeline C — Ausgaben aus TEI:
  data/tei/boehtlingk1887.tei.xml
    → HTML-Leseansicht (Sutra + Kommentar + Bildlink)
    → Such-PDF
    → JSON/Plaintext-Export
```

## ALTO-Korpus — Kennzahlen (Stand nach Plan 01-02)

| Kennzahl              | Wert       |
|-----------------------|------------|
| Seiten gesamt         | 877        |
| Seiten mit Text       | 865        |
| Leerseiten            | 12         |
| TextLines gesamt      | 36.942     |
| Ø TextLines/Seite     | 42         |
| Parse-Fehler          | 0          |
| ALTO-Groesse gesamt   | ~data/alto |

## Offene Fragen (Stand Phase 1)

1. Sanskrit-Qualitat: Heidelberger Devanagari-OCR ist unbrauchbar.
   Losung: GRETIL-Sutra-Datenbank als Primaerquelle fur Sutra-Text einbinden.
   Entscheidung faellt in Phase 2 (OCR-Qualitatsanalyse).

2. TEI-Schema-Tiefe: Minimales TEI (pb, milestone, p) oder vollstaendiges
   kritisches Apparat (choice, unclear, supplied)?
   Entscheidung faellt in Phase 4 (TEI-Schema-Definition).

3. eScriptorium: Aufgeschoben. Nur relevant falls eigenes OCR-Modell
   fuer Sanskrit trainiert werden soll. Nach Phase 2-Evaluation entscheiden.

4. Ausgabeformate: HTML und TEI sicher. JSON-API fuer maschinelle
   Weiternutzung (z.B. Verlinkung mit GRETIL/Cologne) pruefen.
