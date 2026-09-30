#!/usr/bin/env python3
"""Source-image measurement helpers.

  inspect_image.py grid   <src.png> <out.png> [--step 50]           # coordinate grid overlay
  inspect_image.py crop   <src.png> <out.png> x y w h [--scale 3] [--step 10]  # zoomed crop with grid
  inspect_image.py colors <src.png> x,y [x,y ...]                    # exact hex at points (3x3 median)
  inspect_image.py palette <src.png> [--n 12]                        # dominant colors
"""
import argparse
import sys

from PIL import Image, ImageDraw


def _grid(img, step, origin=(0, 0), scale=1.0):
    d = ImageDraw.Draw(img)
    W, H = img.size
    ox, oy = origin
    major = step * 5
    first_x = (-(ox % step)) % step
    for sx in range(int(first_x), int(W / scale) + 1, step):
        v = ox + sx
        X = sx * scale
        is_major = v % major == 0
        d.line([(X, 0), (X, H)], fill=(255, 0, 0, 150) if is_major else (255, 0, 0, 55), width=1)
        if is_major or scale >= 3:
            d.text((X + 2, 2), str(v), fill=(200, 0, 0, 255))
    first_y = (-(oy % step)) % step
    for sy in range(int(first_y), int(H / scale) + 1, step):
        v = oy + sy
        Y = sy * scale
        is_major = v % major == 0
        d.line([(0, Y), (W, Y)], fill=(0, 0, 255, 150) if is_major else (0, 0, 255, 55), width=1)
        if is_major or scale >= 3:
            d.text((2, Y + 2), str(v), fill=(0, 0, 200, 255))
    return img


def grid(src, out, step):
    img = Image.open(src).convert("RGBA")
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    _grid(layer, step)
    Image.alpha_composite(img, layer).convert("RGB").save(out)


def crop(src, out, x, y, w, h, scale, step):
    img = Image.open(src).convert("RGBA").crop((x, y, x + w, y + h))
    img = img.resize((int(w * scale), int(h * scale)), Image.NEAREST)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    _grid(layer, step, origin=(x, y), scale=scale)
    Image.alpha_composite(img, layer).convert("RGB").save(out)


def colors(src, pts):
    img = Image.open(src).convert("RGB")
    for p in pts:
        x, y = (int(v) for v in p.split(","))
        px = [img.getpixel((min(max(x + dx, 0), img.width - 1), min(max(y + dy, 0), img.height - 1))) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        med = tuple(sorted(c[i] for c in px)[4] for i in range(3))
        print(f"{x},{y}\t#{med[0]:02X}{med[1]:02X}{med[2]:02X}")


def palette(src, n):
    img = Image.open(src).convert("RGB")
    img.thumbnail((400, 400))
    q = img.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    for c, idx in counts:
        r, g, b = pal[idx * 3: idx * 3 + 3]
        print(f"#{r:02X}{g:02X}{b:02X}\t{c / total:.1%}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grid")
    g.add_argument("src")
    g.add_argument("out")
    g.add_argument("--step", type=int, default=50)
    c = sub.add_parser("crop")
    c.add_argument("src")
    c.add_argument("out")
    for k in ("x", "y", "w", "h"):
        c.add_argument(k, type=int)
    c.add_argument("--scale", type=float, default=3)
    c.add_argument("--step", type=int, default=10)
    k = sub.add_parser("colors")
    k.add_argument("src")
    k.add_argument("pts", nargs="+")
    p = sub.add_parser("palette")
    p.add_argument("src")
    p.add_argument("--n", type=int, default=12)
    a = ap.parse_args()
    if a.cmd == "grid":
        grid(a.src, a.out, a.step)
    elif a.cmd == "crop":
        crop(a.src, a.out, a.x, a.y, a.w, a.h, a.scale, a.step)
    elif a.cmd == "colors":
        colors(a.src, a.pts)
    else:
        palette(a.src, a.n)


if __name__ == "__main__":
    sys.exit(main())
