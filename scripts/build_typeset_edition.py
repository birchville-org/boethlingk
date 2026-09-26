#!/usr/bin/env python3
"""
scripts/build_typeset_edition.py — Builds the complete, modern, typeset edition
of Otto von Böhtlingk's Pāṇini (1887) using Typst.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


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
            p_sutras = [s for s in sutras if s.get("adhyaya") == a_num and s.get("pada") == p_num]
            adh_entry["padas"].append({
                "num": p_num,
                "title_de": de_p,
                "title_sa": sa_p,
                "sutras": p_sutras,
            })
        tree.append(adh_entry)

    with open(out_tree_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, ensure_ascii=False, indent=2)

    # Corrigenda aus TEI-P5 sicherstellen
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile modern typeset PDF of Boethlingk 1887")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/output/boethlingk1887_typeset_edition.pdf"),
        help="Target PDF path",
    )
    args = parser.parse_args()

    t0 = time.time()
    print("=" * 70)
    print("Kompiliere vollständige typografische Neuausgabe (Methode 3)...")
    print("=" * 70)

    prepare_data()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    typst_cmd = [
        "typst", "compile",
        "--root", ".",
        "scripts/boethlingk1887_edition.typ",
        str(args.output),
    ]

    res = subprocess.run(typst_cmd)
    if res.returncode != 0:
        print("Fehler beim Typst-Kompilieren!", file=sys.stderr)
        sys.exit(res.returncode)

    elapsed = time.time() - t0
    size_mb = args.output.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"Erfolg: {args.output} erstellt!")
    print(f"Dateigröße: {size_mb:.2f} MB | Zeit: {elapsed:.2f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
