import sys
sys.path.insert(0, "../../ch6")
from common import *

MONO = "Consolas"
s = Slide()
s.text([24, 4, 1640, 64], "表7-1　API入出力仕様（要約）", 40, bold=True, color=HEAD)

cols = [320, 454, 418, 450]
rh = [46, 180, 196, 162, 180, 104]
T0 = 70
xs = [16]
for w in cols:
    xs.append(xs[-1] + w)
H = lambda t: {"text": t, "fill": "#0E3F82", "color": "#FFFFFF", "bold": True, "size_px": 22, "align": "c"}
rows = [
    ("POST", "/interpret", "質問 → 構造化条件JSON\v（LLM＋検証・正規化ログ）",
     "自然言語の質問、コンテキスト情報 等", '{\n  "question": "部品番号Aの過去TOSを探したい",\n  "context": {"user_id": "u123", ...},\n  "options": {"domain": "TOS"}\n}',
     "構造化条件JSON（正規化後）＋ 検証結果",
     '{\n  "conditions": {\n    "part_no": "A", "target": "TOS",\n    "time_range": null, ...\n  },\n  "validation": {"status": "ok", "messages": []},\n  "normalized_query": "..."\n}',
     ["LLMで質問の意図を解釈し、検索条件を抽出", "業務用語・同義語の正規化、コード値検証", "不明・曖昧な項目は確認メッセージを返す", "このAPIで確定するのは「構造化条件」のみ", "実データの検索は行わない", "解釈・検証のログを記録（F-07）"]),
    ("POST", "/search", "条件JSON → 候補リスト\v（SQL・全文・ベクトル検索+RRF）",
     "検索条件JSON", '{\n  "conditions": {"part_no": "A", "target": "TOS"},\n  "mode": "hybrid",\n  "filters": {"model": "B737",\n              "date_from": "2020-01-01"},\n  "top_k": 20,\n  "rerank": true\n}',
     "検索候補リスト（スコア付き）",
     '{\n  "results": [\n    { "id": "TOS-2024-001", "score": 0.92,\n      "title": "治工具製作指示票",\n      "summary": "...",\n      "source_ref_id": "REF-0001" }, ...\n  ]\n}',
     ["mode：exact / similar / hybrid", "filters：各種条件（機種、期間、ステータス等）", "top_k：取得件数（例：10、20、50）", "複数手法（SQL・全文・ベクトル検索）を統合し\vRRFでランク付け、必要に応じて再ランキング", "権限・アクセス制御を適用", "このAPIで確定するのは「検索結果（候補リスト）」"]),
    ("POST", "/explain", "候補ID → evidence参照\vID付き説明",
     "候補ID、質問（任意）", '{\n  "id": "TOS-2024-001",\n  "question": "このTOSのポイントを教えて"\n}',
     "根拠付き説明（evidence参照ID付き）",
     '{\n  "id": "TOS-2024-001",\n  "explanation": "このTOSは…であり、…",\n  "evidence": [{ "source_ref_id": "REF-0001",\n    "page": 3, "chunk_id": "C-01", "quote": "..." },\n    ...]\n}',
     ["候補の内容を取得し、根拠情報を参照して説明生成", "evidenceに source_ref_id・ページ・引用箇所等を付与", "事実に基づく説明を生成（推測は抑制）", "このAPIで確定するのは「説明文と根拠の紐付け」"]),
    ("POST", "/compare", "候補2～3件の一致・相違\v（欠損を補完しない）",
     "比較対象の候補ID（2～3件）", '{\n  "ids": ["TOS-2024-001", "TOS-2023-045",\n          "TOS-2021-012"],\n  "compare_items": ["工程", "使用部品", "改訂点"]\n}',
     "比較結果（一致・相違の整理表）",
     '{\n  "comparison": [\n    { "item": "工程",\n      "TOS-2024-001": "機械加工",\n      "TOS-2023-045": "機械加工",\n      "TOS-2021-012": "手加工",\n      "note": "2021のみ異なる" }, ... ]\n}',
     ["指定した候補（2～3件）の主要項目を比較", "一致点・相違点を整理して提示", "欠損している項目は「未記載」として表示し、\v値の補完や推測は行わない", "根拠となる source_ref_id を併記", "このAPIで確定するのは「比較結果の提示」のみ"]),
    ("GET", "/source/{ref_id}", "原本参照（ドキュメント・図面等）",
     "参照ID（パスパラメータ）", "/source/REF-0001",
     "原本データ（メタ情報付き）",
     '{ "ref_id": "REF-0001", "type": "pdf",\n  "file_url": "/files/...",\n  "metadata": {"title": "...", "page": 3, ...} }',
     ["source_ref_id に対応する原本データを取得", "ファイル種別（PDF／TIFF／図面 等）に応じて返却", "アクセス権限を確認し、許可されたデータのみ返す", "このAPIで確定するのは「原本データの取得」のみ"]),
]
cells = [[H("エンドポイント"), H("入力（リクエスト）"), H("出力（レスポンス）"), H("確定処理・制約")]]
for r in rows:
    n = len(r[7])
    cells.append([
        {"text": "", "fill": "#E6F1FB"}, {"text": "", "fill": "#FFFFFF"}, {"text": "", "fill": "#FFFFFF"},
        {"text": "\n".join(r[7]), "fill": "#E6F1FB", "size_px": 15 if n >= 6 else 16, "color": INK, "align": "l", "valign": "m",
         "bullet": True, "bullet_indent_px": 16, "line_pitch_px": 22 if n >= 6 else 25, "inset_px": [14, 2, 6, 2]},
    ])
s.add(type="table", box=[16, T0, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells,
      border={"color": "#D6E1EE", "width_px": 2}, name="api-table")

y = T0 + rh[0]
for i, (meth, ep, desc, in_h, in_code, out_h, out_code, _) in enumerate(rows):
    h = rh[i + 1]
    s.rect([32, y + 12, 86, 30], fill="#1F7FE0", r=4, text=meth, size_px=17, bold=True, color="#FFFFFF")
    small = h < 110
    s.text([30, y + (42 if small else 44), 290, 36 if small else 44], ep, 31 if len(ep) < 12 else 24, bold=True, color="#0E2E63")
    s.text([32, y + (78 if small else 90), 286, h - (80 if small else 94)], desc, 14.5 if small else 16, color=HEAD, valign="t", line_pitch_px=25)
    for x, w, head, code in ((xs[1], cols[1], in_h, in_code), (xs[2], cols[2], out_h, out_code)):
        s.text([x + 14, y + 6, w - 20, 28], head, 17, bold=True, color=HEAD)
        ch = h - 46
        s.rect([x + 14, y + 38, w - 28, ch], fill="#EAF2FB", r=6)
        lines = code.count("\n") + 1
        size = 11.5 if lines > 1 else 17
        s.add(type="text", box=[x + 22, y + 42, w - 40, ch - 8], text=code.replace("\n", "\v"), size_px=size, color="#1E2A44",
              font=MONO, font_latin=MONO, valign="m" if lines <= 2 else "t", line_pitch_px=15.5)
    y += h
dump(s)
