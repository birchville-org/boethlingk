# Conventions & Technical Specifications — boethlingk

## 1. Primary Data Source

All facsimile imagery is sourced via the IIIF Image API from Heidelberg University Library:
* **Manifest (v3):** `https://digi.ub.uni-heidelberg.de/diglit/iiif3/boehtlingk1887/manifest`
* **Total Extent:** 877 pages (Book pages 1–478 cover the main text, Śiva-Sūtras, and addenda)
* **IIIF Image URL Scheme:**
  `https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3ANNNNNNNNN.jpg/full/max/0/default.jpg`

---

## 2. ID & Numbering Scheme

* **Page Index:** 0-based index corresponding to manifest order (`items[index]`).
  * Index 0 = Title page
  * Index 26 = Book page 1 (label `"1"`, Śiva-Sūtras)
* **Sūtra Reference Scheme:** `Adhyāya.Pāda.Sūtra` (e.g. `1.1.1` to `8.4.68`).
  * In TEI P5: `<milestone unit="sutra" n="1.1.1"/>` and `<entry xml:id="sutra-1.1.1">`
  * In Master JSON: Keyed by `"id": "1.1.1"`

---

## 3. Language Tagging (BCP 47 & TEI)

* `de` / `xml:lang="de"`: German translation and commentary.
* `sa` / `xml:lang="sa"`: Canonical Sanskrit in Devanāgarī.
* `sa-Latn` / `xml:lang="sa-Latn"`: Sanskrit in academic IAST transliteration.

---

## 4. TEI Page Referencing

Each page transition in the TEI edition links directly to Heidelberg's IIIF high-resolution facsimile:
```xml
<pb n="1" facs="https://digi.ub.uni-heidelberg.de/iiif/3/boehtlingk1887%3A000000001.jpg/full/max/0/default.jpg"/>
```
