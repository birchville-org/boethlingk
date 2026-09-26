# Konventionen — boethlingk

## Datenbasis

Kein lokales Bildarchiv. Alle Bilder und OCR-Daten kommen vom
IIIF-Server der UB Heidelberg:

  Manifest (v3): https://digi.ub.uni-heidelberg.de/diglit/iiif3/boehtlingk1887/manifest
  Umfang: 877 Seiten
  IIIF-Format: v3 (items[])
  ALTO-XML: pro Seite via canvas.annotations[].id abrufbar

Bild-URL-Muster (aus Manifest):
  https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/full/max/0/default.jpg

## ID-Schema

Seitenindex: 0-based, entspricht Position im Manifest (items[index])
  Seite 0   = Titelblatt
  Seite 26  = Textseite 1 (label "1")
  Seite 876 = letzte Seite

Dateinamen:
  ALTO-XML:     data/alto/alto_{NNNN}.xml      (z.B. alto_0026.xml)
  TEI pro Band: data/tei/boehtlingk1887.tei.xml (ein Gesamt-TEI)
  HTML-Ausgabe: data/html/book.html

Sutra-Referenz: Adhyaya.Pada.Sutra  →  z.B. "1.1.37"
  Quelle: Heidelberger Seitenkopf ("1, 1, 37." → normalisiert "1.1.37")
  Verwendung in TEI: <milestone unit="sutra" n="1.1.37"/>
  Kreuzreferenz: GRETIL Gottingen (paniniiu.htm)

## Koordinatensystem (ALTO)

ALTO-Koordinaten beziehen sich auf die Bildgroesse der jeweiligen Seite:
  alto_page_width  / alto_page_height: Pixelabmessungen (z.B. 2238x3548)
  hpos / vpos:  Pixel-Koordinaten der Textzeile (oben links)
  width / height: Abmessungen der Textzeile in Pixeln

Beispiel Seite 26 (label "1"):
  ALTO: 2238 x 3548 Pixel
  Erste Zeile: hpos=778 vpos=930 (Sanskrit-Sutra, Zeile 1)

IIIF-Crop-URL pro Zeile (aus fetch.py / iiif_region()):
  {iiif_service}/pct:{x},{y},{w},{h}/full/0/default.jpg

## TEI-Referenzierung

TEI pb-Element pro Seite:
  <pb n="{label}" facs="{iiif_image_url}"/>

Beispiel:
  <pb n="1" facs="https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3A000000001.jpg/full/max/0/default.jpg"/>

Sutra als milestone:
  <milestone unit="sutra" n="1.1.1"/>

Sprachkennzeichnung:
  xml:lang="de"         Deutscher Kommentartext (Heidelberger OCR: gut)
  xml:lang="sa"         Sanskrit Devanagari (korrekt erkannt)
  xml:lang="sa-x-ocr"  Sanskrit aus OCR (Devanagari als Kauderwelsch, unkorrigiert)
  xml:lang="sa-Latn"   Sanskrit in IAST-Transliteration (aus GRETIL)

## Zwei-Gleise-Strategie

Gleis A — schnell, Deutsch:
  pplx/panini_pipeline/ (fetch + segment + render) → data/html/
  Qualitat: gut fuer deutschen Kommentartext
  Schwache: Devanagari-OCR unbrauchbar (Heidelberger Artefakt)
  Einsatz: Smoke-Test, Leseedition Phase 2

Gleis B — Mastertext:
  data/alto/ → scripts/alto_to_tei.py → data/tei/
  Ziel: Sutra-verankerte TEI-Edition mit IIIF-Bildlinks
  Sutra-Devanagari: aus GRETIL-DB einbinden (nicht aus OCR)

## IIIF-Entscheidung

Option A (gewaehlt): IIIF-first, kein lokaler Bild-Download
  Bilder bleiben auf Heidelberger Server, TEI pb/@facs referenziert direkt
  Vorteil: kein Speicherplatz, immer aktuell
  Nachteil: Offline-Betrieb erfordert lokalen IIIF-Mirror

eScriptorium: aufgeschoben — nur falls eigenes OCR-Training fuer Sanskrit
noetig wird. Erst Sanskrit-Qualitat aus Heidelberger ALTO evaluieren (Phase 2).
