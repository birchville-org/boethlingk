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

## 🚀 Step 4: Verify, Commit & Pull Request (Curation Workflow)

The `boethlingk` project is maintained as a **scholarly curated edition** (Curated Edition, directed by Marco Demarmels / birchville-org). To ensure the long-term canonical integrity of the 3,997 sūtras and strict compliance of the TEI-P5 XML edition, all textual corrections, philological refinements, and enhancements must be submitted via **feature branches and Pull Requests (PR)**.

### 1. Run Local Integrity Checks
Before committing, verify that no sūtras were dropped or inadvertently modified, and that the TEI-P5 RelaxNG schema validation succeeds:

```bash
# a) Check master JSON integrity (exactly 14 Shiva Sutras + 3,983 Astadhyayi Sutras = 3,997):
python3 -c "
import json
with open('data/ashtadhyayi_complete_boethlingk1887.json', encoding='utf-8') as f:
    d = json.load(f)
assert len(d['shiva_sutras']) == 14
assert len(d['sutras']) == 3983
print('Integrity: 100% OK')
"

# b) Regenerate and validate TEI-P5 XML against the official RelaxNG schema:
python3 scripts/generate_tei_p5.py \
  --input data/ashtadhyayi_complete_boethlingk1887.json \
  --output data/tei/boehtlingk1887_p5.xml \
  --schema schemas/tei_all.rng
```

### 2. Create a Feature Branch & Commit Changes
Do not commit directly to `main`. Isolate changes within a descriptive feature branch:

```bash
# Create and checkout a new branch (convention: fix/sutra-<ref> or corr/<topic>)
git checkout -b fix/sutra-1.1.4

# Stage modified dataset and generated TEI-P5 XML
git add data/ashtadhyayi_complete_boethlingk1887.json data/tei/boehtlingk1887_p5.xml

# Create a clear, conventional commit message
git commit -m "fix(sutra): correct reading and commentary for sutra 1.1.4"
```

### 3. Push Branch & Open a Pull Request (PR)
Push the branch to the remote repository (or your fork):

```bash
git push -u origin fix/sutra-1.1.4
```

Then open a **Pull Request** against branch `main` on GitHub:
* **Via GitHub Web UI:** Follow the *"Compare & pull request"* prompt that appears automatically after pushing.
* **Via GitHub CLI (`gh`):**
  ```bash
  gh pr create \
    --title "fix(sutra): correct reading and commentary for sutra 1.1.4" \
    --body "Philological alignment with Heidelberg UB facsimile page 3: correction in commentary for sutra 1.1.4."
  ```

> 💡 **Best Practice for Pull Requests:**
> - **Sūtra Reference (`ref`) & Page:** Specify the affected sūtra reference and book page (e.g., `Sūtra 1.1.4, p. 3`).
> - **Facsimile Reference:** Include a link to the corresponding Heidelberg UB IIIF facsimile scan.
> - **Rationale:** Provide a brief explanation of the correction (e.g., resolving an OCR misread of IAST diacritics or Devanāgarī ligatures).

### 4. Automated CI Validation on Pull Requests
Whenever a Pull Request is opened or updated, the GitHub Actions CI pipeline (`.github/workflows/ci.yml`) automatically executes:
* **Master Dataset Integrity:** Verifies all 3,997 sūtras for completeness and uniqueness (0 duplicates, 0 gaps).
* **TEI-P5 RelaxNG Validation:** Validates the generated XML file against the official `schemas/tei_all.rng` schema.

Merging requires all CI checks to pass with green status.

### 5. Curation, Review & Approval
As the project curator, **Marco Demarmels** philologically and technically reviews submitted changes against the original 1887 print and Heidelberg UB facsimiles:
1. **Philological Review:** Does the proposed change faithfully represent Böhtlingk's original text and apparatus (Leipzig 1887)?
2. **Canonical Consistency:** Does canonical numbering, pāda structure, and text model remain unaltered?
3. **Approval & Merge:** Once approved, the Pull Request is merged into the canonical `main` branch, and updated release artifacts are generated if needed.

*(Note: Direct commits and pushes to `main` are reserved exclusively for the project curator for administrative releases and automated deployment pipelines.)*
