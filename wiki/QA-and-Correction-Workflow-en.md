> 🌐 **Language / Sprache:** [🇬🇧 English](QA-and-Correction-Workflow-en) | [🇩🇪 Deutsch](QA-and-Correction-Workflow)

# 🛠️ QA & Correction Workflow

This guide explains how to collate, correct, and synchronize OCR readings, editorial notes, or diacritical fixes across all digital edition artifacts (Typst book PDF, TEI-P5 XML, and 1:1 Sandwich PDF) in the `boethlingk` project.

---

## 🏛️ Architecture: Single Source of Truth

All corrections are made in **one central place only**:  
👉 [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

Never edit generated output files directly (such as XML or PDF), because those are automatically overwritten during build runs.

```text
                               ┌────────────────────────┐
                               │       Correction       │
                               │   in Master JSON File  │
                               └───────────┬────────────┘
                                           │
                     ┌─────────────────────┼─────────────────────┐
                     ▼                     ▼                     ▼
        scripts/build_typeset_edition.py   │          scripts/generate_tei_p5.py
                     │                     │                     │
                     ▼                     │                     ▼
        [boethlingk1887_typeset.pdf]       │           [boehtlingk1887_p5.xml]
               (Typeset Book PDF)          │             (Archival TEI RelaxNG)
                                           ▼
                              scripts/build_sandwich_pdf.py
                                           │
                                           ▼
                             [boehtlingk1887_sandwich.pdf]
                                  (1:1 Facsimile PDF)
```

---

## 🔍 Path 1: Visual Collation with the QA Viewer (Recommended)

The repository provides [`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html), an offline split-pane editor conforming to the Payer Global Web Editor Standard.

### 1. Start Local Server
Due to browser security policies regarding local files, run a simple local web server:
```bash
python3 -m http.server 8000
```
Open in your browser: `http://localhost:8000/viewer.html`

### 2. Editor Features & Usage
- **Left Pane (Facsimile Inspection):** Displays the high-resolution Heidelberg University Library scans with smooth zoom and pan.
- **Right Pane (Sūtra Data Fields):** Directly edit the current Sūtra fields:
  - `canonical_devanagari`: Devanāgarī text
  - `canonical_iast`: Scholarly transliteration
  - `translation`: German translation by Otto Böhtlingk (1887)
  - `commentary`: Philological apparatus and citations
- **Snippet Toolbar:** Quick-insert buttons for Dandas (`॥`) and IAST diacritics (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`, `ṃ`, `ḥ`).
- **Navigation:** Browse Sūtras using keyboard arrow keys or navigation buttons.

### 3. Save with Silent Auto-Repair
- Press `Cmd+S` / `Ctrl+S` or click **"Save (JSON)"**.
- The editor silently repairs formatting discrepancies and directly writes the updated dataset back to `data/ashtadhyayi_complete_boethlingk1887.json` using the *File System Access API*.

---

## ⌨️ Path 2: Direct Editing in Code Editor

If you already know the specific Sūtra reference (e.g., `1.1.4`):

1. Open `data/ashtadhyayi_complete_boethlingk1887.json` in your editor.
2. Search for `"ref": "1.1.4"`.
3. Adjust the fields:
   ```json
   {
     "ref": "1.1.4",
     "adhyaya": 1,
     "pada": 1,
     "sutra_num": 4,
     "page": 2,
     "canonical_devanagari": "न धातुलोप आर्धधातुके",
     "canonical_iast": "na dhātulopa ārdhadhātuke",
     "translation": "Corrected translation here...",
     "commentary": "Corrected commentary here..."
   }
   ```
4. Save the file.

---

## ⚡ Step 3: Recompile Output Artifacts

Run the build commands from your terminal:

### 1. Rebuild Typeset Book PDF (Takes ~0.9 seconds)
```bash
python3 scripts/build_typeset_edition.py
```
Produces the complete 737-page vector PDF:  
👉 `data/output/boethlingk1887_typeset_edition.pdf`

### 2. Regenerate & Validate TEI-P5 XML Edition (Takes ~3 seconds)
```bash
python3 scripts/generate_tei_p5.py
```
Updates `data/tei/boehtlingk1887_p5.xml` and validates it against `schemas/tei_all.rng`.

### 3. (Optional) Rebuild 1:1 Sandwich PDF
```bash
python3 scripts/build_sandwich_pdf.py \
  --img-dir data/img_cache \
  --mistral-dir data/mistral \
  --master-json data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/output/boehtlingk1887_sandwich.pdf
```

---

## 🚀 Step 4: Verify & Commit

1. Run integrity check:
   ```bash
   python3 -c "
   import json
   with open('data/ashtadhyayi_complete_boethlingk1887.json', encoding='utf-8') as f:
       d = json.load(f)
   assert len(d['shiva_sutras']) == 14
   assert len(d['sutras']) == 3983
   print('Integrity: 100% OK')
   "
   ```

2. Commit and push:
   ```bash
   git add data/ashtadhyayi_complete_boethlingk1887.json data/tei/boehtlingk1887_p5.xml
   git commit -m "fix(sutra): correct reading and commentary for sutra 1.1.4"
   git push origin main
   ```
