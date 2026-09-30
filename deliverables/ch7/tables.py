"""表7-2 / 表7-3: icon + name column, then bullet columns."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-calender/fa5aa6a6-fb44-5544-883f-6c163ad9f321/scratchpad/ch6")
from common import *  # noqa

FILLS = ("#EAF3FC", "#FFFFFF")


def build(title, heads, cols, rows, T0=70, H0=44, total=868, name_sizes=(21, 15.5), bsize=16, colored_cells=False):
    s = Slide()
    s.text([24, 4, 1640, 62], title, 38, bold=True, color=HEAD)
    rh_each = (total - H0) / len(rows)
    rh = [H0] + [rh_each] * len(rows)
    Hd = lambda t: {"paras": [[{"text": x[0], "size_px": x[1], "bold": True} for x in t]], "fill": "#0E3F82", "color": "#FFFFFF", "align": "c"}
    cells = [[Hd(h) for h in heads]]
    for i, r in enumerate(rows):
        fill = FILLS[i % 2]
        row = [{"paras": [[{"text": r["name"], "size_px": name_sizes[0], "bold": True}], [{"text": r["sub"], "size_px": name_sizes[1]}]], "color": HEAD, "fill": fill,
                "align": "l", "line_pitch_px": rh_each * 0.4 if rh_each < 70 else 30, "inset_px": [96, 2, 4, 2]}]
        for c in r["cols"]:
            if isinstance(c, dict):  # product cell: title + bullets
                paras = [[{"text": t, "size_px": c.get("tsize", 19), "bold": True, "color": "#1356B0"}] for t in c["titles"]]
                paras += [[{"text": "・" + b, "size_px": bsize - 1}] for b in c["bullets"]]
                row.append({"paras": paras, "color": INK, "fill": "#F1F7FD" if colored_cells else fill, "align": "l", "valign": "m",
                            "line_pitch_px": c.get("pitch", 24), "inset_px": [16, 2, 6, 2]})
            else:
                row.append({"text": "\n".join(c), "size_px": bsize, "color": INK, "fill": fill, "align": "l", "valign": "m", "bullet": True,
                            "bullet_indent_px": 18, "line_pitch_px": min(27, rh_each / (len(c) + 0.6)), "inset_px": [24, 2, 6, 2]})
        cells.append(row)
    s.add(type="table", box=[16, T0, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells,
          border={"color": "#D6E1EE", "width_px": 1.5}, name="table")
    y = T0 + H0
    isz = min(52, rh_each - 14)
    for r in rows:
        s.icon(r["icon"], [36, y + (rh_each - isz) / 2, isz, isz], **r.get("icon_kw", {}))
        y += rh_each
    return s
