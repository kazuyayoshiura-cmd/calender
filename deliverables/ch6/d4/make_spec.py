import sys
sys.path.insert(0, "..")
from common import *

s = Slide()
header(s, "表6-2", "版・適用に関する不足／矛盾時の表示方針")

cols = [316, 310, 298, 724]
rh = [84, 112, 130, 130, 124, 132]
T0 = 80
H = lambda t1, t2=None: {"paras": [[{"text": t1, "size_px": 23, "bold": True}]] + ([[{"text": t2, "size_px": 18, "bold": True}]] if t2 else []),
                          "fill": "#0E3F82", "color": "#FFFFFF", "align": "c", "line_pitch_px": 32}
BADGE = {"blue": ("#DCEBFA", "#1F5FB8"), "red": ("#FCE1E1", "#D42A2A"), "yellow": ("#FDF0CF", "#5A4300"), "gray": ("#E3E7EC", "#3A4552"), "pink": ("#FCE1E1", "#C0303A")}
rows = [
    ("有効・適用範囲内", "（通常）", NAVY, "latest", "（最新版）", "NEW", "check", "applicable", "（適用可能）",
     "通常表示", "blue", ["最新版であり、対象に適用可能です。", "関連情報（根拠・適用範囲・発効日等）を表示します。"]),
    ("有効だが", "適用範囲外", "#2AA0EE", "latest", "（最新版）", "NEW", "warn", "not applicable", "（適用不可）",
     "対象外の警告", "red", ["最新版ですが、対象への適用範囲外です。", "適用範囲（FROM－THRU 等）を表示し、対象外であることを\v明示します。"]),
    ("旧版だが", "適用範囲内", "#2AA0EE", "old", "（旧版）", "OLD", "check", "applicable", "（適用可能）",
     "旧版の警告", "yellow", ["旧版ですが、対象に適用可能です。", "最新版の有無を確認するよう案内し、必要に応じて最新版を\v提示します。"]),
    ("版情報が未登録", "（版列の NULL 等）", "#5B6573", "unknown", "（版不明）", "?", "question", "unverified", "（適用未確認）",
     "版不明・適用未確認", "gray", ["版情報が不明のため、最新版とは断定できません。", "対象への適用性も未確認です。\v追加の情報を確認してください。"]),
    ("同一IDで", "内容に矛盾あり", "#2AA0EE", "conflict", "（矛盾あり）", "!", "question", "unverified", "（適用未確認）",
     "両方の情報を提示・矛盾箇所を明示", "pink", ["同一文書番号に複数の異なる情報が存在します。", "確認できた情報を両方提示し、矛盾箇所を明示します。"]),
]
cells = [[H("状態"), H("版情報", "（版の新しさ）"), H("適用可否", "（対象への適用）"), H("表示・回答方針", "（ユーザーへの表示文言・対応）")]]
for i, r in enumerate(rows):
    cells.append([
        {"paras": [[{"text": r[0]}], [{"text": r[1]}]], "size_px": 22, "bold": True, "color": HEAD, "fill": "#E6F1FB", "align": "l",
         "line_pitch_px": 34, "inset_px": [84, 2, 4, 2]},
        {"paras": [[{"text": r[3], "size_px": 22, "bold": True}], [{"text": r[4], "size_px": 18}]], "color": HEAD, "fill": "#FFFFFF", "align": "l",
         "line_pitch_px": 32, "inset_px": [150, 2, 4, 2]},
        {"paras": [[{"text": r[7], "size_px": 22 if len(r[7]) < 12 else 20, "bold": True}], [{"text": r[8], "size_px": 18}]], "color": HEAD, "fill": "#FFFFFF",
         "align": "l", "line_pitch_px": 32, "inset_px": [110, 2, 2, 2]},
        {"text": "", "fill": "#FFFFFF"},
    ])
s.add(type="table", box=[14, T0, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells,
      border={"color": "#DCE4EE", "width_px": 1.5}, name="policy-table")

xs = [14]
for w in cols:
    xs.append(xs[-1] + w)
y = T0 + rh[0]
for i, r in enumerate(rows):
    h = rh[i + 1]
    cy = y + h / 2
    num(s, xs[0] + 42, cy, i + 1, fill=r[2], d=46, size=24)
    # version icon: Azure file + native badge
    s.icon("azure:file", [xs[1] + 36, cy - 38, 66, 76])
    tag = r[5]
    if tag in ("NEW", "OLD"):
        s.rect([xs[1] + 76, cy + 6, 52, 30], fill="#1F7FE0" if tag == "NEW" else "#6B7684", r=4, text=tag, size_px=15, bold=True, color="#FFFFFF")
    else:
        s.add(type="ellipse", box=[xs[1] + 84, cy + 2, 38, 38], fill="#7A838F" if tag == "?" else "#E02020", line={"color": "#FFFFFF", "width_px": 2},
              text=tag, size_px=20, bold=True, color="#FFFFFF")
    # applicability icon
    ic = {"check": ("material:check_circle-fill", "#1F7FE0"), "warn": ("material:warning-fill", "#E02020"), "question": ("material:help-fill", "#7A838F")}[r[6]]
    s.icon(ic[0], [xs[2] + 30, cy - 32, 64, 64], ic[1])
    # policy badge + bullets
    bf, bc = BADGE[r[10]]
    wide = len(r[9]) > 10
    bw = 420 if wide else (190 if len(r[9]) > 6 else 164)
    if wide:
        s.rect([xs[3] + 18, y + 12, bw, 40], fill=bf, r=6, text=r[9], size_px=20, bold=True, color=bc)
        s.add(type="text", box=[xs[3] + 18, y + 58, 700, h - 64], text="\n".join(r[11]), size_px=16.5, color=INK, valign="t",
              bullet=True, bullet_indent_px=18, line_pitch_px=26)
    else:
        s.rect([xs[3] + 18, cy - 24, bw, 48], fill=bf, r=6, text=r[9], size_px=20 if len(r[9]) < 7 else 17.5, bold=True, color=bc)
        s.add(type="text", box=[xs[3] + bw + 34, y + 8, 724 - bw - 44, h - 16], text="\n".join(r[11]), size_px=16.5, color=INK,
              valign="m", bullet=True, bullet_indent_px=18, line_pitch_px=26)
    y += h

warn(s, [14, 822, 1648, 104], ["情報が不足している場合や矛盾がある場合でも、最新版である、または対象に適用可能であると断定しないこと。",
                               "版の新しさと対象への適用は別の判定です。不明な場合は「版不明」「適用未確認」として表示し、必要に応じて追加情報の確認を促します。"],
     sizes=(22, 18))
dump(s)
