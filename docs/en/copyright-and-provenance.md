# ⚖️ Copyright, Public Domain & Provenance

This document explains the legal status of Otto von Böhtlingk's 1887 edition, the copyright status of the digital scans provided by Heidelberg University Library, the rationale and implementation of removing library watermark stamps, and the standards of scholarly provenance and citation.

---

## 1. Public Domain Status of the Original Work

The underlying source work, **«Pâṇini's Grammatik»** by Otto von Böhtlingk (2nd edition, Leipzig 1887), is entirely in the **Public Domain**:

* **Author:** Otto von Böhtlingk (* June 11, 1815 in Saint Petersburg; † April 1, 1904 in Leipzig).
* **Statutory Term of Protection:** Under § 64 UrhG (Germany), Art. 9 URG (Switzerland), and Directive 2006/116/EC (EU), copyright protection expires 70 years after the author's death (*post mortem auctoris*).
* **Expiration Date:** 1904 + 70 years = expired on December 31, 1974.
* **Legal Consequence:** Since **January 1, 1975**, the work has been in the public domain. The Sanskrit text, German translation, scientific commentary, and critical notes may be freely reproduced, digitized, edited, modified, typeset, and republished by anyone for both non-commercial and commercial purposes.

---

## 2. Status of the 2D Digital Facsimiles (Heidelberg University Library)

For optical collation and text alignment (OCR & alignment pipeline), scans provided by Heidelberg University Library (UB Heidelberg) are utilized. These digital reproductions **do not create new intellectual property rights**:

### European and German Law (EU DSM Directive & § 68 UrhG)
* **EU Directive 2019/790 (DSM Directive), Article 14:**
  > *"Member States shall provide that, when the term of protection of a work of visual art has expired, any material resulting from an act of reproduction of that work is not subject to copyright or related rights [...]"*
* **German Copyright Act (§ 68 UrhG - Reproductions of Public Domain Visual Works):**
  Faithful reproductions of out-of-copyright works do not enjoy related rights protection (§§ 70, 71, 72, or 73 UrhG).
* **Case Law on 2D Scans:** Merely technical 2D flatbed/scanner reproductions of printed text pages lack personal intellectual creativity (no original work under § 2 UrhG) and do not qualify for photographic related rights (§ 72 UrhG).

Consequently, extracting, cleaning, typesetting, and publishing the digitized text does not infringe any third-party copyrights.

---

## 3. Removal of Library Watermark Stamps

The digital scans from UB Heidelberg contain institutional margin stamps and funding watermarks:

```text
UNIVERSITÄTS-
BIBLIOTHEK
HEIDELBERG
Baden-Württemberg | GEFÖRDERT DURCH DIE DFG
```

### Legal Assessment
These stamps serve solely to identify the scanning institution and project funding. They do not constitute copyright in the 19th-century text. Removing these markings from the extracted textual body does not infringe on any intellectual property.

### Philological & Technical Rationale
In automated OCR pipelines, such marginal markings are inadvertently captured as text and interspersed into the Sūtra commentary. Full removal is essential for a clean scholarly edition:
* **Data Integrity:** Eliminates modern institutional boilerplate from Böhtlingk's original philological notes.
* **TEI-P5 Compliance:** The XML body (`<div type="commentary">`) must solely contain authentic text of the primary edition.
* **Cross-Page Commentary Continuity:** Commentaries spanning across page boundaries (e.g., Sūtra 1.1.58) must be stitched together seamlessly without interruption.

### Technical Implementation
Boilerplate filtering is handled deterministically in the pipeline scripts ([`scripts/align_mistral_sutras.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/align_mistral_sutras.py) and [`scripts/build_sandwich_pdf.py`](https://github.com/birchville-org/boethlingk/blob/main/scripts/build_sandwich_pdf.py)):

```python
# Excerpt from scripts/align_mistral_sutras.py:
def clean_commentary_paragraphs(text: str) -> list[str]:
    lines = text.split("\n")
    cleaned_lines = []
    in_block = False
    for l in lines:
        l_str = l.strip()
        if any(k in l_str.upper() for k in [
            "UNIVERSITÄTS", "BIBLIOTHEK", "HEIDELBERG",
            "BADEN-WÜRTTEMBERG", "GEFÖRDERT DURCH", "DIGI.UB"
        ]):
            in_block = True
            continue
        elif in_block:
            if re.match(r"^\d+$", l_str) or l_str in ["B", "b", ""]:
                continue
            else:
                in_block = False
                cleaned_lines.append(l)
        else:
            cleaned_lines.append(l)
    return cleaned_lines
```

---

## 4. Scholarly Provenance & Citation Standards

While the text is free of copyright restrictions, **good academic practice** requires transparent documentation of the digital source and provenance.

In the `boethlingk` project, provenance is explicitly documented in:

1. **TEI-P5 Header (`boehtlingk1887_p5.xml`):**
   ```xml
   <sourceDesc>
     <bibl xml:id="Boehtlingk1887">
       <author>Otto von Böhtlingk</author>
       <title>Pâṇini's Grammatik</title>
       <pubPlace>Leipzig</pubPlace>
       <publisher>Verlag von H. Haessel</publisher>
       <date when="1887">1887</date>
       <note type="digitization">
         Digitized by Heidelberg University Library.
         URN: urn:nbn:de:bsz:16-diglit-323605
         URL: https://digi.ub.uni-heidelberg.de/diglit/boethlingk1887
       </note>
     </bibl>
   </sourceDesc>
   ```

2. **Typeset Edition (`boethlingk1887_typeset_edition.pdf`):**
   The colophon lists the original 1887 publication details, publisher H. Haessel Leipzig, and UB Heidelberg as the facsimile source.

3. **Master JSON Metadata:**
   Each Sūtra entry references the exact facsimile page number in the Heidelberg digital repository.

---

## 5. Licensing of the New Edition

* **Primary Historical Text:** Public Domain.
* **Pipeline Code & TEI Modeling:** Released under the [MIT License](https://github.com/birchville-org/boethlingk/blob/main/LICENSE).
