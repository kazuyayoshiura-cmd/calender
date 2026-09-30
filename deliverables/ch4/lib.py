"""Shared helpers for chapter-4 slide specs (canvas 1672x941, 16:9)."""
import json

NAVY = "#1F3F7A"; HEAD = "#1F3A6E"; INK = "#1E2A44"; SUB = "#33466A"; ARROW = "#1F3A6E"
BOX_FILL = "#EEF5FC"; BOX_LINE = "#3A5F8F"
KINDS = {
    "box": ("#EEF5FC", "#3A5F8F"), "white": ("#FFFFFF", "#3A5F8F"), "blue": ("#DCEBFA", "#5B8FD0"),
    "yellow": ("#FFF3D6", "#E0B85A"), "green": ("#E3F2DC", "#8CC27A"), "pink": ("#FBDDE2", "#D9707F"),
    "final": ("#D8E9FA", "#7FAAD9"), "dash": ("#FFFFFF", "#3A5F8F"),
}


class Slide:
    def __init__(self):
        self.E = []

    def add(self, **k):
        self.E.append(k)
        return k

    def text(self, box, text, size, bold=False, color=INK, align="l", valign="m", **k):
        return self.add(type="text", box=box, text=text, size_px=size, bold=bold, color=color, align=align, valign=valign, **k)

    def rich(self, box, paras, color=INK, align="l", valign="m", **k):
        return self.add(type="text", box=box, paras=paras, color=color, align=align, valign=valign, **k)

    def rect(self, box, fill="#FFFFFF", line=None, r=None, **k):
        d = dict(type="roundRect" if r is not None else "rect", box=box, fill=fill, line=line, **k)
        if r is not None:
            d["radius_px"] = r
        return self.add(**d)

    def node(self, box, title, sub=None, kind="box", tsize=17, ssize=14.5, align="c", bullets=None, pitch=None, r=6, tcolor=HEAD):
        """Flow box: bold title + optional sub lines (regular) + optional bullet lines, all in the shape itself."""
        fill, line = KINDS[kind]
        ln = {"color": line, "width_px": 1.5, **({"dash": "dash"} if kind == "dash" else {})}
        paras = [[{"text": title, "size_px": tsize, "bold": True, "color": tcolor}]]
        for s in (sub.split("\n") if sub else []):
            paras.append([{"text": s, "size_px": ssize, "color": SUB}])
        for b in bullets or []:
            paras.append([{"text": "・" + b, "size_px": ssize, "color": SUB}])
        d = dict(type="roundRect", box=box, radius_px=r, fill=fill, line=ln, paras=paras, align=align, color=SUB,
                 line_pitch_px=pitch or round(ssize * 1.45, 1), inset_px=[8, 2, 8, 2])
        return self.add(**d)

    def diamond(self, box, text, size=15, kind="blue"):
        fill, line = KINDS[kind]
        return self.add(type="diamond", box=box, fill=fill, line={"color": line, "width_px": 1.5}, text=text, size_px=size,
                        bold=True, color=HEAD, line_pitch_px=round(size * 1.35, 1))

    def arrow(self, pts, w=2.2, color=ARROW, dash=None, head="end"):
        d = dict(type="arrow", points=pts, color=color, width_px=w, head=head)
        if dash:
            d["dash"] = dash
        return self.add(**d)

    def line(self, pts, w=2.2, color=ARROW, dash=None):
        d = dict(type="line", points=pts, color=color, width_px=w)
        if dash:
            d["dash"] = dash
        return self.add(**d)

    def label(self, box, text, size=14, align="l", color=INK, bold=False):
        return self.text(box, text, size, bold=bold, color=color, align=align)

    def icon(self, ref, box, color=NAVY, **k):
        return self.add(type="icon", icon=ref, box=box, color=color, **k)

    def title(self, text, sub=None):
        self.text([30, 10, 1612, 54], text, 34, bold=True, color=HEAD, name="title")

    def dump(self, path="spec.json", slides=None):
        doc = {"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF"}
        if slides:
            doc["slides"] = slides
        else:
            doc["elements"] = self.E
        json.dump(doc, open(path, "w"), ensure_ascii=False, indent=1)
        print(len(self.E), "elements")
