#!/usr/bin/env python3
"""Render a .pptx to PNG and compare it with the source image.

  preview.py <deck.pptx> <src.png> <out_dir>

Writes <out_dir>/preview.png (slide 1 at source resolution), compare.png
(source | preview side by side) and overlay.png (50% blend, misalignment shows as ghosting).
Needs LibreOffice (soffice). Fonts in this sandbox differ from Windows/Mac Office, so
judge text size/position, not exact glyph shapes.
"""
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image


def render(pptx, W, H):
    tmp = tempfile.mkdtemp()
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise SystemExit("soffice not found: install LibreOffice to preview")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, pptx], check=True, capture_output=True, timeout=180)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(pptx))[0] + ".pdf")
    import fitz

    doc = fitz.open(pdf)
    page = doc[0]
    zoom = W / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return img.resize((W, H))


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    pptx, src, out_dir = sys.argv[1:]
    os.makedirs(out_dir, exist_ok=True)
    s = Image.open(src).convert("RGB")
    p = render(pptx, *s.size)
    p.save(os.path.join(out_dir, "preview.png"))
    cmp_ = Image.new("RGB", (s.width * 2 + 10, s.height), "white")
    cmp_.paste(s, (0, 0))
    cmp_.paste(p, (s.width + 10, 0))
    cmp_.save(os.path.join(out_dir, "compare.png"))
    Image.blend(s, p, 0.5).save(os.path.join(out_dir, "overlay.png"))
    for f in ("preview.png", "compare.png", "overlay.png"):
        print(os.path.join(out_dir, f))
    return 0


if __name__ == "__main__":
    sys.exit(main())
