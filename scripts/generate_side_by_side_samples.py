#!/usr/bin/env python3
"""
Generates side-by-side comparison images (Original 1887 Scan vs. Neusatz)
for representative pages (1, 2, 8, 70, 476).
"""
from pathlib import Path
from PIL import Image
import pymupdf

doc = pymupdf.open("/Volumes/SanDisk1TB/proj/boethlingk/data/output/boethlingk1887_facsimile_dense_test.pdf")
out_dir = Path("/Volumes/SanDisk1TB/proj/boethlingk/data/output/comparisons")
out_dir.mkdir(parents=True, exist_ok=True)

test_pages = [1, 2, 8, 70, 476]

for p in test_pages:
    # PDF page index: front matter is 5 pages, so Page 1 is index 5, Page p is index 4 + p
    pdf_idx = 4 + p
    page = doc[pdf_idx]
    pix = page.get_pixmap(dpi=150)
    
    rend_path = out_dir / f"rendered_p{p:03d}.png"
    pix.save(str(rend_path))
    
    scan_path = Path(f"/Volumes/SanDisk1TB/proj/boethlingk/data/img_cache/7_3A000000{p:03d}_jpg_full_max_0_default_jpg.jpg")
    if not scan_path.exists():
        print(f"Scan not found for page {p} at {scan_path}")
        continue
        
    scan = Image.open(scan_path)
    rend = Image.open(rend_path)
    
    target_h = 1200
    scan_w = int(scan.width * target_h / scan.height)
    rend_w = int(rend.width * target_h / rend.height)
    
    scan_res = scan.resize((scan_w, target_h), Image.Resampling.LANCZOS)
    rend_res = rend.resize((rend_w, target_h), Image.Resampling.LANCZOS)
    
    comp = Image.new("RGB", (scan_w + rend_w + 30, target_h + 60), (250, 248, 245))
    
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(comp)
    # Header label
    draw.text((20, 15), f"HISTORISCHES ORIGINAL (Böhtlingk 1887, S. {p})", fill=(3, 25, 46))
    draw.text((scan_w + 50, 15), f"FAKSIMILE-NEUSATZ (Birchville Scholarly Synthesis, S. {p})", fill=(180, 83, 9))
    
    comp.paste(scan_res, (20, 45))
    comp.paste(rend_res, (scan_w + 40, 45))
    
    comp_file = out_dir / f"vergleich_seite_{p:03d}.png"
    comp.save(str(comp_file))
    print(f"✓ Erstellt: {comp_file} (Breite: {comp.width}px, Höhe: {comp.height}px)")

print("Vergleichsbilder erfolgreich in data/output/comparisons generiert!")
