#!/usr/bin/env python3
"""Bundled icon libraries: lookup, recolor, search, and contact sheets.

Libraries (all under assets/icons/):
  azure   - Microsoft Azure Architecture Icons (multi-color SVG, keep original colors)
  lucide  - Lucide outline icons (generic: server, database, shield, user, file...)
  material- Google Material Symbols, rounded (solid "<name>-fill" and outline "<name>")
  simple  - Simple Icons brand logos (docker, postgresql, nvidia, github...)

CLI:
  icons.py search <keyword> [<keyword> ...] [--lib azure|lucide|simple] [--limit 12]
  icons.py sheet  <out.png> <lib:name> [<lib:name> ...]      # labelled preview grid
  icons.py svg    <lib:name> [--color #hex] [--stroke 2]      # print SVG
"""
import argparse
import functools
import io
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "icons")
LIBS = ("azure", "lucide", "material", "simple")


@functools.lru_cache(None)
def _lucide():
    return json.load(open(os.path.join(ROOT, "lucide.json"), encoding="utf-8"))["icons"]


@functools.lru_cache(None)
def _simple():
    return json.load(open(os.path.join(ROOT, "simple-icons.json"), encoding="utf-8"))["icons"]


@functools.lru_cache(None)
def _material():
    return json.load(open(os.path.join(ROOT, "material.json"), encoding="utf-8"))["icons"]


@functools.lru_cache(None)
def _material_alias():
    # material names mix "_" (base) and "-fill" (suffix); accept either separator
    return {k.replace("-", "_"): k for k in _material()}


@functools.lru_cache(None)
def _azure():
    d = os.path.join(ROOT, "azure")
    return sorted(f[:-4] for f in os.listdir(d) if f.endswith(".svg"))


def names(lib):
    return {"azure": _azure, "lucide": lambda: list(_lucide()), "material": lambda: list(_material()), "simple": lambda: list(_simple())}[lib]()


def parse_ref(ref):
    if ":" not in ref:
        raise ValueError(f"icon ref must be lib:name, got {ref!r}")
    lib, name = ref.split(":", 1)
    if lib not in LIBS:
        raise ValueError(f"unknown icon lib {lib!r} (use {', '.join(LIBS)})")
    return lib, name


def get_svg(lib, name, color=None, stroke_width=None):
    """Return SVG text. color recolors lucide (stroke) / material, simple (fill); azure keeps its colors."""
    if lib == "azure":
        path = os.path.join(ROOT, "azure", name + ".svg")
        if not os.path.exists(path):
            raise KeyError(f"azure:{name} not found")
        svg = open(path, encoding="utf-8").read()
        return re.sub(r"<title>.*?</title>", "", svg, flags=re.S)
    if lib == "lucide":
        icon = _lucide().get(name)
        if icon is None:
            raise KeyError(f"lucide:{name} not found")
        parts = []
        for tag, attrs in icon["nodes"]:
            a = " ".join(f'{k}="{v}"' for k, v in attrs.items() if k != "key")
            parts.append(f"<{tag} {a}/>")
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
            f'fill="none" stroke="{color or "#000000"}" stroke-width="{stroke_width or 2}" '
            'stroke-linecap="round" stroke-linejoin="round">' + "".join(parts) + "</svg>"
        )
    if lib == "material":
        d = _material().get(_material_alias().get(name.replace("-", "_"), name))
        if d is None:
            raise KeyError(f"material:{name} not found")
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 -960 960 960">'
            f'<path fill="{color or "#000000"}" d="{d}"/></svg>'
        )
    icon = _simple().get(name)
    if icon is None:
        raise KeyError(f"simple:{name} not found")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">'
        f'<path fill="{color or icon.get("hex", "#000000")}" d="{icon["d"]}"/></svg>'
    )


def render_png(svg, px):
    import cairosvg

    return cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=px, output_height=px)


def search(keywords, lib=None, limit=12):
    kws = [k.lower() for k in keywords]
    results = []
    for L in ([lib] if lib else LIBS):
        for n in names(L):
            hay_name = n.lower()
            tags = []
            if L == "lucide":
                tags = [t.lower() for t in _lucide()[n]["tags"]]
            elif L == "simple":
                tags = [_simple()[n]["title"].lower()]
            score = 0
            for k in kws:
                if hay_name == k:
                    score += 10
                elif re.search(rf"(^|[-_]){re.escape(k)}($|[-_])", hay_name):
                    score += 6
                elif k in hay_name:
                    score += 3
                if any(t == k for t in tags):
                    score += 4
                elif any(k in t for t in tags):
                    score += 1
            if score:
                results.append((score, L, n))
    results.sort(key=lambda r: (-r[0], len(r[2])))
    return results[:limit]


def contact_sheet(out, refs, cell=120):
    from PIL import Image, ImageDraw

    cols = min(6, max(1, len(refs)))
    rows = (len(refs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 24)), "white")
    draw = ImageDraw.Draw(sheet)
    for i, ref in enumerate(refs):
        lib, name = parse_ref(ref)
        x, y = (i % cols) * cell, (i // cols) * (cell + 24)
        try:
            png = Image.open(io.BytesIO(render_png(get_svg(lib, name), cell - 40))).convert("RGBA")
            sheet.paste(png, (x + 20, y + 10), png)
        except KeyError:
            draw.text((x + 20, y + 50), "NOT FOUND", fill="red")
        draw.text((x + 4, y + cell), ref[:22], fill="black")
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("keywords", nargs="+")
    s.add_argument("--lib", choices=LIBS)
    s.add_argument("--limit", type=int, default=12)
    s.add_argument("--sheet", help="also write a contact sheet of the hits")
    c = sub.add_parser("sheet")
    c.add_argument("out")
    c.add_argument("refs", nargs="+")
    v = sub.add_parser("svg")
    v.add_argument("ref")
    v.add_argument("--color")
    v.add_argument("--stroke", type=float)
    a = ap.parse_args()
    if a.cmd == "search":
        hits = search(a.keywords, a.lib, a.limit)
        for score, lib, n in hits:
            print(f"{lib}:{n}\t{score}")
        if a.sheet and hits:
            print(contact_sheet(a.sheet, [f"{l}:{n}" for _, l, n in hits]))
    elif a.cmd == "sheet":
        print(contact_sheet(a.out, a.refs))
    else:
        print(get_svg(*parse_ref(a.ref), color=a.color, stroke_width=a.stroke))


if __name__ == "__main__":
    sys.exit(main())
