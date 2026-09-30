"""Render every slide of a pptx to prev/slide<N>.png (1672px wide)."""
import os
import subprocess
import sys

import fitz

pptx = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "prev"
os.makedirs(out, exist_ok=True)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, pptx], check=True, capture_output=True, timeout=180)
doc = fitz.open(os.path.join(out, os.path.splitext(os.path.basename(pptx))[0] + ".pdf"))
for i, page in enumerate(doc):
    z = 1672 / page.rect.width
    page.get_pixmap(matrix=fitz.Matrix(z, z)).save(os.path.join(out, f"slide{i + 1}.png"))
    print(os.path.join(out, f"slide{i + 1}.png"))
