import sys
sys.path.insert(0, "../../ch4")
from lib import *

HEADF = "#0E2E63"; RED = "#C8304A"
s = Slide()
s.rect([14, 14, 136, 56], fill=HEADF, r=4, text="表 5-2", size_px=28, bold=True, color="#FFFFFF")
s.text([176, 8, 900, 68], "単一方式の失敗パターンとハイブリッドでの補完", 40, bold=True, color=HEAD)
s.rect([1112, 14, 546, 60], fill="#E3F0FB", r=8, text="確定条件はコード、意味の拡張は検索", size_px=24, bold=True, color=HEAD)

cols = [378, 604, 662]
xs = [14]
for w in cols:
    xs.append(xs[-1] + w)
rh = [64, 200, 200, 200, 186]
ys = [90]
for h in rh:
    ys.append(ys[-1] + h)

H = lambda t1, t2: {"paras": [[{"text": t1, "size_px": 23, "bold": True}, {"text": t2, "size_px": 20, "bold": True}]], "fill": HEADF, "color": "#FFFFFF", "align": "c"}
BUL = {"bullet": True, "bullet_indent_px": 18, "size_px": 17.5, "color": INK, "align": "l", "line_pitch_px": 28, "valign": "t"}

rows = [
    ("構造化検索のみ", "（完全一致・フィルタ）", "SQL による\nコード・番号の一致検索", "azure:sql-database",
     "意味表現・略語を取り逃す", ["正式名称と異なる表現（略語・通称・旧称）で\vヒットしない", "関連する部品や工程の言い換え表現を拾えない", "人の記憶にある曖昧な表現では検索できない"],
     "全文 BM25 ＋ ベクトル検索で補完", "azure:search", ["キーワード一致（BM25）で表記揺れ・略語を拾う", "意味的に近い表現（ベクトル）で類似情報を候補に拡張", "コードでの確定検索を軸に、関連候補を幅広く提示"]),
    ("全文 BM25 のみ", "（キーワード一致）", "文書・図面テキストの\nキーワード検索", "azure:file",
     "表記揺れ・意味類似に弱い", ["同義語・表記揺れ（例：治具／治工具）でヒットしない", "キーワードが本文に無い関連情報を取り逃す", "文脈的に類似する内容（類似工程・類似事例）を拾えない"],
     "ベクトル検索で補完", "azure:cognitive-services", ["意味的な類似性に基づき、関連文書や類似事例を取得", "キーワードが異なる文書も候補に含める", "BM25 とベクトルの結果を RRF で統合し、網羅性を向上"]),
    ("ベクトル検索のみ", "（意味類似検索）", "文書・図面・属性の\nベクトル類似検索", "azure:cognitive-services",
     "確定キー・版／適用条件を保証できない", ["部品番号・工程番号などの厳密な一致が不得意", "最新版のみ、特定機種のみ等の版／適用条件を\v保証できない", "意味的に近いが、別の部品・旧版の情報を返すリスク"],
     "構造化検索（SQL）の必須条件フィルタで補完", "azure:sql-database", ["部品番号・工程番号・文書番号などで対象を厳密に絞り込み", "版・適用機種・有効期間などの業務条件をフィルタ", "そのうえでベクトル検索により、関連候補を拡張"]),
    ("LLM 単独", "（生成のみ・検索なし）", "事前知識に基づく\n生成回答", "azure:azure-openai",
     "根拠なき断定・再現不能", ["存在しない情報の生成（ハルシネーション）", "出典・根拠が不明で、業務で使えない", "同じ質問でも回答が変わり、再現性がない"],
     "検索結果＋業務 API の決定的処理で補完", "azure:sql-database", ["検索で取得した根拠情報をコンテキストに生成", "確定部分は DB／業務 API での決定的な取得・検証を実施", "回答には出典・文書 ID・版・適用条件を付与し、再現性を確保"]),
]
cells = [[H("単一方式", ""), H("起きる失敗", "（取り逃しの典型例）"), H("ハイブリッドでの補完", "（組み合わせによる解決）")]]
for r in rows:
    cells.append([{"text": "", "fill": "#EAF3FC"},
                  {**BUL, "text": "\n".join(r[5]), "fill": "#FFFFFF", "inset_px": [34, 64, 40, 4]},
                  {**BUL, "text": "\n".join(r[8]), "fill": "#EAF3FC", "inset_px": [50, 86, 8, 4]}])
s.add(type="table", box=[14, ys[0], sum(cols), ys[-1] - ys[0]], col_widths_px=cols, row_heights_px=rh, cells=cells,
      border={"color": "#FFFFFF", "width_px": 4}, name="failure-table")

for i, (t1, t2, desc, ic, fail, _, fix, fic, _) in enumerate(rows):
    top, bot = ys[i + 1], ys[i + 2]
    # col 1
    s.icon(ic, [34, top + 16, 66, 66])
    s.rich([120, top + 14, 260, 72], [[{"text": t1, "size_px": 24, "bold": True}], [{"text": t2, "size_px": 20, "bold": True}]], color=HEAD, line_pitch_px=34)
    s.rect([48, top + 100, 312, bot - top - 118], fill="#E6EAF0", r=8, text=desc, size_px=18, color=INK, line_pitch_px=28)
    # col 2 heading
    s.add(type="ellipse", box=[xs[1] + 24, top + 14, 44, 44], fill=RED, line=None, text="✕", size_px=24, bold=True, color="#FFFFFF")
    s.text([xs[1] + 84, top + 12, 500, 48], fail, 23, bold=True, color=HEAD)
    # arrow between columns
    s.add(type="chevron", box=[xs[2] - 32, (top + bot) / 2 - 30, 26, 60], point_px=26, fill="#9AA9BD", line=None)
    # col 3 heading
    s.icon(fic, [xs[2] + 46, top + 18, 58, 58])
    s.text([xs[2] + 120, top + 20, 530, 52], fix, 23, bold=True, color=HEAD)
s.dump()
