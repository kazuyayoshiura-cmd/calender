import sys
sys.path.insert(0, "../../ch4")
from lib import *

HEADF = "#0E2E63"


def header(s, sub_title, pill):
    s.rect([14, 14, 136, 56], fill=HEADF, r=4, text="表 5-4", size_px=28, bold=True, color="#FFFFFF")
    s.rich([176, 8, 1000, 68], [[{"text": "方式比較の評価計画", "size_px": 40, "bold": True}, {"text": sub_title, "size_px": 26, "bold": True}]], color=HEAD)
    if pill:
        s.rect([1000, 14, 658, 60], fill="#E3F0FB", r=8, text=pill, size_px=18.5, bold=True, color=HEAD)


# ================= 4-1: comparison table
a = Slide()
header(a, "", "代表質問セットで各方式を比較し、業務での有効性と採用可否を判断する")
cols = [276, 256, 170, 170, 170] + [120] * 5
H = lambda t, **k: {"text": t, "fill": HEADF, "color": "#FFFFFF", "bold": True, "size_px": 19, "align": "c", "line_pitch_px": 26, **k}
SUBH = lambda t1, t2: {"paras": [[{"text": t1, "size_px": 19, "bold": True}], [{"text": t2, "size_px": 14.5, "bold": True}]],
                        "fill": "#E6EEF8", "color": HEAD, "align": "c", "line_pitch_px": 25}
Q = lambda t: {"text": t, "fill": "#E6EEF8", "color": HEAD, "bold": True, "size_px": 17, "align": "c", "line_pitch_px": 24}
cells = [[H("検索方式", span=[2, 1]), H("概要", span=[2, 1]), H("評価指標（主要3指標）", span=[1, 3]), None, None,
          H("評価対象（代表質問セットでの傾向）", span=[1, 5]), None, None, None, None],
         [None, None, SUBH("Top-5到達率（%）", "↑ 高いほど良い"), SUBH("根拠の正確性（%）", "↑ 高いほど良い"), SUBH("応答時間（秒）", "↓ 短いほど良い"),
          Q("①番号・\n条件一致"), Q("②略語・\n表記揺れ"), Q("③言い換え\n（意味類似）"), Q("④同名\n異義語"), Q("⑤版・適用\n条件")]]
data = [
    ("構造化のみ", "（SQL・フィルタ）", "確定キーや番号での\n厳密な一致検索", "80%", "95%", "0.5", "◎△△△◎"),
    ("全文のみ", "（BM25）", "キーワード一致による\n全文検索", "60%", "70%", "1.0", "○○△△△"),
    ("ベクトルのみ", "（意味類似）", "意味的な類似性による\nベクトル検索", "70%", "75%", "1.2", "△○◎△△"),
    ("併用", "（BM25＋\vベクトル）", "全文とベクトルの\nハイブリッド（RRF統合）", "85%", "85%", "1.5", "◎○○○○"),
    ("併用＋リランク", "（RRF＋\vReranker）", "ハイブリッド結果を\n生成AIで再ランキング", "88%", "90%", "2.5", "◎◎◎○○"),
]
for i, (m1, m2, desc, t5, acc, rt, marks) in enumerate(data):
    fill = "#FFFFFF" if i % 2 == 0 else "#F3F7FB"
    row = [{"paras": [[{"text": m1, "size_px": 21, "bold": True}], [{"text": m2, "size_px": 15.5, "bold": True}]], "color": HEAD, "align": "l",
            "fill": "#EAF3FC", "line_pitch_px": 26, "inset_px": [118, 2, 2, 2]},
           {"text": desc, "size_px": 17.5, "color": INK, "align": "l", "fill": fill, "line_pitch_px": 27, "inset_px": [16, 2, 4, 2]}]
    row += [{"text": v, "size_px": 26, "bold": True, "color": HEAD, "align": "c", "fill": fill} for v in (t5, acc, rt)]
    row += [{"text": m, "size_px": 30, "color": "#1F4E8C", "align": "c", "fill": fill} for m in marks]
    cells.append(row)
rh = [48, 92] + [126] * 5
a.add(type="table", box=[14, 90, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells,
      border={"color": "#D3DEEB", "width_px": 1.2}, name="evaluation-table")
icons = [["azure:sql-database"], ["azure:file"], ["azure:cognitive-services"], ["azure:file", "azure:cognitive-services"], ["azure:metrics"]]
y = 90 + 48 + 92
for i, ic in enumerate(icons):
    cy = y + 126 * i + 63
    if len(ic) == 1:
        a.icon(ic[0], [28, cy - 32, 64, 64])
    else:
        a.icon(ic[0], [20, cy - 22, 40, 44])
        a.text([58, cy - 14, 16, 28], "+", 20, bold=True, color=HEAD, align="c")
        a.icon(ic[1], [72, cy - 20, 40, 40])
a.text([14, 900, 1644, 30], "凡例：◎ 得意　○ 対応可能　△ 苦手（取り逃しリスクあり）", 17, color=SUB, align="r")

# ================= 4-2: targets / metrics / criteria
b = Slide()
header(b, "（評価対象・評価指標の定義・採否判断の基準）", None)


def panel(box, title):
    b.rect(box, fill="#FFFFFF", line={"color": "#C9D6E6", "width_px": 1.2}, r=6)
    b.rect([box[0], box[1], box[2], 50], fill=HEADF, r=6)
    b.rect([box[0], box[1] + 30, box[2], 20], fill=HEADF)
    b.text([box[0] + 20, box[1], box[2] - 30, 50], title, 22, bold=True, color="#FFFFFF")


# left: question set
panel([20, 92, 700, 752], "評価対象：代表質問セット（例）")
qs = [("番号・条件一致", "「部品番号 123456 のTOSを教えて」"), ("略語・表記揺れ", "「治具／治工具／ジグに関する作業指示」"), ("言い換え\v（意味類似）", "「過去に類似工程で使われた\vTOSを探したい」"),
      ("同名異義語", "「A工程のドリルについて\v（治具のドリル or 加工のドリル？）」"), ("版・適用条件", "「JP-2024-001 の最新版と\v適用機種を教えて」")]
qh = 132
b.add(type="table", box=[36, 158, 668, qh * 5], col_widths_px=[250, 418], row_heights_px=[qh] * 5,
      cells=[[{"text": k, "size_px": 20, "bold": True, "color": HEAD, "fill": "#EAF3FC", "align": "l", "inset_px": [76, 2, 4, 2], "line_pitch_px": 28},
              {"text": v, "size_px": 18, "color": INK, "fill": "#F7FAFD", "align": "l", "line_pitch_px": 28, "line_pitch": None, "inset_px": [16, 2, 8, 2]}] for k, v in qs],
      border={"color": "#FFFFFF", "width_px": 4})
for i in range(5):
    cy = 158 + qh * i + qh / 2
    b.add(type="ellipse", box=[50, cy - 22, 44, 44], fill="#1F4E8C", line=None, text=str(i + 1), size_px=22, bold=True, color="#FFFFFF")

# middle: metric definitions
panel([736, 92, 460, 752], "評価指標の定義")
mh = 220
b.add(type="table", box=[752, 158, 428, mh * 3], col_widths_px=[150, 278], row_heights_px=[mh] * 3,
      cells=[[{"text": k, "size_px": 20, "bold": True, "color": HEAD, "fill": "#EAF3FC", "align": "c"},
              {"text": v, "size_px": 18, "color": INK, "fill": "#F7FAFD", "align": "l", "line_pitch_px": 30, "inset_px": [16, 2, 10, 2]}]
             for k, v in [("Top-5\n到達率", "正解または許容回答が\v上位5件に含まれる割合\v（％）。高いほど良い。"),
                          ("根拠の\n正確性", "提示された根拠（出典・\v版・該当箇所等）が正しい\v割合（%）。高いほど良い。"),
                          ("応答時間", "質問入力から最終回答の\v表示までの時間（秒）。\v短いほど良い。")]],
      border={"color": "#FFFFFF", "width_px": 4})

# right: criteria
panel([1212, 92, 446, 752], "採否判断の基準（例）")
b.add(type="table", box=[1228, 158, 414, 300], col_widths_px=[150, 264], row_heights_px=[110, 90, 100],
      cells=[[{"text": k, "size_px": 18, "bold": True, "color": HEAD, "fill": "#EAF3FC", "align": "c", "line_pitch_px": 26},
              {"text": v, "size_px": 17.5, "color": INK, "fill": "#F7FAFD", "align": "l", "line_pitch_px": 27, "inset_px": [14, 2, 8, 2]}]
             for k, v in [("Top-5\n到達率", "80%以上（全体）\vかつ 各質問セットで\v70%以上"), ("根拠の\n正確性", "85%以上（全体）"), ("応答時間", "3秒以内（目安）")]],
      border={"color": "#FFFFFF", "width_px": 4})
b.rect([1228, 486, 220, 38], fill="#3E6FA8", r=4, text="リランクの採用判断", size_px=18, bold=True, color="#FFFFFF")
b.rect([1228, 530, 414, 298], fill="#F7FAFD", r=4)
b.add(type="text", box=[1244, 546, 392, 270], text="併用に対して Top-5到達率の改善が\v+3%未満 かつ 根拠の正確性の改善が\v+3%未満の場合、リランクは不採用とする。\n応答時間が業務要件（3秒以内）を\v超える場合も不採用とする。",
      size_px=17, color=INK, valign="t", bullet=True, line_pitch_px=28, para_space_px=14, bullet_indent_px=20)

# footer
b.rect([20, 860, 1638, 64], fill="#EEF2F7", r=6)
b.icon("azure:file", [36, 870, 40, 44])
b.rich([90, 860, 1560, 64], [[{"text": "前提：", "size_px": 19, "bold": True, "color": HEAD},
                              {"text": "評価は固定の代表質問セットで実施し、各方式を同一条件で比較する。辞書・プロンプト・パラメータ等の調整も評価対象に含め、再現性のある結果で判断する。", "size_px": 17.5}]],
       color=INK)

import json
for name, sl in (("spec_41.json", a), ("spec_42.json", b)):
    json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": sl.E}, open(name, "w"), ensure_ascii=False, indent=1)
print(len(a.E), len(b.E))
