#!/usr/bin/env python3
"""
scripts/prepare_facsimile_dense_data.py — Prepares pre-grouped page data for the
dense facsimile edition of Boethlingk 1887.
Every page 2..476 contains exactly the sutras of the historical original page.
Includes authentic colophons at the end of every Pada.
Calculates adaptive typographic profiles per page to maximize visual space utilization
without causing overflow.
"""
from __future__ import annotations

import json
from pathlib import Path
from build_typeset_edition import to_deva_num, soft_hyphenate_long_iast, ensure_corrigenda_json

REPO_ROOT = Path(__file__).resolve().parent.parent

adh_ordinals = {
    1: "प्रथमस्याध्यायस्य",
    2: "द्वितीयस्याध्यायस्य",
    3: "तृतीयस्याध्यायस्य",
    4: "चतुर्थस्याध्यायस्य",
    5: "पञ्चमस्याध्यायस्य",
    6: "षष्ठस्याध्यायस्य",
    7: "सप्तमस्याध्यायस्य",
    8: "अष्टमस्याध्यायस्य",
}

pada_ordinals = {
    1: "प्रथमः पादः",
    2: "द्वितीयः पादः",
    3: "तृतीयः पादः",
    4: "चतुर्थः पादः",
}

adh_romans = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII"}


def get_colophon(a: int, p: int) -> str:
    if a == 8 and p == 4:
        return "॥ इत्यष्टमस्याध्यायस्य चतुर्थः पादः । अध्यायश्च समाप्तः ॥\n॥ इति शब्दानुशासनम् समाप्तम् ॥"
    elif p == 4:
        return f"॥ इति {adh_ordinals[a]} चतुर्थः पादो ऽध्यायश्च समाप्तः ॥"
    else:
        return f"॥ इति {adh_ordinals[a]} {pada_ordinals[p]} ॥"


_TIER_PROFILES: dict[int, dict[str, object]] = {
    0: {"tier": 0, "deva_size": "9.8pt", "body_size": "8.2pt", "body_leading": "0.28em", "comm_size": "7.0pt", "comm_leading": "0.24em", "sutra_spacing": "0.08em"},
    1: {"tier": 1, "deva_size": "10.0pt", "body_size": "8.4pt", "body_leading": "0.32em", "comm_size": "7.2pt", "comm_leading": "0.26em", "sutra_spacing": "0.14em"},
    2: {"tier": 2, "deva_size": "10.4pt", "body_size": "8.7pt", "body_leading": "0.35em", "comm_size": "7.5pt", "comm_leading": "0.29em", "sutra_spacing": "0.25em"},
    3: {"tier": 3, "deva_size": "10.8pt", "body_size": "9.0pt", "body_leading": "0.38em", "comm_size": "7.7pt", "comm_leading": "0.32em", "sutra_spacing": "0.38em"},
    4: {"tier": 4, "deva_size": "11.2pt", "body_size": "9.3pt", "body_leading": "0.42em", "comm_size": "8.0pt", "comm_leading": "0.35em", "sutra_spacing": "0.60em"},
    5: {"tier": 5, "deva_size": "11.8pt", "body_size": "9.6pt", "body_leading": "0.46em", "comm_size": "8.3pt", "comm_leading": "0.38em", "sutra_spacing": "0.95em"},
}

_EXTREME_TIER_0 = {
    "tier": 0,
    "deva_size": "9.6pt",
    "body_size": "8.1pt",
    "body_leading": "0.27em",
    "comm_size": "6.9pt",
    "comm_leading": "0.23em",
    "sutra_spacing": "0.06em",
}


def calculate_profile(p_num: int, sutras: list[dict]) -> dict:
    s_count = len(sutras)
    trans_chars = sum(len(s.get("translation", "")) for s in sutras)
    comm_chars = sum(len(s.get("commentary", "")) for s in sutras)
    has_colophon = any(s.get("colophon") for s in sutras)
    total_chars = trans_chars + comm_chars

    if p_num in (8, 378, 438, 460):
        return dict(_TIER_PROFILES[0])
    if p_num in (282, 286):
        return dict(_EXTREME_TIER_0)
    if p_num == 70 or (s_count >= 11 and total_chars > 800):
        return dict(_TIER_PROFILES[1])

    est_lines = s_count * 2.1 + (trans_chars / 75.0) + (comm_chars / 95.0) + (2.5 if has_colophon else 0.0)
    if est_lines >= 38.0 or comm_chars > 2200 or total_chars > 2600:
        tier = 1
    elif est_lines >= 34.0 or comm_chars > 1900 or total_chars > 2300:
        tier = 2
    elif est_lines >= 30.0 or comm_chars > 1400:
        tier = 3
    elif est_lines >= 24.0:
        tier = 4
    else:
        tier = 5
    return dict(_TIER_PROFILES[tier])


def main() -> None:
    master_path = REPO_ROOT / "data" / "ashtadhyayi_complete_boethlingk1887.json"
    with open(master_path, encoding="utf-8") as f:
        master = json.load(f)

    hyphens_path = REPO_ROOT / "data" / "original_hyphenations.json"
    hyphens = {}
    if hyphens_path.exists():
        with open(hyphens_path, encoding="utf-8") as f:
            hyphens = json.load(f)

    ensure_corrigenda_json(REPO_ROOT)

    sutras = master["sutras"]

    # Map last sutra of each pada
    last_sutra_of_pada = {}
    for s in sutras:
        key = (s["adhyaya"], s["pada"])
        last_sutra_of_pada[key] = s["ref"]

    # Group by page
    by_page = {}
    for s in sutras:
        p = s.get("page")
        if p:
            by_page.setdefault(p, []).append(s)

    calibrated_profiles_path = REPO_ROOT / "data" / "calibrated_dense_profiles.json"
    calibrated_profiles = {}
    if calibrated_profiles_path.exists():
        with open(calibrated_profiles_path, encoding="utf-8") as f:
            calibrated_profiles = json.load(f)

    pages_output = []
    for p_num in range(2, 477):
        p_sutras = by_page.get(p_num, [])
        processed = []
        for s in p_sutras:
            sc = dict(s)
            ref = s.get("ref", "")
            if ref in hyphens:
                sc["canonical_devanagari"] = hyphens[ref]
            if "canonical_iast" in sc:
                sc["canonical_iast"] = soft_hyphenate_long_iast(sc["canonical_iast"])
            sc["sutra_num_deva"] = to_deva_num(s.get("sutra_num", 0))

            is_end = (ref == last_sutra_of_pada.get((s["adhyaya"], s["pada"])))
            sc["is_pada_end"] = is_end
            if is_end:
                sc["colophon"] = get_colophon(s["adhyaya"], s["pada"])
            else:
                sc["colophon"] = ""
            processed.append(sc)

        first_s = p_sutras[0] if p_sutras else {}
        last_s = p_sutras[-1] if p_sutras else {}
        a_num = first_s.get("adhyaya", 1)
        p_num_in_adh = first_s.get("pada", 1)

        prof = calibrated_profiles[str(p_num)] if str(p_num) in calibrated_profiles else calculate_profile(p_num, processed)

        pages_output.append({
            "page_num": p_num,
            "adh_num": a_num,
            "pada_num": p_num_in_adh,
            "header_adh_str": f"{adh_romans.get(a_num, 'I')}. Adhyāya. {p_num_in_adh}. Pāda.",
            "last_sutra_ref": f"{last_s.get('adhyaya', 1)}, {last_s.get('pada', 1)}, {last_s.get('sutra_num', 1)}.",
            "profile": prof,
            "sutras": processed,
        })

    out_path = REPO_ROOT / "data" / "ashtadhyayi_facsimile_dense.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pages_output, f, ensure_ascii=False, indent=2)

    print(f"Erfolgreich {len(pages_output)} Seiten (S. 2–476) mit adaptiven Profilen exportiert nach {out_path}")


if __name__ == "__main__":
    main()
