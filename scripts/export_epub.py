#!/usr/bin/env python3
"""
scripts/export_epub.py — Exports Otto von Böhtlingk's Pāṇini (1887)
into a standardized, reflowable EPUB 3 eBook with embedded Unicode fonts
(Noto Serif Devanagari + Linux Libertine O) for e-readers and mobile devices.
"""
from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import re
import shutil
import sys
import uuid
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional


def log(msg: str):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] [export_epub] {msg}", file=sys.stderr)


EPUB_CSS = """/* Boethlingk 1887 — Universal Scholarly EPUB 3 Stylesheet */
@namespace epub "http://www.idpf.org/2007/ops";

@font-face {
    font-family: "Linux Libertine O";
    font-style: normal;
    font-weight: normal;
    src: url("../fonts/LinLibertine_R.otf") format("opentype");
}
@font-face {
    font-family: "Linux Libertine O";
    font-style: normal;
    font-weight: bold;
    src: url("../fonts/LinLibertine_RB.otf") format("opentype");
}
@font-face {
    font-family: "Linux Libertine O";
    font-style: italic;
    font-weight: normal;
    src: url("../fonts/LinLibertine_RI.otf") format("opentype");
}
@font-face {
    font-family: "Noto Serif Devanagari";
    font-style: normal;
    font-weight: normal;
    src: url("../fonts/NotoSerifDevanagari-Regular.ttf") format("truetype");
}
@font-face {
    font-family: "Noto Serif Devanagari";
    font-style: normal;
    font-weight: bold;
    src: url("../fonts/NotoSerifDevanagari-Bold.ttf") format("truetype");
}

body {
    font-family: "Linux Libertine O", "Noto Serif Devanagari", "DejaVu Serif", serif;
    font-size: 1.05em;
    line-height: 1.55;
    margin: 5% 7%;
    text-align: justify;
    text-rendering: optimizeLegibility;
    -webkit-hyphens: auto;
    -moz-hyphens: auto;
    hyphens: auto;
}

h1, h2, h3, h4 {
    font-family: "Linux Libertine O", "Noto Serif Devanagari", serif;
    font-weight: bold;
    line-height: 1.25;
    margin-top: 1.8em;
    margin-bottom: 0.8em;
    text-align: left;
    page-break-after: avoid;
    break-after: avoid;
}

h1 {
    font-size: 1.8em;
    text-align: center;
    margin-top: 2.2em;
    margin-bottom: 1.2em;
}

h2 {
    font-size: 1.4em;
    border-bottom: 1px solid #ddd;
    padding-bottom: 0.25em;
    margin-top: 2em;
}

h3 {
    font-size: 1.15em;
    color: #444;
}

p {
    margin: 0.4em 0;
}

/* Title Page */
.title-page {
    text-align: center;
    margin-top: 20%;
    margin-bottom: 20%;
}
.title-page h1 {
    font-size: 2.3em;
    margin-bottom: 0.2em;
}
.title-page .subtitle {
    font-size: 1.15em;
    font-style: italic;
    margin-bottom: 2em;
    color: #444;
}
.title-page .author {
    font-size: 1.35em;
    font-weight: bold;
    margin-top: 1.5em;
}
.title-page .publisher {
    font-size: 0.95em;
    color: #666;
    margin-top: 4em;
}

/* Sūtra Container */
.sutra {
    margin: 1.4em 0;
    padding: 0.8em 1em;
    background-color: #fbfbfb;
    border-left: 3px solid #6c757d;
    border-radius: 2px;
    page-break-inside: avoid;
    break-inside: avoid;
}

.sutra-head {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.6em;
    margin-bottom: 0.5em;
    font-size: 1.1em;
    border-bottom: 1px dotted #ccc;
    padding-bottom: 0.3em;
}

.sutra-ref {
    font-family: "Linux Libertine O", sans-serif;
    font-weight: bold;
    color: #8b0000;
    background: #f0ebe4;
    padding: 0.1em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}

.sutra-devanagari {
    font-family: "Noto Serif Devanagari", serif;
    font-weight: bold;
    font-size: 1.25em;
    color: #111;
}

.sutra-iast {
    font-family: "Linux Libertine O", serif;
    font-style: italic;
    color: #444;
}

.sutra-page {
    margin-left: auto;
    font-size: 0.8em;
    color: #888;
}

.translation {
    font-size: 1.0em;
    font-weight: normal;
    color: #1a1a1a;
    margin: 0.5em 0;
}

.commentary {
    font-size: 0.92em;
    color: #333;
    margin-top: 0.5em;
    padding-left: 0.6em;
    border-left: 2px solid #e0e0e0;
}

/* Corrigenda */
.corrigendum-item {
    margin: 0.6em 0;
    padding: 0.4em 0;
    border-bottom: 1px dotted #e0e0e0;
}
"""


def load_dataset(base_dir: Path) -> tuple[list, list, list]:
    grouped_path = base_dir / "data/ashtadhyayi_grouped_edition.json"
    if not grouped_path.exists():
        log("Bereite gruppierte Daten vor...")
        sys.path.insert(0, str(base_dir))
        from scripts.build_typeset_edition import prepare_data
        prepare_data()

    with open(grouped_path, encoding="utf-8") as f:
        grouped = json.load(f)

    shiva_sutras = []
    shiva_path = base_dir / "data/shiva_sutras.json"
    if shiva_path.exists():
        with open(shiva_path, encoding="utf-8") as f:
            shiva_sutras = json.load(f)

    corrigenda = []
    corr_path = base_dir / "data/corrigenda.json"
    if corr_path.exists():
        with open(corr_path, encoding="utf-8") as f:
            corrigenda = json.load(f)

    return grouped, shiva_sutras, corrigenda


def escape_xml(text: str) -> str:
    if not text:
        return ""
    return html.escape(str(text))


def clean_commentary_html(comm: str) -> str:
    if not comm:
        return ""
    paras = [p.strip() for p in comm.split("\n\n") if p.strip()]
    if not paras:
        paras = [comm.strip()]
    out = []
    for p in paras:
        out.append(f"<p>{escape_xml(p)}</p>")
    return "\n".join(out)


def build_epub(base_dir: Path, output_path: Path):
    t_start = datetime.datetime.now()
    log(f"Starte EPUB 3 Generierung -> {output_path}")

    grouped_tree, shiva_sutras, corrigenda = load_dataset(base_dir)
    work_dir = base_dir / "data/output/_epub_build"
    if work_dir.exists():
        shutil.rmtree(work_dir)

    oebps = work_dir / "OEBPS"
    text_dir = oebps / "text"
    fonts_dir = oebps / "fonts"
    styles_dir = oebps / "styles"
    meta_inf = work_dir / "META-INF"

    text_dir.mkdir(parents=True, exist_ok=True)
    fonts_dir.mkdir(parents=True, exist_ok=True)
    styles_dir.mkdir(parents=True, exist_ok=True)
    meta_inf.mkdir(parents=True, exist_ok=True)

    # 1. mimetype
    with open(work_dir / "mimetype", "w", encoding="utf-8") as f:
        f.write("application/epub+zip")

    # 2. container.xml
    with open(meta_inf / "container.xml", "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>""")

    # 3. CSS
    with open(styles_dir / "stylesheet.css", "w", encoding="utf-8") as f:
        f.write(EPUB_CSS)

    # 4. Copy Fonts
    font_src_dir = base_dir / "data/fonts"
    embedded_fonts = []
    font_files = [
        ("LinLibertine_R.otf", "application/vnd.ms-opentype"),
        ("LinLibertine_RB.otf", "application/vnd.ms-opentype"),
        ("LinLibertine_RI.otf", "application/vnd.ms-opentype"),
        ("NotoSerifDevanagari-Regular.ttf", "application/x-font-truetype"),
        ("NotoSerifDevanagari-Bold.ttf", "application/x-font-truetype"),
    ]
    for fn, mtype in font_files:
        src = font_src_dir / fn
        if src.exists():
            shutil.copy2(src, fonts_dir / fn)
            embedded_fonts.append((fn, mtype))
            log(f"Font eingebettet: {fn} ({src.stat().st_size / 1024:.1f} KB)")
        else:
            log(f"WARNUNG: Font {fn} nicht gefunden in {font_src_dir}!")

    # 5. Build Content Documents
    manifest_items = []
    spine_items = []
    toc_entries = []

    # Titlepage
    title_xhtml = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
<head>
  <meta charset="utf-8" />
  <title>Pâṇini's Grammatik</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body epub:type="frontmatter">
  <section class="title-page" epub:type="titlepage">
    <h1>Pâṇini's Grammatik</h1>
    <div class="subtitle">Herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen</div>
    <div class="author">von Otto Böhtlingk</div>
    <div class="publisher">Leipzig • Verlag von H. Haessel • 1887<br/>Digitale Edition: birchville-org/boethlingk</div>
  </section>
</body>
</html>"""
    with open(text_dir / "titlepage.xhtml", "w", encoding="utf-8") as f:
        f.write(title_xhtml)
    manifest_items.append(("titlepage", "text/titlepage.xhtml", "application/xhtml+xml"))
    spine_items.append("titlepage")
    toc_entries.append(("Titelblatt", "text/titlepage.xhtml", []))

    # Śiva-Sūtras
    if shiva_sutras:
        shiva_html_parts = [
            """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="sa">
<head>
  <meta charset="utf-8" />
  <title>Śiva-Sūtrāṇi</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body>
  <section id="shiva-sutras">
    <h1>Śiva-Sūtrāṇi (Māheśvara-Sūtras)</h1>
    <p><em>Die 14 einleitenden Lautsūtras zur Ableitung der grammatischen Pratyāhāras.</em></p>
"""
        ]
        for s in shiva_sutras:
            ref = s.get("ref", "")
            s_ocr = escape_xml(s.get("sutra_ocr", ""))
            s_can = escape_xml(s.get("canonical_devanagari", "") or s_ocr)
            s_iast = escape_xml(s.get("canonical_iast", ""))
            page = s.get("page", 1)
            shiva_html_parts.append(f"""
    <article class="sutra" id="sutra-{ref}">
      <header class="sutra-head">
        <span class="sutra-ref">{ref}</span>
        <span class="sutra-devanagari">{s_can}</span>
        {f'<span class="sutra-iast">{s_iast}</span>' if s_iast else ''}
        <span class="sutra-page">[S. {page}]</span>
      </header>
    </article>
""")
        shiva_html_parts.append("  </section>\n</body>\n</html>")
        with open(text_dir / "shiva.xhtml", "w", encoding="utf-8") as f:
            f.write("\n".join(shiva_html_parts))
        manifest_items.append(("shiva", "text/shiva.xhtml", "application/xhtml+xml"))
        spine_items.append("shiva")
        toc_entries.append(("Śiva-Sūtrāṇi (Māheśvara-Sūtras)", "text/shiva.xhtml", []))

    # 8 Adhyāyas
    for adh in grouped_tree:
        a_num = adh["num"]
        a_title_de = adh["title_de"]
        a_title_sa = adh["title_sa"]
        doc_id = f"adhyaya_{a_num}"
        fn = f"adh_{a_num}.xhtml"

        adh_parts = [
            f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
<head>
  <meta charset="utf-8" />
  <title>{a_title_de} ({a_title_sa})</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body>
  <section id="adh-{a_num}">
    <h1>{a_title_de}<br/><span style="font-size:0.65em; font-weight:normal; font-style:italic;">{a_title_sa}</span></h1>
"""
        ]

        pada_toc = []
        for pada in adh.get("padas", []):
            p_num = pada["num"]
            p_title_de = pada["title_de"]
            p_title_sa = pada["title_sa"]
            pada_id = f"adh-{a_num}-pada-{p_num}"

            adh_parts.append(f"""
    <section id="{pada_id}">
      <h2>{p_title_de} ({p_title_sa})</h2>
""")
            sutras = pada.get("sutras", [])
            for s in sutras:
                ref = s.get("ref", "")
                can_dev = escape_xml(s.get("canonical_devanagari", "") or s.get("sutra_ocr", ""))
                can_iast = escape_xml(s.get("canonical_iast", ""))
                trans = escape_xml(s.get("translation", ""))
                comm = s.get("commentary", "")
                page = s.get("page", "")

                adh_parts.append(f"""
      <article class="sutra" id="sutra-{ref}">
        <header class="sutra-head">
          <span class="sutra-ref">{ref}</span>
          <span class="sutra-devanagari">{can_dev}</span>
          {f'<span class="sutra-iast">{can_iast}</span>' if can_iast else ''}
          {f'<span class="sutra-page">[S. {page}]</span>' if page else ''}
        </header>
        {f'<div class="translation">{trans}</div>' if trans else ''}
        {f'<div class="commentary">{clean_commentary_html(comm)}</div>' if comm else ''}
      </article>
""")
            adh_parts.append("    </section>\n")
            pada_toc.append((f"{p_title_de} ({p_title_sa})", f"text/{fn}#{pada_id}"))

        adh_parts.append("  </section>\n</body>\n</html>")
        with open(text_dir / fn, "w", encoding="utf-8") as f:
            f.write("\n".join(adh_parts))

        manifest_items.append((doc_id, f"text/{fn}", "application/xhtml+xml"))
        spine_items.append(doc_id)
        toc_entries.append((f"{a_title_de} ({a_title_sa})", f"text/{fn}", pada_toc))

    # Corrigenda (Nachträge & Verbesserungen)
    if corrigenda:
        corr_parts = [
            """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
<head>
  <meta charset="utf-8" />
  <title>Nachträge und Verbesserungen</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body epub:type="backmatter">
  <section id="corrigenda">
    <h1>Nachträge und Verbesserungen</h1>
    <p><em>Böhtlingks Verzeichnis der Berichtigungen und Ergänzungen (Buchseiten 477–478).</em></p>
    <div class="corrigenda-list">
"""
        ]
        for it in corrigenda:
            txt = escape_xml(it.get("text", ""))
            corr_parts.append(f'      <div class="corrigendum-item">{txt}</div>\n')
        corr_parts.append("    </div>\n  </section>\n</body>\n</html>")

        with open(text_dir / "corrigenda.xhtml", "w", encoding="utf-8") as f:
            f.write("\n".join(corr_parts))
        manifest_items.append(("corrigenda", "text/corrigenda.xhtml", "application/xhtml+xml"))
        spine_items.append("corrigenda")
        toc_entries.append(("Nachträge und Verbesserungen", "text/corrigenda.xhtml", []))

    # 6. nav.xhtml (EPUB 3 Navigation Document)
    nav_parts = [
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="de">
<head>
  <meta charset="utf-8" />
  <title>Inhaltsverzeichnis</title>
  <link rel="stylesheet" type="text/css" href="../styles/stylesheet.css" />
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Inhaltsverzeichnis</h1>
    <ol>
"""
    ]
    for title, href, children in toc_entries:
        if children:
            nav_parts.append(f'      <li><a href="{href}">{escape_xml(title)}</a>\n        <ol>\n')
            for c_title, c_href in children:
                nav_parts.append(f'          <li><a href="{c_href}">{escape_xml(c_title)}</a></li>\n')
            nav_parts.append('        </ol>\n      </li>\n')
        else:
            nav_parts.append(f'      <li><a href="{href}">{escape_xml(title)}</a></li>\n')
    nav_parts.append("""    </ol>
  </nav>
</body>
</html>""")
    with open(oebps / "nav.xhtml", "w", encoding="utf-8") as f:
        f.write("".join(nav_parts))
    manifest_items.append(("nav", "nav.xhtml", "application/xhtml+xml", "properties=\"nav\""))

    # 7. toc.ncx (EPUB 2 backward compatibility for Tolino, older Kindles)
    ncx_parts = [
        f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.openmobilealliance.org/tech/DTD/ncx-2005-1.dtd" version="2005-1" xml:lang="de">
  <head>
    <meta name="dtb:uid" content="urn:uuid:boethlingk-panini-1887"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>Pâṇini's Grammatik (Otto Böhtlingk 1887)</text></docTitle>
  <navMap>
"""
    ]
    play_order = 1
    for title, href, children in toc_entries:
        ncx_parts.append(f"""    <navPoint id="np_{play_order}" playOrder="{play_order}">
      <navLabel><text>{escape_xml(title)}</text></navLabel>
      <content src="{href}"/>
""")
        play_order += 1
        for c_title, c_href in children:
            ncx_parts.append(f"""      <navPoint id="np_{play_order}" playOrder="{play_order}">
        <navLabel><text>{escape_xml(c_title)}</text></navLabel>
        <content src="{c_href}"/>
      </navPoint>
""")
            play_order += 1
        ncx_parts.append("    </navPoint>\n")
    ncx_parts.append("  </navMap>\n</ncx>")
    with open(oebps / "toc.ncx", "w", encoding="utf-8") as f:
        f.write("".join(ncx_parts))
    manifest_items.append(("ncx", "toc.ncx", "application/x-dtbncx+xml"))

    # 8. content.opf
    opf_parts = [
        """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id" xml:lang="de">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">urn:uuid:boethlingk-panini-1887</dc:identifier>
    <dc:title>Pâṇini's Grammatik</dc:title>
    <dc:creator>Otto Böhtlingk</dc:creator>
    <dc:language>de</dc:language>
    <dc:language>sa</dc:language>
    <dc:publisher>Verlag von H. Haessel, Leipzig</dc:publisher>
    <dc:description>Pâṇini's Grammatik, herausgegeben, übersetzt, erläutert und mit verschiedenen Indices versehen von Otto Böhtlingk (1887). Vollständige digitale Ausgabe der 3.997 Sūtras.</dc:description>
    <meta property="dcterms:modified">""" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """</meta>
  </metadata>
  <manifest>
    <item id="css" href="styles/stylesheet.css" media-type="text/css"/>
"""
    ]

    for item in manifest_items:
        item_id = item[0]
        href = item[1]
        mtype = item[2]
        props = f" {item[3]}" if len(item) > 3 else ""
        opf_parts.append(f'    <item id="{item_id}" href="{href}" media-type="{mtype}"{props}/>\n')

    for fn, mtype in embedded_fonts:
        fid = f"font_{fn.replace('.', '_')}"
        opf_parts.append(f'    <item id="{fid}" href="fonts/{fn}" media-type="{mtype}"/>\n')

    opf_parts.append('  </manifest>\n  <spine toc="ncx">\n')
    for sp in spine_items:
        opf_parts.append(f'    <itemref idref="{sp}"/>\n')
    opf_parts.append('  </spine>\n</package>')

    with open(oebps / "content.opf", "w", encoding="utf-8") as f:
        f.write("".join(opf_parts))

    # 9. Packaging into ZIP/EPUB
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as zf:
        # First file MUST be mimetype, uncompressed!
        zf.write(work_dir / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)

        # Everything else can be deflated
        for root, dirs, files in os.walk(work_dir):
            for file in sorted(files):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(work_dir)
                if str(rel_path) == "mimetype":
                    continue
                zf.write(full_path, str(rel_path), compress_type=zipfile.ZIP_DEFLATED)

    # Cleanup temp dir
    shutil.rmtree(work_dir)

    elapsed = (datetime.datetime.now() - t_start).total_seconds()
    size_mb = output_path.stat().st_size / (1024 * 1024)
    log("=" * 60)
    log(f"EPUB 3 erfolgreich erstellt: {output_path}")
    log(f"Dateigröße: {size_mb:.2f} MB | Dauer: {elapsed:.2f} s")
    log("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Export Boethlingk 1887 as EPUB 3 eBook")
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("/Volumes/SanDisk1TB/proj/boethlingk"),
        help="Base directory of boethlingk repo",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("/Volumes/SanDisk1TB/proj/boethlingk/data/output/boethlingk1887.epub"),
        help="Target EPUB path",
    )
    args = parser.parse_args()
    build_epub(args.dir, args.output)


if __name__ == "__main__":
    main()
