#!/usr/bin/env python3
"""
scripts/build_facsimile_dense_edition.py — Compiles the dense facsimile edition
of Otto von Böhtlingk's Pāṇini (1887), achieving exact 1:1 page parity with the
historical 1887 Leipzig edition (each of pages 1–476 corresponds to exactly 1 page).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_typeset_edition import load_edition_structure, verify_required_fonts
from prepare_facsimile_dense_data import main as prepare_dense_data


def _find_body_start_index(doc: pymupdf.Document) -> int:
    """Locate PDF 0-based index of original page 1 (Śiva-Sūtras) or fail loudly."""
    for i in range(min(10, len(doc))):
        text = doc[i].get_text()
        if "॥ अथ शब्दानुशासनम् ॥" in text or "अ इ उ ण्" in text:
            return i
    raise RuntimeError("Front-Matter-Grenze (Śiva-Sūtras auf Originalseite 1) im PDF nicht gefunden.")


def _find_corrigenda_start_index(doc: pymupdf.Document, body_start_idx: int) -> int:
    """Locate PDF 0-based index of Corrigenda heading in body text or fail loudly."""
    for i in range(len(doc) - 1, body_start_idx, -1):
        for b in doc[i].get_text("dict").get("blocks", []):
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    if span["bbox"][1] >= 45.0 and "Nachträge und Verbesserungen (Corrigenda)" in span.get("text", ""):
                        return i
    raise RuntimeError("Corrigenda-Startseite ('Nachträge und Verbesserungen (Corrigenda)') im PDF nicht gefunden.")


def post_process_dense_pdf(pdf_path: Path) -> None:
    """Inject native PDF page labels and complete hierarchical bookmarks."""
    print("Post-Processing via PyMuPDF: Injektion von Page-Labels & TOC-Outline...")
    structure = load_edition_structure(REPO_ROOT)
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    try:
        front_matter_count = _find_body_start_index(doc)
    except RuntimeError as exc:
        doc.close()
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Front Matter Seiten: {front_matter_count} (i–{front_matter_count})")
    print(f"Haupttext beginnt auf PDF-Seite {front_matter_count + 1} mit Originalseite 1 (Śiva-Sūtras).")

    # 1. Native Page Labels:
    # Front Matter: 0..front_matter_count-1 -> Roman i..
    # Body: front_matter_count..total_pages-1 -> Arabic 1..
    labels = [
        {"startpage": 0, "prefix": "", "style": "r", "firstpagenum": 1},
        {"startpage": front_matter_count, "prefix": "", "style": "D", "firstpagenum": 1},
    ]
    doc.set_page_labels(labels)
    print("✓ Native PDF Page-Labels erfolgreich gesetzt.")

    # 2. Hierarchical Bookmarks (TOC Outline) built from edition_structure.json
    def p(orig_p: int) -> int:
        return min(front_matter_count + orig_p, total_pages)

    toc = [list(entry) for entry in structure["front_matter_bookmarks"]]
    toc.append([1, "Śiva-Sūtras (Akṣarasamāmnāya)", p(structure["shiva_sutras_page"])])
    for adh in structure["adhyayas"]:
        toc.append([1, f"{adh['title_de']} ({adh['pada_range']})", p(adh["start_page"])])
        for pada in adh["padas"]:
            toc.append([2, f"{pada['num']}. Pāda: {pada['incipit']} ({pada['sutra_range']})", p(pada["start_page"])])
    toc.append([1, "Nachträge und Verbesserungen (Corrigenda)", p(structure["facsimile_corrigenda_pages"][0])])

    doc.set_toc(toc)
    print(f"✓ {len(toc)} hierarchische Bookmarks erfolgreich injiziert.")

    # Save via temporary file to allow overwriting without incremental collision
    tmp_path = pdf_path.with_name(f"{pdf_path.stem}_tmp.pdf")
    doc.save(str(tmp_path), deflate=True)
    doc.close()
    tmp_path.replace(pdf_path)


def verify_page_parity(pdf_path: Path) -> None:
    """Verify exact 1:1 parity across pages 1..476 and exit non-zero on any overflow."""
    print("=" * 70)
    print("Verifikation der 1:1-Seitenparität:")
    print("=" * 70)

    structure = load_edition_structure(REPO_ROOT)
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    with open(REPO_ROOT / "data" / "ashtadhyayi_facsimile_dense.json", encoding="utf-8") as f:
        pages_data = json.load(f)

    try:
        front_matter_count = _find_body_start_index(doc)
        corrigenda_idx = _find_corrigenda_start_index(doc, front_matter_count)
    except RuntimeError as exc:
        doc.close()
        print(f"FEHLER: {exc}", file=sys.stderr)
        sys.exit(1)

    actual_text_pages = corrigenda_idx - front_matter_count
    corrigenda_pages_count = total_pages - corrigenda_idx

    print(f"Gesamtseiten im PDF: {total_pages}")
    print(f"Front-Matter: {front_matter_count} Seiten (i–{front_matter_count})")
    print(f"Textseiten S. 1–476: {actual_text_pages} Seiten")
    print(f"Corrigenda S. 477–479: {corrigenda_pages_count} Seiten")

    overflows = 0
    if front_matter_count != structure["front_matter_pages"]:
        print(
            f"FEHLER: Front Matter hat {front_matter_count} Seiten (erwartet {structure['front_matter_pages']}).",
            file=sys.stderr,
        )
        overflows += 1

    if actual_text_pages != structure["text_pages_count"]:
        print(
            f"FEHLER: {actual_text_pages} Textseiten zwischen S. 1 und Corrigenda (erwartet {structure['text_pages_count']}).",
            file=sys.stderr,
        )
        overflows += 1

    if total_pages != structure["total_facsimile_pdf_pages"]:
        print(
            f"FEHLER: Gesamtseiten {total_pages} != erwartet {structure['total_facsimile_pdf_pages']}.",
            file=sys.stderr,
        )
        overflows += 1

    for p_info in pages_data:
        orig_p = p_info["page_num"]
        pdf_idx = front_matter_count + (orig_p - 1)
        if pdf_idx >= total_pages:
            print(f"FEHLER: Originalseite {orig_p} liegt jenseits des PDF-Endes ({pdf_idx} >= {total_pages})!", file=sys.stderr)
            overflows += 1
            continue

        # Collect right-margin canonical reference tokens inside body area (exclude header y < 45 and inline citations)
        margin_refs: set[str] = set()
        for b in doc[pdf_idx].get_text("dict").get("blocks", []):
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    if span["bbox"][1] >= 45.0 and span["bbox"][0] > 350.0:
                        txt = span.get("text", "").strip()
                        if txt:
                            margin_refs.add(txt)

        missing = []
        for s in p_info["sutras"]:
            a, p, sn = s["adhyaya"], s["pada"], s["sutra_num"]
            ref_str = f"{a}, {p}, {sn}."
            if ref_str not in margin_refs:
                missing.append(ref_str)

        if missing:
            overflows += 1
            print(f"Überlauf auf Originalseite {orig_p} (PDF-Seite {pdf_idx + 1}): Fehlende Sūtras im Satzspiegel: {missing}", file=sys.stderr)

    doc.close()

    if overflows == 0:
        print("✓ EXAKTE 1:1-SEITENPARITÄT: Alle 476 Originalseiten belegen jeweils genau 1 Seite.")
        print("=" * 70)
    else:
        print(f"FEHLER: {overflows} Paritätsverletzung(en) festgestellt.", file=sys.stderr)
        print("=" * 70)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile dense facsimile edition of Boethlingk 1887")
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "data" / "output" / "boethlingk1887_facsimile_dense.pdf",
        help="Target PDF path",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        default=False,
        help="Synchronize output PDF to directory given by --sync-dir or $BOETHLINGK_SYNC_DIR",
    )
    parser.add_argument(
        "--sync-dir",
        type=Path,
        default=None,
        help="Target directory for --sync (falls back to $BOETHLINGK_SYNC_DIR)",
    )
    args = parser.parse_args()

    t0 = time.time()
    print("=" * 70)
    print("Kompiliere dichte Faksimile-Ausgabe (1:1-Seitenparität mit Böhtlingk 1887)...")
    print("=" * 70)

    # 1. Daten & Schriften prüfen
    prepare_dense_data()
    verify_required_fonts(REPO_ROOT)

    # 2. Typst kompilieren
    args.output.parent.mkdir(parents=True, exist_ok=True)
    typst_cmd = ["typst", "compile", "--root", str(REPO_ROOT)]
    fonts_dir = REPO_ROOT / "data" / "fonts"
    if fonts_dir.is_dir():
        typst_cmd.extend(["--font-path", str(fonts_dir)])
    typst_cmd.extend([str(REPO_ROOT / "scripts" / "boethlingk1887_facsimile_dense.typ"), str(args.output)])

    res = subprocess.run(typst_cmd)
    if res.returncode != 0:
        print("Fehler beim Typst-Kompilieren!", file=sys.stderr)
        sys.exit(res.returncode)

    # 3. PyMuPDF Post-Processing
    post_process_dense_pdf(args.output)

    # 4. Paritäts-Check (blockierend)
    verify_page_parity(args.output)

    # 5. Automatisches Quality Gate: Pytest Suite über sys.executable
    print("=" * 70)
    print("Führe automatisches Quality Gate (pytest tests/) aus...")
    test_env = {**os.environ, "BOETHLINGK_REQUIRE_PDF": "1"}
    test_res = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(REPO_ROOT / "tests")],
        cwd=str(REPO_ROOT),
        env=test_env,
        capture_output=True,
        text=True,
    )
    if test_res.returncode != 0:
        print("FEHLER: Quality Gate fehlgeschlagen!", file=sys.stderr)
        print(test_res.stdout, file=sys.stderr)
        print(test_res.stderr, file=sys.stderr)
        sys.exit(test_res.returncode)
    print("✓ Quality Gate erfolgreich: Alle Text-, Layout- & Paritäts-Tests bestanden.")

    # 6. Sync nach Arbeitsordner (NUR mit explizitem --sync Flag und Zielverzeichnis)
    if args.sync:
        env_sync = os.environ.get("BOETHLINGK_SYNC_DIR")
        sync_dir = args.sync_dir or (Path(env_sync) if env_sync else None)
        if sync_dir is None or not sync_dir.exists():
            print(
                f"FEHLER: --sync angefordert, aber Zielverzeichnis nicht gesetzt oder nicht vorhanden: {sync_dir}",
                file=sys.stderr,
            )
            sys.exit(1)
        dest_file = sync_dir / "BOETHLINGK 1887 Panini Grammatik (Dichte Faksimile-Ausgabe).pdf"
        shutil.copy2(args.output, dest_file)
        print(f"✓ Synchronisiert nach Arbeitsordner: {dest_file}")
    else:
        print("ℹ︎ Lokaler Build: Keine externe Synchronisation (Genehmigung erforderlich).")

    elapsed = time.time() - t0
    size_mb = args.output.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"Erfolg: {args.output} erstellt!")
    print(f"Dateigröße: {size_mb:.2f} MB | Zeit: {elapsed:.2f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
