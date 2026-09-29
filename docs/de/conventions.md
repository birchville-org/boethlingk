# 📐 Konventionen & Technische Spezifikationen — boethlingk

> Dieses Dokument definiert die Identifikationsschemata, Sprach-Kennzeichnungen und typografischen Konventionen des Projekts `boethlingk`.

---

## 1. Primäre Datenquelle

Alle Faksimile-Bilder stammen über die standardisierte IIIF Image API von der Universitätsbibliothek Heidelberg:
* **Manifest (v3):** `https://digi.ub.uni-heidelberg.de/diglit/iiif3/boehtlingk1887/manifest`
* **Gesamtumfang:** 877 Seiten (Buchseiten 1–478 umfassen den Haupttext, die Śiva-Sūtras und die Nachträge)
* **IIIF-Bild-URL-Muster:**
  `https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/full/max/0/default.jpg`

---

## 2. Identifikations- & Zählschema

### Seitenindex
* **0-basierter Index** entsprechend der Reihenfolge im IIIF-Manifest (`items[index]`):
  * Index 0 = Titelblatt
  * Index 26 = Buchseite 1 (Label `"1"`, Śiva-Sūtras)
  * Index 27 = Buchseite 2 (Aṣṭādhyāyī 1.1.1)
  * Index 503 = Buchseite 478 (Ende der Nachträge)

### Sūtra-Referenzschema
* **Struktur:** `Adhyāya.Pāda.Sūtra` (z. B. `1.1.1` bis `8.4.68`)
  * Im TEI-P5-XML: `<milestone unit="sutra" n="1.1.1"/>` und `<entry xml:id="sutra-1.1.1">`
  * Im Master-JSON: Identifiziert durch `"ref": "1.1.1"`
* **Śiva-Sūtras:** Nummeriert von `1` bis `14` (in JSON unter `shiva_sutras`)

---

## 3. Sprachkennzeichnung (BCP 47 & TEI)

* `de` / `xml:lang="de"`: Deutscher Übersetzungstext und philologische Kommentare von Otto von Böhtlingk.
* `sa` / `xml:lang="sa"`: Kanonischer Sanskrit-Text in Devanāgarī.
* `sa-Latn` / `xml:lang="sa-Latn"`: Sanskrit in wissenschaftlicher IAST-Transliteration.

---

## 4. TEI-Seitenreferenzierung

Jeder Seitenübergang in der TEI-P5-Edition ist mit dem hochauflösenden IIIF-Faksimile der UB Heidelberg verknüpft:
```xml
<pb n="1" facs="https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3A000000001.jpg/full/max/0/default.jpg"/>
```

---

## 5. Koordinatensystem & Bounding-Boxen (Sandwich-PDF)

* Mistral OCR (`mistral-ocr-latest`) liefert Bounding Boxes für erkannte Wörter und Zeilenblöcke (`data/mistral/*.mistral.json`).
* Die Koordinaten werden im Koordinatensystem der Heidelberger Faksimiles (Pixelabmessungen, z. B. 2.238 x 3.548 Pixel) berechnet.
* Beim PDF-Assembly ([`scripts/build_sandwich_pdf.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/build_sandwich_pdf.py)) werden die Koordinaten in PDF-Punkte umgerechnet und mit PDF Text Rendering Mode 3 (*Neither fill nor stroke text*) deckungsgleich über die gedruckten Glyphen gelegt.
