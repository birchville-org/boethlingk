# 🛠️ QA & Correction Workflow

This guide explains how to collate, correct, and synchronize OCR misreadings, typos, or diacritical inaccuracies across all digital edition artifacts (Typst book PDF, TEI-P5 XML, and 1:1 Sandwich PDF) in the `boethlingk` project.

---

## 🏛️ Architecture Principle: Single Source of Truth

All corrections are made **strictly in one central location**:
👉 [`data/ashtadhyayi_complete_boethlingk1887.json`](https://github.com/birchville-org/boethlingk/blob/main/data/ashtadhyayi_complete_boethlingk1887.json)

Manual edits in generated output files (such as XML or PDF) must be avoided, as these files are automatically and deterministically overwritten during each build cycle.

```text
                               ┌────────────────────────┐
                               │     Correction in      │
                               │   Master JSON File     │
                               └───────────┬────────────┘
                                           │
                     ┌─────────────────────┼─────────────────────┐
                     ▼                     ▼                     ▼
        scripts/build_typeset_edition.py   │          scripts/generate_tei_p5.py
                     │                     │                     │
                     ▼                     │                     ▼
        [boethlingk1887_typeset.pdf]       │           [boehtlingk1887_p5.xml]
              (Modern Book PDF)            │            (Archival XML & RelaxNG)
                                           ▼
                              scripts/build_sandwich_pdf.py
                                           │
                                           ▼
                             [boehtlingk1887_sandwich.pdf]
                                  (1:1 Facsimile PDF)
```

---

## 🔍 Method 1: Visual Collation with the QA Viewer (Recommended)

For optical comparison between transcribed text and primary facsimiles, the repository provides the interactive [`viewer.html`](https://github.com/birchville-org/boethlingk/blob/main/viewer.html).

### 1. Launch Local Web Server
Due to browser security policies (CORS) regarding local files, start a local HTTP server in the repository root:
```bash
python3 -m http.server 8000
```
Open in your browser: `http://localhost:8000/viewer.html`

### 2. Controls & Editor Features
- **Left Pane (Facsimile Inspection):** Displays the high-resolution scan from Heidelberg University Library. Zoom with mouse wheel or pinch-to-zoom; pan by holding left-click and dragging.
- **Right Pane (Sūtra Fields):** Directly edit the current Sūtra:
  - `canonical_devanagari`: Canonical Devanāgarī text
  - `canonical_iast`: Scholarly IAST transliteration
  - `translation`: German translation by Otto Böhtlingk (1887)
  - `commentary`: Philological commentary and textual apparatus
- **Snippet Toolbar:** Quick-insert buttons for dandas (`॥`) and IAST diacritics (`ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`, `ṃ`, `ḥ`).
- **Navigation:** Use arrow keys or click *Previous / Next Sūtra* buttons.

### 3. Save with Silent Auto-Repair
- Press `Cmd+S` (macOS) or `Ctrl+S` (Windows/Linux), or click **"Save (JSON)"**.
- The editor performs unobtrusive *Silent Auto-Repair* (stripping invalid tokens and normalizing punctuation) and saves changes directly to `data/ashtadhyayi_complete_boethlingk1887.json` using the *File System Access API*.

---

## ⌨️ Method 2: Targeted Edits in Code Editor

If you know the Sūtra reference (e.g., `1.1.4`):

1. Open `data/ashtadhyayi_complete_boethlingk1887.json` in VS Code or your preferred text editor.
2. Search for `"ref": "1.1.4"`.
3. Modify the fields directly:
   ```json
   {
     "ref": "1.1.4",
     "adhyaya": 1,
     "pada": 1,
     "sutra_num": 4,
     "page": 2,
     "canonical_devanagari": "न धातुलोप आर्धधातुके",
     "canonical_iast": "na dhātulopa ārdhadhātuke",
     "translation": "Wenn ein ārdhadhātuka genanntes Suffix...",
     "commentary": "Beispiele लोलुव, मरीमज..."
   }
   ```
4. Save the file.

---

## ⚡ Step 3: Recompile Distribution Artifacts

After saving your corrections, run the build scripts from the terminal:

### 1. Rebuild Typst Book Edition (Build time: ~0.9 seconds)
```bash
python3 scripts/build_typeset_edition.py
```
Generates the publication-ready 737-page vector PDF:  
👉 `data/output/boethlingk1887_typeset_edition.pdf`

### 2. Generate & Validate TEI-P5 XML Edition (Build time: ~3 seconds)
```bash
python3 scripts/generate_tei_p5.py
```
Updates `data/tei/boehtlingk1887_p5.xml` and validates it against the official TEI RelaxNG schema (`schemas/tei_all.rng`).

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

1. Run local integrity checks:
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

The GitHub Actions CI pipeline (`.github/workflows/ci.yml`) validates dataset integrity and schema validity automatically on every push.
