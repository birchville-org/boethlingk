#!/usr/bin/env python3
import json
import subprocess
import pymupdf
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from build_facsimile_dense_edition import post_process_dense_pdf

# Multi-tier typographic ladder: optimized for maximum comfortable reading size
levels = [
    # Level 5: Maximum comfort (for 1-5 sutras with short text)
    {"level": 5, "deva_size": "11.8pt", "body_size": "9.6pt", "body_leading": "0.45em", "comm_size": "8.4pt", "comm_leading": "0.42em", "sutra_spacing": "0.95em"},
    # Level 4: Generous comfort (for pages like Page 8: 3-6 sutras, medium text)
    {"level": 4, "deva_size": "11.4pt", "body_size": "9.3pt", "body_leading": "0.42em", "comm_size": "8.1pt", "comm_leading": "0.38em", "sutra_spacing": "0.70em"},
    # Level 3: Relaxed standard (for 6-8 sutras, average text)
    {"level": 3, "deva_size": "10.8pt", "body_size": "8.9pt", "body_leading": "0.37em", "comm_size": "7.7pt", "comm_leading": "0.32em", "sutra_spacing": "0.38em"},
    # Level 2: Compact standard (for 8-10 sutras, textstark)
    {"level": 2, "deva_size": "10.4pt", "body_size": "8.6pt", "body_leading": "0.33em", "comm_size": "7.4pt", "comm_leading": "0.27em", "sutra_spacing": "0.20em"},
    # Level 1: Dense safety (for 10-12 sutras, z.B. S. 3, 70)
    {"level": 1, "deva_size": "10.0pt", "body_size": "8.4pt", "body_leading": "0.30em", "comm_size": "7.2pt", "comm_leading": "0.25em", "sutra_spacing": "0.12em"},
    # Level 0: Extreme safety (for S. 282, 286 mit 11 Sutras & viel Text)
    {"level": 0, "deva_size": "9.6pt", "body_size": "8.1pt", "body_leading": "0.26em", "comm_size": "6.9pt", "comm_leading": "0.23em", "sutra_spacing": "0.06em"},
]

def find_first_overflow(pdf_path: Path, pages_data: list[dict], front_matter_count: int = 5) -> int | None:
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)
    
    for i, p_info in enumerate(pages_data):
        orig_p = p_info["page_num"]
        pdf_idx = front_matter_count + (orig_p - 1)
        if pdf_idx >= total_pages:
            doc.close()
            return orig_p
            
        page_text = doc[pdf_idx].get_text()
        for s in p_info["sutras"]:
            ref_str = f"{s['adhyaya']}, {s['pada']}, {s['sutra_num']}."
            if ref_str not in page_text:
                doc.close()
                return orig_p
    doc.close()
    return None

def main():
    json_path = Path("data/ashtadhyayi_facsimile_dense.json")
    with open(json_path, encoding="utf-8") as f:
        pages = json.load(f)

    # Initial intelligent assignment based on sutra count and text length
    for p in pages:
        pnum = p["page_num"]
        s_cnt = len(p["sutras"])
        tr_len = sum(len(s.get("translation", "")) for s in p["sutras"])
        cm_len = sum(len(s.get("commentary", "")) for s in p["sutras"])
        tot = tr_len + cm_len
        has_col = any(s.get("colophon") for s in p["sutras"])

        if pnum in [282, 286]:
            lvl_idx = 5 # Level 0
        elif pnum in [3, 70, 378, 460] or s_cnt >= 11:
            lvl_idx = 4 # Level 1
        elif s_cnt <= 4:
            if tot > 3000: # Page 8
                lvl_idx = 1 # Level 4
            elif tot > 1500 or has_col:
                lvl_idx = 1 # Level 4
            else:
                lvl_idx = 0 # Level 5
        elif s_cnt <= 7:
            if tot > 2000 or has_col:
                lvl_idx = 2 # Level 3
            elif tot > 1200:
                lvl_idx = 1 # Level 4
            else:
                lvl_idx = 0 # Level 5
        elif s_cnt <= 9:
            if tot > 1600 or has_col:
                lvl_idx = 3 # Level 2
            elif tot > 1000:
                lvl_idx = 2 # Level 3
            else:
                lvl_idx = 1 # Level 4
        else: # 10 sutras
            if tot > 1200:
                lvl_idx = 4 # Level 1
            else:
                lvl_idx = 3 # Level 2

        p["level_idx"] = lvl_idx
        cfg = dict(levels[lvl_idx])
        cfg["tier"] = cfg["level"]
        p["profile"] = cfg

    output_pdf = Path("data/output/boethlingk1887_facsimile_dense.pdf")

    # Optimization loop
    iteration = 0
    while True:
        iteration += 1
        print(f"--- Iteration {iteration} ---")
        
        # Save json
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(pages, f, ensure_ascii=False, indent=2)

        # Compile typst
        typst_cmd = [
            "typst", "compile",
            "--root", ".",
            "--font-path", "data/fonts",
            "scripts/boethlingk1887_facsimile_dense.typ",
            str(output_pdf),
        ]
        res = subprocess.run(typst_cmd)
        if res.returncode != 0:
            print("Typst compile error!", file=sys.stderr)
            sys.exit(1)

        post_process_dense_pdf(output_pdf)
        overflow_page = find_first_overflow(output_pdf, pages)
        
        if overflow_page is None:
            print("======================================================================")
            print("✓ PERFEKTE PARITÄT ERREICHT! Alle Seiten passen ohne Überlauf!")
            print("======================================================================")
            break

        print(f"Überlauf gefunden auf Seite {overflow_page}! Passe Profil an...")
        p_obj = next(p for p in pages if p["page_num"] == overflow_page)
        if p_obj["level_idx"] < len(levels) - 1:
            p_obj["level_idx"] += 1
            cfg = dict(levels[p_obj["level_idx"]])
            cfg["tier"] = cfg["level"]
            p_obj["profile"] = cfg
            print(f"Seite {overflow_page} heruntergestuft auf Level {cfg['level']}: body={cfg['body_size']}, comm={cfg['comm_size']}, sp={cfg['sutra_spacing']}")
        else:
            print(f"FEHLER: Seite {overflow_page} ist bereits auf Level 0 und läuft trotzdem über!", file=sys.stderr)
            sys.exit(1)

    # Save final calibrated profiles
    calibrated = {str(p["page_num"]): p["profile"] for p in pages}
    with open("data/calibrated_dense_profiles.json", "w", encoding="utf-8") as f:
        json.dump(calibrated, f, indent=2)
    print("Gespeichert nach data/calibrated_dense_profiles.json")

if __name__ == "__main__":
    main()
