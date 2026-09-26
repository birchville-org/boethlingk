# Pipeline-Entscheidungen — boethlingk

## 1. IIIF-first: kein lokales Bildarchiv

Entscheidung: Bilder bleiben auf dem Heidelberger Server, kein lokaler Download.

Begruendung:
- UB Heidelberg betreibt stabilen IIIF-Server mit 877 Seiten
- TEI pb/@facs referenziert IIIF-URL direkt → kein Dateipfad-Problem
- IIIF Image API liefert Bildausschnitte pro Zeile/Sutra on-demand
- Spart ~2-3 GB lokalen Speicher

Vorbehalt: Offline-Betrieb erfordert lokalen IIIF-Mirror (cantaloupe).
Aufgeschoben bis konkreter Bedarf besteht.

## 2. ALTO-direkt statt eScriptorium

Entscheidung: ALTO-XML direkt von Heidelberg als OCR-Grundlage.
kein eScriptorium fuer den initialen OCR-Abruf.

Begruendung:
- Heidelberg liefert bereits ALTO-XML mit Pixelkoordinaten (HPOS/VPOS)
- 877 Dateien vollstaendig abrufbar via scripts/fetch_alto.py
- eScriptorium waere nur noetig fuer eigenes OCR-Training
- Unnoetige Komplexitaet vermeiden bis Sanskrit-Problem klar ist

eScriptorium bleibt Option fuer Phase 2.5 (INSERTED) falls Sanskrit-Training noetig.

## 3. pplx-Pipeline: Wiederverwendung

Entscheidung: pplx/panini_pipeline/ unveraendert wiederverwenden.

Was wiederverwendet wird:
- fetch.py: IIIF-Client + ALTO-Parser + OcrLine-Objekte
- segment.py: Seitenstruktur-Erkennung (Sutra/Kommentar/Fussnote/Kapitel)
- corrections.py: OCR-Korrekturregeln (Deutsch/Sanskrit/Bohtlingk-spezifisch)
- render.py: HTML-Ausgabe (Gleis A)

Was nicht wiederverwendet wird:
- cli.py: wird durch GSD-Workflow-Skripte ersetzt
- goldstandard-Workflow: ersetzt durch TEI-Mastertext-Ansatz

## 4. GRETIL als Sutra-Primaerquelle

Entscheidung: Sutra-Text (Devanagari/IAST) nicht aus Heidelberger OCR,
sondern aus GRETIL-Datenbank (Uni Gottingen).

Begruendung:
- Heidelberger Devanagari-OCR ist unbrauchbar (Kauderwelsch-Zeichen)
- GRETIL hat alle ~4000 Sutras maschinenlesbar in IAST
- Sutra-Referenz (1.1.37) aus Heidelberger Seitenkopf als Schluessel

Umsetzung: Phase 3 (03-01: GRETIL Sutra-Daten importieren).

## 5. Zwei-Gleise-Strategie

Gleis A (schnell, parallel nutzbar):
  pplx-Pipeline → HTML-Leseedition des deutschen Kommentartexts
  Qualitat: gut fuer Fliesstext, schlecht fuer Devanagari
  Nutzen: schnelles Ergebnis, Smoke-Test, editorische Vorkontrolle
  Start: Phase 2 (Plan 02-03)

Gleis B (Mastertext, Hauptziel):
  ALTO-XML → TEI-Transformation → Sutra-verankerte Edition
  Qualitat: vollstaendig, GRETIL-gestuetzt, bildverankert
  Nutzen: zitierfahig, maschinenlesbar, Erstedition
  Start: Phase 3-4

## 6. Offene Entscheidungen

Sanskrit-Qualitat (Phase 2):
  Frage: Reicht GRETIL-Mapping fuer alle Sutras, oder gibt es Luecken?
  Entscheidung nach Phase 2 OCR-Qualitatsanalyse und GRETIL-Abdeckungspruefung.

TEI-Schema-Tiefe (Phase 4):
  Frage: Minimales TEI oder vollstaendiger kritischer Apparat?
  Empfehlung: zunachst minimal (pb, milestone, seg, note), spaeter erweiterbar.

eScriptorium (offen):
  Trigger: falls GRETIL-Abdeckung < 80% oder manuelle Sutra-Korrektur noetig.
  Dann: Phase 2.5 (INSERTED) mit eScriptorium-Setup und Kraken-Training.

JSON-API (Phase 5):
  Frage: Nur TEI+HTML, oder auch JSON fuer maschinelle Weiternutzung?
  Relevant fuer Verlinkung mit Cologne CDSL und Sanskrit Heritage Site.
