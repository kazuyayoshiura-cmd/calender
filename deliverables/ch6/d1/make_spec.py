import sys
sys.path.insert(0, "..")
from common import *

s = Slide()
header(s, "図6-1", "版の新しさ × 対象への適用 による判定")

# axes
s.arrow([[252, 740], [252, 84]], w=3, color=NAVY)
s.arrow([[252, 740], [1644, 740]], w=3, color=NAVY)
s.line([[940, 88], [940, 736]], w=1.2, color="#8FA3BF", dash="dash")
s.line([[264, 414], [1632, 414]], w=1.2, color="#8FA3BF", dash="dash")

# y-axis labels
s.rich([36, 124, 210, 72], [[{"text": "適用確認", "size_px": 25, "bold": True, "color": HEAD}], [{"text": "（対象に適用可能）", "size_px": 19}]], color=INK, align="c", line_pitch_px=34)
s.rect([42, 348, 188, 106], fill=NAVY, r=8, text="対象への\n適用", size_px=27, bold=True, color="#FFFFFF", line_pitch_px=38)
s.rich([36, 610, 210, 104], [[{"text": "適用不明", "size_px": 25, "bold": True, "color": HEAD}], [{"text": "（対象への適用性", "size_px": 19}], [{"text": "が未確認）", "size_px": 19}]],
       color=INK, align="c", line_pitch_px=32)
# x-axis labels
s.rich([290, 752, 140, 66], [[{"text": "旧", "size_px": 25, "bold": True, "color": HEAD}], [{"text": "（古い版）", "size_px": 19}]], color=INK, align="c", line_pitch_px=32)
s.rect([800, 758, 280, 68], fill=NAVY, r=8, text="版の新しさ", size_px=28, bold=True, color="#FFFFFF")
s.rich([1440, 752, 160, 66], [[{"text": "最新", "size_px": 25, "bold": True, "color": HEAD}], [{"text": "（新しい版）", "size_px": 19}]], color=INK, align="c", line_pitch_px=32)

quads = [
    # x, y, panel fill, label fill, label, judge, dot, cand, cand_sub, message, judgment
    (268, 96, "#EAF3FC", "#1E7BE0", "旧版・参照用", "断定可", "#2E8CF0", "候補B", "（旧版・適用確認）", "旧版・参照用",
     "「この情報は旧版ですが、対象に適用可能です。\v　必要に応じて最新版も確認してください。」", "適用可、ただし最新版ではない\vことを明示"),
    (950, 96, "#DDEBF9", "#0E3A7A", "推奨候補", "断定可", "#0E2A8A", "候補A", "（最新・適用確認）", "推奨候補",
     "「最新版であり、対象に適用可能です。\v　優先的にご確認ください。」", "最新版かつ適用可と断定可能"),
    (268, 424, "#EEF0F3", "#4A5563", "保留", "断定不可", "#7A838F", "候補D", "（旧版・適用不明）", "保留",
     "「旧版であり、対象への適用性も未確認です。\v　追加の情報を確認してください。」", "最新版ではない、適用可否も不明\vのため断定不可"),
    (950, 424, "#E8F4FC", "#22A7F0", "適用未確認", "断定不可", "#2AAEF2", "候補C", "（最新・適用不明）", "適用未確認",
     "「最新版ですが、対象への適用性は未確認です。\v　適用範囲や条件を確認してください。」", "最新版であることのみ確認可能、\v適用可否は断定不可"),
]
for x, y, pf, lf, label, judge, dot, cand, csub, disp, msg, jud in quads:
    s.rect([x, y, 670, 306], fill=pf, line={"color": "#C4D6EA", "width_px": 1.2}, r=10)
    s.rect([x + 22, y + 18, 318 if len(label) > 4 else 238, 62], fill=lf, r=8, text=label, size_px=32, bold=True, color="#FFFFFF")
    s.rect([x + (360 if len(label) > 4 else 270), y + 24, 120, 48], fill="#FFFFFF", line={"color": "#C9D3DF", "width_px": 1.2}, r=6,
           text=judge, size_px=19, bold=True, color=HEAD)
    s.add(type="ellipse", box=[x + 482, y + 90, 42, 42], fill=dot, line={"color": "#FFFFFF", "width_px": 3})
    s.rich([x + 532, y + 84, 140, 56], [[{"text": cand, "size_px": 20, "bold": True, "color": HEAD}], [{"text": csub, "size_px": 13.5, "bold": True}]],
           color=INK, line_pitch_px=26)
    s.add(type="text", box=[x + 24, y + 96, 620, 200], valign="t", color=INK, bullet=True, bullet_indent_px=24, line_pitch_px=31, para_space_px=6,
          paras=[[{"text": "表示ラベル：" + disp, "size_px": 20, "bold": True}],
                 [{"text": "ユーザーに提示する文言：", "size_px": 20, "bold": True}, {"text": "\v" + msg, "size_px": 20}],
                 [{"text": "断定可否：" + jud, "size_px": 20, "bold": True}]])

warn(s, [40, 842, 1592, 84], ["版の新しさと対象への適用は別の判定です。情報が欠損している場合でも、最新版であると断定しないこと。"], sizes=(25,))
dump(s)
