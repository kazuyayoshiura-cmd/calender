import sys
sys.path.insert(0, "../../ch6")
from common import *

MONO = "Consolas"
s = Slide()
s.text([24, 4, 1640, 62], "表7-4　検索候補の共通データ構造（API間で受け渡す共通フォーマット）", 38, bold=True, color=HEAD)
s.text([24, 70, 1640, 60], "検索・版判定・説明生成の各APIで共通して扱う「検索候補（1件）」のデータ構造を定義する。構造化・全文・ベクトルなど異なる検索方式の結果を統一フォーマットで扱い、\n以降の版・適用判定、根拠提示、生成に利用する。",
       17.5, color=HEAD, line_pitch_px=28)

cols = [54, 176, 130, 60, 372, 350]
rh = [40, 52, 38, 36, 36, 54, 54, 34, 56, 38, 54, 76, 52, 54]
T0 = 142
H = lambda t: {"text": t, "fill": "#0E3F82", "color": "#FFFFFF", "bold": True, "size_px": 18, "align": "c"}
rows = [
    ("candidate_id", "string", "○", "検索候補を一意に識別するID\v（検索方式・データソース・元ID等を含む）", "例：DOC-12345、TOS-9876-10"),
    ("data_source", "string", "○", "データソース種別", "N-PLUS / TOS / 共有文書"),
    ("source_type", "string", "○", "データの種類", "構造化 / 文書 / その他"),
    ("title", "string", "○", "候補のタイトル（文書名・工程名等）", "例：WPS W-55 Rev.C、作業工程 10"),
    ("matched_conditions", "object", "○", "検索時にマッチした条件\v（質問から抽出・正規化した条件との対応）", '{ "部品番号": "A123", "工程番号": "10", … }'),
    ("similarity", "number", "○", "検索スコア（0～1）\v（ベクトル類似度・RRF後の統合スコア等）", "0.0 ～ 1.0（例：0.87）"),
    ("version_status", "string", "○", "版の状態", "latest / old / draft / unknown"),
    ("applicability", "string", "○", "適用判定の結果", "applicable / not_applicable /\vunverified / partial"),
    ("unverified_items", "array<string>", "△", "適用判定で未確認・不明な項目", '["号機", "機種", "発効日"]'),
    ("source_ref", "object", "○", "元データへの参照情報", '{ "table": "WPS", "id": "W-55",\v  "file_path": "\\\\...", "url": "...", "page": 12 }'),
    ("evidence", "array<object>", "○", "回答の根拠として利用する箇所の一覧\v（本文・表・項番・ページ等）",
     '[ { "type": "text", "page": 12, "section": "3.2",\v    "text": "..." }, { "type": "table", "page": 15,\v    "row": 3, "col": 2, "text": "..." } ]'),
    ("excerpt", "string", "△", "検索時にマッチした本文の抜粋\v（ハイライト表示用）", "例：\"機械加工前に…\""),
    ("metadata", "object", "△", "その他のメタデータ（更新日・ファイル種別・\vREV 等、表示に必要な情報）", '{ "rev": "C", "effective_date": "2025-06-01",\v  "file_type": "PDF", "更新日": "2025-06-10" }'),
]
cells = [[H(""), H("項目名"), H("型"), H("必須"), H("説明"), H("主な設定値・形式例")]]
for i, (name, typ, req, desc, ex) in enumerate(rows):
    f = "#F3F7FB" if i % 2 == 0 else "#FFFFFF"
    code_like = ex.startswith("{") or ex.startswith("[")
    cells.append([
        {"text": str(i + 1), "size_px": 17, "bold": True, "color": HEAD, "fill": "#E6F1FB", "align": "c"},
        {"text": name, "size_px": 18 if len(name) < 15 else (16 if len(name) < 17 else 14), "bold": True, "color": "#1356B0", "fill": "#E6F1FB", "align": "l", "inset_px": [12, 2, 2, 2]},
        {"text": typ, "size_px": 15.5, "color": INK, "fill": f, "align": "l", "inset_px": [12, 2, 2, 2]},
        {"text": req, "size_px": 17, "color": INK, "fill": f, "align": "c"},
        {"text": desc, "size_px": 15, "color": INK, "fill": f, "align": "l", "line_pitch_px": 22, "inset_px": [12, 2, 4, 2]},
        {"text": ex, "size_px": 14 if code_like else 15, "color": INK, "fill": f, "align": "l", "line_pitch_px": 21, "inset_px": [12, 2, 4, 2]},
    ])
s.add(type="table", box=[22, T0, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells, border={"color": "#FFFFFF", "width_px": 2}, name="schema-table")

# JSON panel
JX, JW = 1178, 474
s.rect([JX, T0, JW, 690], fill="#EAF3FC", r=6)
s.rect([JX, T0, JW, 40], fill="#0E3F82", r=6, text="検索候補のJSON例", size_px=18, bold=True, color="#FFFFFF")
KEY = "#1F3A6E"; STR = "#C8302C"; NUM = "#1E7B4E"
json_lines = [
    ("{", None), ('  "candidate_id": ', '"DOC-12345",'), ('  "data_source": ', '"共有文書",'), ('  "source_type": ', '"文書",'), ('  "title": ', '"WPS W-55 Rev.C",'),
    ('  "matched_conditions": {', None), ('    "部品番号": ', '"A123",'), ('    "工程番号": ', '"10",'), ('    "検索語": ', '"WPS"'), ("  },", None),
    ('  "similarity": ', "0.87,", NUM), ('  "version_status": ', '"latest",'), ('  "applicability": ', '"applicable",'), ('  "unverified_items": [],', None),
    ('  "source_ref": {', None), ('    "file_path": ', '"\\\\share\\manual\\WPS_W-55.pdf",'), ('    "page": ', "12,", NUM), ('    "doc_id": ', '"WPS_W-55",'), ('    "rev": ', '"C"'), ("  },", None),
    ('  "evidence": [', None), ("    {", None), ('      "type": ', '"text",'), ('      "page": ', "12,", NUM), ('      "section": ', '"3.2",'), ('      "text": ', '"機械加工前に…"'), ("    },", None),
    ("    {", None), ('      "type": ', '"table",'), ('      "page": ', "15,", NUM), ('      "row": ', "3,", NUM), ('      "col": ', "2,", NUM), ('      "text": ', '"…"'), ("    }", None), ("  ],", None),
    ('  "excerpt": ', '"機械加工前に治具を確認する…",'), ('  "metadata": {', None), ('    "rev": ', '"C",'), ('    "effective_date": ', '"2025-06-01",'), ('    "file_type": ', '"PDF",'),
    ('    "更新日": ', '"2025-06-10"'), ("  }", None), ("}", None),
]
paras = []
for ln in json_lines:
    k, v = ln[0], ln[1]
    runs = [{"text": k, "color": KEY}]
    if v:
        runs.append({"text": v, "color": ln[2] if len(ln) > 2 else STR})
    paras.append(runs)
s.add(type="text", box=[JX + 16, T0 + 46, JW - 24, 640], paras=paras, size_px=11.5, font=MONO, font_latin=MONO, valign="t", line_pitch_px=14.6)

# bottom boxes
for x, w, ic, title, lines, sz in [
        (22, 978, "azure:app-configuration", "設計方針", ["構造化検索・全文検索・ベクトル検索 など、すべての検索方式の結果を同一フォーマットに変換する。",
                                                    "版・適用判定（VA）で付与する version_status / applicability を含める。",
                                                    "evidence により回答の根拠箇所（本文・表・項番・ページ等）を明示し、生成文はこの情報に基づいて作成する。",
                                                    "API 間（/search → /version-check → /evidence → /explain）で共通して利用する。"], 14),
        (1008, 644, "azure:file", "補足", ["必須：全ケースで必要な項目、△：必要に応じて設定する項目。", "unverified_items がある場合、生成時に「適用未確認」と明示する。",
                                            "metadata は表示要件に応じて拡張可能（種別、更新日等）。", "実際の実装では、キー名や値は API 仕様書で詳細に定義する。"], 13)]:
    s.rect([x, 840, w, 92], fill="#F3F7FB", r=6)
    s.rect([x, 840, 150, 92], fill="#E6F1FB", r=6)
    s.icon(ic, [x + 12, 862, 48, 48])
    s.text([x + 66, 840, 84, 92], title, 17, bold=True, color=HEAD)
    s.add(type="text", box=[x + 162, 844, w - 170, 84], text="\n".join(lines), size_px=sz, color=INK, valign="m", bullet=True, bullet_indent_px=13, line_pitch_px=20.5)
dump(s)
