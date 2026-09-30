import sys
sys.path.insert(0, "../../ch4")
from lib import *

HEADF = "#0E2E63"
s = Slide()
s.rect([12, 8, 1648, 76], fill="#E3F0FB", r=10)
s.text([12, 8, 1648, 76], "確定条件はコードで絞り、意味検索は候補拡張に限定", 38, bold=True, color=HEAD, align="c")

cols = [290, 302, 291, 417, 352]
xs = [10]
for w in cols:
    xs.append(xs[-1] + w)
rh = [72, 198, 214, 204, 150]
ys = [94]
for h in rh:
    ys.append(ys[-1] + h)

H = lambda t: {"text": t, "fill": HEADF, "color": "#FFFFFF", "bold": True, "size_px": 22, "align": "c", "line_pitch_px": 30}
BUL = {"bullet": True, "bullet_indent_px": 20, "size_px": 18.5, "color": INK, "align": "l", "line_pitch_px": 28, "inset_px": [18, 4, 8, 4]}
RISK = {**BUL, "size_px": 17.5, "line_pitch_px": 27, "fill": "#EEF1F5", "bullet_indent_px": 18}


def risk(items):
    return {**RISK, "paras": [[{"text": h + "：", "bold": True}, {"text": "\v" + t}] for h, t in items]}


rows = [
    ("部品番号・工程番号・\v文書番号など\v確定キーのみ", ["部品番号 123456 の\v図面を検索", "工程番号 10-20 の\v作業手順を表示", "文書番号 JP-2024-001\vを参照"],
     ("構造化検索", "（完全一致・フィルタ）"), ["確定キーは一意性が高く、\v構造化検索で正確かつ高速に\v目的のデータへ到達できる", "不要な類似候補を除外し、\v誤った情報の混入を防ぐ"],
     [("ベクトル検索のみ", "表記ゆれや類似表現により\v別の部品・文書を返す可能性"), ("全文検索のみ", "コード項目の一致精度が低く、\v該当データを取り逃す可能性")]),
    ("確定キー＋\v自然言語", ["部品番号 123456 の\v後継品を教えて", "工程番号 10-20 の\v不具合事例を調べて"],
     ("構造化で絞って", "全文・ベクトル"), ["確定キーで対象範囲を絞り込み、\vその中から自然言語の意図に合う\v情報を全文・ベクトルで検索する", "ノイズを抑えつつ、関連情報の\v取りこぼしを防げる"],
     [("構造化検索のみ", "確定キーだけでは関連情報\v（関連文書・類似事例）を\v取り逃す可能性"), ("ベクトル検索のみ", "対象範囲が広くノイズが多く、\v目的の情報を見落とす可能性")]),
    ("自然言語のみ", ["この部品の類似事例を\v教えて", "加工方法の注意点を調べて", "この不具合の原因は？"],
     ("全文 BM25＋", "ベクトルのハイブリッド"), ["キーワードの一致（全文 BM25）\vと意味の類似（ベクトル）を\v組み合わせ、用語の揺れや\v類似表現にも対応できる", "網羅性を高め、関連する候補を\v幅広く提示できる"],
     [("全文検索のみ", "同義語・表記ゆれにより\v関連情報を取り逃す可能性"), ("ベクトル検索のみ", "固有名詞や専門用語の一致に\v弱く、重要な情報を見落とす可能性")]),
    ("意図不明／\v同名異義語", None,
     ("追加確認", "（Dify質問分岐）"), ["意図が不明確な場合や同名異義語\vが存在する場合は、追加質問により\v対象を特定してから検索を実行する", "誤った解釈による検索を防ぎ、\v精度の高い結果を提示できる"],
     [("単一検索方式のみ", "誤った対象で検索され、無関係な\v結果を提示する可能性が高く、\v正しい情報を取り逃す")]),
]
cells = [[H("質問種類"), H("質問例"), H("採用する方式"), H("なぜこの方式を採用するのか（理由）"), H("単一方式で起きる\n取り逃しリスク")]]
for i, (kind, ex, (m1, m2), why, rk) in enumerate(rows):
    if ex is None:
        excell = {**BUL, "paras": [[{"text": "この部品について教えて"}, {"text": "\v（対象の部品が不明）", "size_px": 14, "color": SUB}],
                                   [{"text": "“フランジ”の図面を探して"}, {"text": "\v（同名異義語が複数存在）", "size_px": 14, "color": SUB}]]}
    else:
        excell = {**BUL, "text": "\n".join(ex)}
    cells.append([
        {"text": kind, "size_px": 20.5, "bold": True, "color": HEAD, "align": "l", "valign": "t", "line_pitch_px": 31, "fill": "#EAF3FC", "inset_px": [80, 26, 4, 4]},
        excell,
        {"paras": [[{"text": m1}], [{"text": m2}]], "size_px": 21, "bold": True, "color": HEAD, "align": "c", "valign": "b", "fill": "#E3F0FB",
         "line_pitch_px": 30, "inset_px": [4, 4, 4, 22 if i < 3 else 14]},
        {**BUL, "text": "\n".join(why), "size_px": 17.5, "line_pitch_px": 27},
        risk(rk),
    ])
s.add(type="table", box=[10, ys[0], sum(cols), ys[-1] - ys[0]], col_widths_px=cols, row_heights_px=rh, cells=cells,
      border={"color": "#FFFFFF", "width_px": 3}, name="method-table")

icons = [[("azure:sql-database", 64)], [("azure:sql-database", 58), ("+", 0), ("azure:search", 52)], [("azure:file", 58), ("+", 0), ("azure:cognitive-services", 62)],
         [("azure:bot-services", 62)]]
for i, ic in enumerate(icons):
    top = ys[i + 1]
    # number badge
    cy = top + 42
    s.add(type="ellipse", box=[26, cy - 24, 48, 48], fill="#1F4E8C", line=None, text=str(i + 1), size_px=24, bold=True, color="#FFFFFF")
    total = sum(sz for _, sz in ic) + 26 * sum(1 for r, _ in ic if r == "+")
    x = xs[2] + (cols[2] - total) / 2
    iy = top + (18 if i < 3 else 10)
    for ref, sz in ic:
        if ref == "+":
            s.text([x, iy + 16, 26, 30], "+", 24, bold=True, color=HEAD, align="c")
            x += 26
        else:
            s.icon(ref, [x, iy + (66 - sz) / 2, sz, sz])
            x += sz
s.dump()
