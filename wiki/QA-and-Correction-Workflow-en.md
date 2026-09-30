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
