#!/usr/bin/env python3
"""
scripts/build_typeset_edition.py — Compiles the modernized, scholarly typeset
edition of Otto von Böhtlingk's Pāṇini (1887) using Typst & PyMuPDF.

Features:
- Full Birchville Scholarly Synthesis front matter with coat of arms & imprint.
- Classical Leipzig typography: Noto Serif Devanagari + STIX Two Text, leading 0.46em.
- Left-aligned Devanāgarī headings with right-margin canonical references (Adhyāya, Pāda, Sūtra).
- Dynamic running headers displaying the last Sūtra reference of the current page.
- Dynamic original page boundaries: '📖 Böhtlingk (1887) S. X'.
- Widow/orphan prevention: Sūtra heading and translation locked together.
- Native PDF page labels: Roman 'i'–'vi' for front matter, Arabic '1'–'...' for body.
- 45+ hierarchical PDF bookmarks (TOC outline).
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


def to_deva_num(n: int | str) -> str:
    digits = "०१२३४५६७८९"
    return "".join(digits[int(c)] if c.isdigit() else c for c in str(n))


def soft_hyphenate_long_iast(text: str, max_chunk: int = 35) -> str:
    """Insert soft hyphens into excessively long IAST compounds so Typst can break them gracefully."""
    words = text.split()
    new_words = []
    vowels = "aeiouāīūṛṝḷḹeaiāu"
    for w in words:
        if len(w) > max_chunk:
            parts = []
            curr = 0
            while curr < len(w):
                next_cut = curr + max_chunk
                if next_cut >= len(w):
                    parts.append(w[curr:])
                    break
                cut_pos = -1
                for i in range(next_cut, curr + 15, -1):
                    if i < len(w) and w[i].lower() in vowels:
                        cut_pos = i + 1
                        break
                if cut_pos == -1:
                    cut_pos = next_cut
                parts.append(w[curr:cut_pos])
                curr = cut_pos
            new_words.append("\u00ad".join(parts))
        else:
            new_words.append(w)
    return " ".join(new_words)


def prepare_data() -> None:
    """Pre-group master dataset by Adhyāya and Pāda for optimal Typst typesetting."""
    master_path = Path("data/ashtadhyayi_complete_boethlingk1887.json")
    out_tree_path = Path("data/ashtadhyayi_grouped_edition.json")

    with open(master_path, encoding="utf-8") as f:
        raw = json.load(f)

    adhyaya_names = {
        1: ("Erster Adhyāya", "Prathamo 'dhyāyaḥ"),
        2: ("Zweiter Adhyāya", "Dvitīyo 'dhyāyaḥ"),
        3: ("Dritter Adhyāya", "Tṛtīyo 'dhyāyaḥ"),
        4: ("Vierter Adhyāya", "Caturtho 'dhyāyaḥ"),
        5: ("Fünfter Adhyāya", "Pañcamo 'dhyāyaḥ"),
        6: ("Sechster Adhyāya", "Ṣaṣṭho 'dhyāyaḥ"),
        7: ("Siebenter Adhyāya", "Saptamo 'dhyāyaḥ"),
        8: ("Achter Adhyāya", "Aṣṭamo 'dhyāyaḥ"),
    }

    pada_names = {
        1: ("Erster Pāda", "Prathamaḥ Pādaḥ"),
        2: ("Zweiter Pāda", "Dvitīyaḥ Pādaḥ"),
        3: ("Dritter Pāda", "Tṛtīyaḥ Pādaḥ"),
        4: ("Vierter Pāda", "Caturthaḥ Pādaḥ"),
    }

    tree = []
    sutras = raw["sutras"]

    hyphens_path = Path("data/original_hyphenations.json")
    hyphens = {}
    if hyphens_path.exists():
        with open(hyphens_path, encoding="utf-8") as f:
            hyphens = json.load(f)

    for a_num in range(1, 9):
        de_a, sa_a = adhyaya_names[a_num]
        adh_entry = {
            "num": a_num,
            "title_de": de_a,
            "title_sa": sa_a,
            "padas": [],
        }
        for p_num in range(1, 5):
            de_p, sa_p = pada_names[p_num]
            p_sutras = []
            for s in sutras:
                if s.get("adhyaya") == a_num and s.get("pada") == p_num:
                    s_copy = dict(s)
                    ref = s.get("ref", "")
                    if ref in hyphens:
                        s_copy["canonical_devanagari"] = hyphens[ref]
                    if "canonical_iast" in s_copy:
                        s_copy["canonical_iast"] = soft_hyphenate_long_iast(s_copy["canonical_iast"])
                    s_copy["sutra_num_deva"] = to_deva_num(s.get("sutra_num", 0))
                    p_sutras.append(s_copy)
            adh_entry["padas"].append({
                "num": p_num,
                "title_de": de_p,
                "title_sa": sa_p,
                "sutras": p_sutras,
            })
        tree.append(adh_entry)

    with open(out_tree_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

    # Ensure corrigenda.json exists
    corrigenda_path = Path("data/corrigenda.json")
    if not corrigenda_path.exists():
        tei_path = Path("data/tei/boehtlingk1887_p5.xml")
        if tei_path.exists():
            from lxml import etree
            tree_tei = etree.parse(str(tei_path))
            back = tree_tei.find(".//{http://www.tei-c.org/ns/1.0}back")
            if back is not None:
                items = back.findall(".//{http://www.tei-c.org/ns/1.0}item")
                corrigenda = [{"text": "".join(it.itertext()).strip()} for it in items]
                with open(corrigenda_path, "w", encoding="utf-8") as f:
                    json.dump(corrigenda, f, ensure_ascii=False, indent=2)


CANONICAL_PADAS = {
    (1, 1): ("वृद्धिरादैच्", "1.1.1–75"),
    (1, 2): ("गाङ्कुटादिभ्यो ऽञ्णिन्ङित्", "1.2.1–73"),
    (1, 3): ("भूवादयो धातवः", "1.3.1–93"),
    (1, 4): ("आ कडारादेका संज्ञा", "1.4.1–110"),
    (2, 1): ("समर्थः पदविधिः", "2.1.1–72"),
    (2, 2): ("पूर्वो ऽपरो ऽधरोत्तराणि", "2.2.1–38"),
    (2, 3): ("अनभिहिते", "2.3.1–73"),
    (2, 4): ("द्विगुरेकवचनम्", "2.4.1–85"),
    (3, 1): ("प्रत्ययः", "3.1.1–150"),
    (3, 2): ("कर्मण्यण्", "3.2.1–188"),
    (3, 3): ("उणादयो बहुलम्", "3.3.1–176"),
    (3, 4): ("धातुसम्बन्धे प्रत्ययाः", "3.4.1–117"),
    (4, 1): ("ङ्याप्प्रातिपदिकात्", "4.1.1–178"),
    (4, 2): ("तेन रक्तं रागात्", "4.2.1–145"),
    (4, 3): ("युष्मदस्मदोरन्यतरस्याम्", "4.3.1–168"),
    (4, 4): ("प्राग्वहतेष्ठञ्", "4.4.1–144"),
    (5, 1): ("प्राङ्क्रीताच्छः", "5.1.1–136"),
    (5, 2): ("धान्यनां भवने क्षेत्रे खञ्", "5.2.1–140"),
    (5, 3): ("प्राग्दिशो विभक्तिः", "5.3.1–119"),
    (5, 4): ("पादशतस्य संख्यादेर्वीप्सायाम्", "5.4.1–160"),
    (6, 1): ("एकाचो द्वे प्रथमस्य", "6.1.1–223"),
    (6, 2): ("बहुव्रीहौ प्रकृत्या पूर्वपदम्", "6.2.1–199"),
    (6, 3): ("अलुगुत्तरपदे", "6.3.1–139"),
    (6, 4): ("अङ्गस्य", "6.4.1–175"),
    (7, 1): ("युवोरनाकौ", "7.1.1–103"),
    (7, 2): ("सिचि वृद्धिः परस्मैपदेषु", "7.2.1–118"),
    (7, 3): ("लघोरुपधायाः", "7.3.1–120"),
    (7, 4): ("णिच्युपसंख्यानम्", "7.4.1–97"),
    (8, 1): ("सर्वस्य द्वे", "8.1.1–74"),
    (8, 2): ("पूर्वत्रासिद्धम्", "8.2.1–108"),
    (8, 3): ("रषाभ्यां नो णः समानपदे", "8.3.1–119"),
    (8, 4): ("स्तोः श्चुना श्चुः", "8.4.1–68"),
}

ADH_NAMES = {
    1: ("Erster Adhyāya", "1.1–1.4"),
    2: ("Zweiter Adhyāya", "2.1–2.4"),
    3: ("Dritter Adhyāya", "3.1–3.4"),
    4: ("Vierter Adhyāya", "4.1–4.4"),
    5: ("Fünfter Adhyāya", "5.1–5.4"),
    6: ("Sechster Adhyāya", "6.1–6.4"),
    7: ("Siebenter Adhyāya", "7.1–7.4"),
    8: ("Achter Adhyāya", "8.1–8.4"),
}


def post_process_pdf(pdf_path: Path) -> None:
    """Inject native PDF page labels and complete hierarchical bookmarks."""
    print("Post-Processing via PyMuPDF: Injektion von Page-Labels & TOC-Outline...")
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)

    native_toc = doc.get_toc()

    # Find start of body (Śiva-Sūtras)
    shiva_idx = next((entry[2] - 1 for entry in native_toc if "Śiva" in entry[1]), 5)

    # 1. Native Page Labels:
    # Front Matter: 0..shiva_idx -> Roman i..
    # Body: shiva_idx..end -> Arabic 1..
    labels = [
        {"startpage": 0, "style": "r", "firstpagenum": 1},
        {"startpage": shiva_idx, "style": "D", "firstpagenum": 1},
    ]
    doc.set_page_labels(labels)

    # 2. Complete hierarchical TOC Bookmarks
    front_matter = [
        [1, "Titelei & Front Matter", 1],
        [2, "Halbtitel (Bastard Title)", 1],
        [2, "Editionsvermerk & Curation Badge", 2],
        [2, "Haupttitel (Leipzig 1887)", 3],
        [2, "Vorwort zur digitalen Neuausgabe", 4],
        [2, "Inhaltsübersicht", 5],
    ]

    final_toc = list(front_matter)
    current_a = 0
    current_p = 0

    for lvl, title, pno in native_toc:
        if "Śiva" in title:
            final_toc.append([1, "Śiva-Sūtras (Akṣarasamāmnāya)", pno])
        elif lvl == 1 and "Adhyāya" in title:
            current_a += 1
            current_p = 0
            name, rng = ADH_NAMES.get(current_a, (f"{current_a}. Adhyāya", ""))
            final_toc.append([1, f"{name} ({rng})", pno])
        elif lvl == 2 and current_a > 0:
            current_p += 1
            incipit, rng = CANONICAL_PADAS.get((current_a, current_p), ("", ""))
            final_toc.append([2, f"{current_p}. Pāda: {incipit} ({rng})", pno])
        elif "Nachträge" in title or "Verbesserungen" in title:
            final_toc.append([1, "Nachträge und Verbesserungen (Corrigenda)", pno])

    doc.set_toc(final_toc)
    temp_out = pdf_path.with_name(pdf_path.stem + ".tmp.pdf")
    doc.save(str(temp_out), garbage=3, deflate=True)
    doc.close()

    temp_out.replace(pdf_path)

    # Export TOC specification file
    toc_txt_path = pdf_path.with_suffix(".toc.txt")
    with open(toc_txt_path, "w", encoding="utf-8") as f:
        f.write("# Pāṇini's Grammatik (Otto von Böhtlingk 1887) — TOC Outline Specification\n")
        f.write("# Format: [Level Indentation] Title | Page\n\n")
        for lvl, title, page_n in final_toc:
            indent = "  " * (lvl - 1)
            f.write(f"{indent}{title} | {page_n}\n")

    print(f"✓ TOC ({len(final_toc)} Einträge) und native Page-Labels erfolgreich injiziert.")
    print(f"✓ TOC-Spezifikation exportiert: {toc_txt_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile modern typeset PDF of Boethlingk 1887")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/boethlingk1887_typeset_edition.pdf"),
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
    print("Kompiliere modernisierte typografische Neuausgabe (Scholarly Synthesis)...")
    print("=" * 70)

    prepare_data()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    typst_cmd = [
        "typst", "compile",
        "--root", ".",
        "--font-path", "data/fonts",
        "scripts/boethlingk1887_edition.typ",
        str(args.output),
    ]

    res = subprocess.run(typst_cmd)
    if res.returncode != 0:
        print("Fehler beim Typst-Kompilieren!", file=sys.stderr)
        sys.exit(res.returncode)

    post_process_pdf(args.output)

    # Sync to User Indologie Panini folder if present (only with explicit --sync flag)
    if args.sync:
        indologie_dest = Path("/Users/marco/Documents/00_Indologie/Panini")
        if indologie_dest.exists():
            dest_file = indologie_dest / "BOETHLINGK 1887 Panini Grammatik (Digital Typeset Neusatz).pdf"
            shutil.copy2(args.output, dest_file)
            old_v2 = indologie_dest / "BOETHLINGK 1887 Panini Grammatik (Digital Typeset Neusatz v2).pdf"
            if old_v2.exists():
                old_v2.unlink()
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
