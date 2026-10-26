#!/usr/bin/env python3
"""
scripts/build_facsimile_dense_edition.py — Compiles the dense facsimile test edition
of Otto von Böhtlingk's Pāṇini (1887), achieving exact 1:1 page parity with the
historical 1887 Leipzig edition (each of pages 1–476 corresponds to exactly 1 page).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

from prepare_facsimile_dense_data import main as prepare_dense_data


def post_process_dense_pdf(pdf_path: Path) -> None:
    """Inject native PDF page labels and complete hierarchical bookmarks."""
    print("Post-Processing via PyMuPDF: Injektion von Page-Labels & TOC-Outline...")
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    # Front matter is exactly pages 0 to 4 (i to v)
    # Page 5 is Original Page 1 (Śiva-Sūtras)
    front_matter_count = 5
    for i in range(min(8, total_pages)):
        text = doc[i].get_text()
        if "॥ अथ शब्दानुशासनम् ॥" in text or "अ इ उ ण्" in text:
            front_matter_count = i
            break

    print(f"Front Matter Seiten: {front_matter_count} (i–{front_matter_count})")
    print(f"Haupttext beginnt auf PDF-Seite {front_matter_count + 1} mit Originalseite 1 (Śiva-Sūtras).")

    # 1. Native Page Labels:
    # Front Matter: 0..front_matter_count-1 -> Roman i..
    # Body: front_matter_count..total_pages-1 -> Arabic 1..
    labels = [
        {"startpage": 0, "prefix": "", "style": "r", "firstpagenum": 1},
        {"startpage": front_matter_count, "prefix": "", "style": "D", "firstpagenum": 1},
    ]
    try:
        doc.set_page_labels(labels)
        print("✓ Native PDF Page-Labels erfolgreich gesetzt.")
    except Exception as e:
        print(f"Hinweis beim Setzen der Page-Labels: {e}")

    # 2. Hierarchical Bookmarks (TOC Outline)
    def p(orig_p: int) -> int:
        return min(front_matter_count + orig_p, total_pages)

    toc = [
        [1, "Titelei & Front Matter", 1],
        [2, "Halbtitel (Bastard Title)", 1],
        [2, "Impressum & Birchville Curation Badge", 2],
        [2, "Haupttitel (Leipzig 1887 Neusatz)", 3],
        [2, "Vorwort zur dichten Faksimile-Ausgabe", 4],
        [2, "Inhaltsübersicht", 5],
        [1, "Śiva-Sūtras (Akṣarasamāmnāya)", p(1)],
        [1, "Erster Adhyāya (1.1–1.4)", p(2)],
        [2, "1. Pāda: वृद्धिरादैच् (1.1.1–75)", p(2)],
        [2, "2. Pāda: गाङ्कुटादिभ्यो ऽञ्णिन्ङित् (1.2.1–73)", p(11)],
        [2, "3. Pāda: भूवादयो धातवः (1.3.1–93)", p(21)],
        [2, "4. Pāda: आ कडारादेका संज्ञा (1.4.1–110)", p(31)],
        [1, "Zweiter Adhyāya (2.1–2.4)", p(43)],
        [2, "1. Pāda: समर्थः पदविधिः (2.1.1–72)", p(43)],
        [2, "2. Pāda: पूर्वो ऽपरो ऽधरोत्तराणि (2.2.1–38)", p(52)],
        [2, "3. Pāda: अनभिहिते (2.3.1–73)", p(56)],
        [2, "4. Pāda: द्विगुरेकवचनम् (2.4.1–85)", p(65)],
        [1, "Dritter Adhyāya (3.1–3.4)", p(75)],
        [2, "1. Pāda: प्रत्ययः (3.1.1–150)", p(75)],
        [2, "2. Pāda: कर्मण्यण् (3.2.1–188)", p(93)],
        [2, "3. Pāda: उणादयो बहुलम् (3.3.1–176)", p(114)],
        [2, "4. Pāda: धातुसम्बन्धे प्रत्ययाः (3.4.1–117)", p(134)],
        [1, "Vierter Adhyāya (4.1–4.4)", p(149)],
        [2, "1. Pāda: ङ्याप्प्रातिपदिकात् (4.1.1–178)", p(149)],
        [2, "2. Pāda: तेन रक्तं रागात् (4.2.1–145)", p(170)],
        [2, "3. Pāda: युष्मदस्मदोरन्यतरस्याम् (4.3.1–168)", p(187)],
        [2, "4. Pāda: प्राग्वहतेष्ठञ् (4.4.1–144)", p(206)],
        [1, "Fünfter Adhyāya (5.1–5.4)", p(221)],
        [2, "1. Pāda: प्राङ्क्रीताच्छः (5.1.1–136)", p(221)],
        [2, "2. Pāda: धान्यनां भवने क्षेत्रे खञ् (5.2.1–140)", p(236)],
        [2, "3. Pāda: प्राग्दिशो विभक्तिः (5.3.1–119)", p(251)],
        [2, "4. Pāda: पादशतस्य संख्यादेर्वीप्सायाम् (5.4.1–160)", p(264)],
        [1, "Sechster Adhyāya (6.1–6.4)", p(283)],
        [2, "1. Pāda: एकाचो द्वे प्रथमस्य (6.1.1–223)", p(283)],
        [2, "2. Pāda: बहुव्रीहौ प्रकृत्या पूर्वपदम् (6.2.1–199)", p(311)],
        [2, "3. Pāda: अलुगुत्तरपदे (6.3.1–139)", p(335)],
        [2, "4. Pāda: अङ्गस्य (6.4.1–175)", p(351)],
        [1, "Siebenter Adhyāya (7.1–7.4)", p(374)],
        [2, "1. Pāda: युवोरनाकौ (7.1.1–103)", p(374)],
        [2, "2. Pāda: सिचि वृद्धिः परस्मैपदेषु (7.2.1–118)", p(387)],
        [2, "3. Pāda: लघोरुपधायाः (7.3.1–120)", p(402)],
        [2, "4. Pāda: णिच्युपसंख्यानम् (7.4.1–97)", p(417)],
        [1, "Achter Adhyāya (8.1–8.4)", p(428)],
        [2, "1. Pāda: सर्वस्य द्वे (8.1.1–74)", p(428)],
        [2, "2. Pāda: पूर्वत्रासिद्धम् (8.2.1–108)", p(438)],
        [2, "3. Pāda: रषाभ्यां नो णः समानपदे (8.3.1–119)", p(452)],
        [2, "4. Pāda: स्तोः श्चुना श्चुः (8.4.1–68)", p(467)],
        [1, "Nachträge und Verbesserungen (Corrigenda)", p(477)],
    ]

    doc.set_toc(toc)
    print(f"✓ {len(toc)} hierarchische Bookmarks erfolgreich injiziert.")

    # Save via temporary file to allow overwriting without incremental collision
    tmp_path = pdf_path.with_name(f"{pdf_path.stem}_tmp.pdf")
    doc.save(str(tmp_path), deflate=True)
    doc.close()
    tmp_path.replace(pdf_path)


def verify_page_parity(pdf_path: Path) -> None:
    """Verifies that each original page 1..476 corresponds 1:1 to exactly one PDF page."""
    print("=" * 70)
    print("Verifikation der 1:1-Seitenparität:")
    print("=" * 70)

    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    with open("data/ashtadhyayi_facsimile_dense.json", encoding="utf-8") as f:
        pages_data = json.load(f)

    front_matter_count = 5
    for i in range(min(8, total_pages)):
        text = doc[i].get_text()
        if "॥ अथ शब्दानुशासनम् ॥" in text or "अ इ उ ण्" in text:
            front_matter_count = i
            break

    print(f"Gesamtseiten im PDF: {total_pages}")
    print(f"Front-Matter: {front_matter_count} Seiten (i–{front_matter_count})")
    print(f"Textseiten S. 1–476: {len(pages_data) + 1} Seiten")

    overflows = 0
    for i, p_info in enumerate(pages_data):
        orig_p = p_info["page_num"]
        pdf_idx = front_matter_count + (orig_p - 1)
        if pdf_idx >= total_pages:
            print(f"FEHLER: Originalseite {orig_p} liegt jenseits des PDF-Endes ({pdf_idx} >= {total_pages})!")
            overflows += 1
            continue

        page_text = doc[pdf_idx].get_text()
        missing = []
        for s in p_info["sutras"]:
            a, p, sn = s["adhyaya"], s["pada"], s["sutra_num"]
            ref_str = f"{a}, {p}, {sn}."
            if ref_str not in page_text:
                missing.append(ref_str)

        if missing:
            overflows += 1
            print(f"Überlauf auf Originalseite {orig_p} (PDF-Seite {pdf_idx + 1}): Fehlende Sūtras: {missing}")

    if overflows == 0:
        print("✓ PERFEKTE 1:1-SEITENPARITÄT: Alle 476 Originalseiten passen exakt auf genau 1 Seite!")
    else:
        print(f"WARNUNG: {overflows} Seiten mit Überlauf festgestellt.")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile dense facsimile test PDF of Boethlingk 1887")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/boethlingk1887_facsimile_dense_test.pdf"),
        help="Target PDF path",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        default=False,
        help="Synchronize output PDF to user Indologie folder (only with explicit approval)",
    )
    args = parser.parse_args()

    t0 = time.time()
    print("=" * 70)
    print("Kompiliere dichte Faksimile-Testausgabe (1:1-Seitenparität mit Böhtlingk 1887)...")
    print("=" * 70)

    # 1. Daten vorbereiten
    prepare_dense_data()

    # 2. Typst kompilieren
    args.output.parent.mkdir(parents=True, exist_ok=True)
    typst_cmd = [
        "typst", "compile",
        "--root", ".",
        "--font-path", "data/fonts",
        "scripts/boethlingk1887_facsimile_dense.typ",
        str(args.output),
    ]

    res = subprocess.run(typst_cmd)
    if res.returncode != 0:
        print("Fehler beim Typst-Kompilieren!", file=sys.stderr)
        sys.exit(res.returncode)

    # 3. PyMuPDF Post-Processing
    post_process_dense_pdf(args.output)

    # 4. Paritäts-Check
    verify_page_parity(args.output)

    # 5. Sync nach Indologie-Arbeitsordner (NUR mit explizitem --sync Flag)
    if args.sync:
        indologie_dest = Path("/Users/marco/Documents/00_Indologie/Panini")
        if indologie_dest.exists():
            dest_file = indologie_dest / "BOETHLINGK 1887 Panini Grammatik (Dichte Faksimile-Testausgabe).pdf"
            shutil.copy2(args.output, dest_file)
            print(f"✓ Synchronisiert nach Indologie-Arbeitsordner: {dest_file}")
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
