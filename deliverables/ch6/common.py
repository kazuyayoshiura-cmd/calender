import json
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-calender/fa5aa6a6-fb44-5544-883f-6c163ad9f321/scratchpad/ch4")
from lib import Slide, HEAD, INK, SUB  # noqa: F401

NAVY = "#0E2E63"; BLUE = "#1F4E8C"; RED = "#D42A2A"


def header(s, tag, title):
    s.rect([20, 10, 166, 58], fill=NAVY, r=6, text=tag, size_px=30, bold=True, color="#FFFFFF")
    s.text([206, 6, 1440, 66], title, 40, bold=True, color=HEAD)


def warn(s, box, lines, sizes=(26, 20)):
    s.rect(box, fill="#FDECEC", line={"color": "#E05050", "width_px": 2}, r=8)
    s.icon("material:warning-fill", [box[0] + 20, box[1] + (box[3] - 66) / 2, 66, 66], "#E02020")
    paras = [[{"text": t, "size_px": sz, "bold": True}] for t, sz in zip(lines, sizes)]
    s.rich([box[0] + 100, box[1], box[2] - 110, box[3]], paras, color=RED, line_pitch_px=36)


def num(s, cx, cy, n, fill=NAVY, d=44, size=22):
    s.add(type="ellipse", box=[cx - d / 2, cy - d / 2, d, d], fill=fill, line=None, text=str(n), size_px=size, bold=True, color="#FFFFFF")


def dump(s, path="spec.json"):
    json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": s.E}, open(path, "w"), ensure_ascii=False, indent=1)
    print(len(s.E), "elements")
