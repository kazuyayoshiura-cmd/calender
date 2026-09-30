import sys
sys.path.insert(0, "../../ch6")
from common import *

NV = "#0E3F82"
s = Slide()
s.text([24, 8, 1640, 66], "図7-1　検索APIのエンドポイント構成とDifyからの呼出関係", 38, bold=True, color=HEAD)

# ---- user
s.icon("azure:users", [18, 318, 60, 64])
s.text([6, 386, 84, 30], "利用者", 19, bold=True, color=HEAD, align="c")
s.arrow([[86, 348], [166, 348]], w=2.5)
s.text([80, 276, 90, 52], "質問\n（自然言語）", 16, color=HEAD, align="c", line_pitch_px=24)
s.arrow([[166, 444], [76, 444]], w=2.5)
s.text([72, 462, 96, 52], "回答\n（根拠付き）", 16, color=HEAD, align="c", line_pitch_px=24)

# ---- Dify
s.rect([172, 94, 298, 658], fill="#E6F1FB", r=10)
s.rect([196, 114, 250, 78], fill="#1356B0", r=6, paras=[[{"text": "Dify ワークフロー", "size_px": 23, "bold": True}], [{"text": "（表示・分岐のみ）", "size_px": 18}]],
       color="#FFFFFF", line_pitch_px=32)
for y, ic, t1, t2 in [(222, "azure:language", "入力", "（質問）"), (350, "azure:workflow", "ワークフロー", "（条件分岐・制御）"), (496, "azure:file", "結果の表示", "（回答・根拠・候補）")]:
    s.rect([196, y, 254, 92], fill="#FFFFFF", r=6)
    s.icon(ic, [210, y + 20, 52, 52])
    s.rich([276, y + 10, 172, 72], [[{"text": t1, "size_px": 19, "bold": True}], [{"text": t2, "size_px": 16}]], color=INK, line_pitch_px=28)
s.arrow([[323, 316], [323, 348]], w=2.5)
s.arrow([[323, 444], [323, 494]], w=2.5)
s.rect([184, 624, 274, 118], fill="#E3E7EC", r=6)
s.text([196, 632, 256, 104], "Difyは表示・分岐のみを担当し、\n検索・判定・生成・記録等の\n確定処理はすべてAPI側で実施", 16, color=INK, line_pitch_px=30)

# ---- Dify <-> API
s.text([476, 268, 98, 56], "API呼出\n（HTTP）", 17, color=HEAD, align="c", line_pitch_px=26)
s.arrow([[474, 338], [572, 338]], w=3.5)
s.arrow([[572, 444], [474, 444]], w=2.5, dash="dash")
s.text([470, 456, 104, 52], "検索結果\n（構造化JSON）", 15, color=HEAD, align="c", line_pitch_px=24)

# ---- search API
s.rect([578, 90, 606, 704], fill="#FFFFFF", line={"color": "#0E2E63", "width_px": 3}, r=6)
s.rect([578, 90, 606, 86], fill="#0E2E63", r=6)
s.icon("azure:app-services", [712, 100, 40, 40])
s.text([760, 98, 360, 44], "検索API（FastAPI）", 27, bold=True, color="#FFFFFF")
s.text([578, 140, 606, 32], "（検索・判定・生成・記録の確定処理）", 19, color="#FFFFFF", align="c")
eps = [("/interpret", "azure:form-recognizers", "LLM抽出 ＋ コード検証", ["質問の意図解釈", "検索条件の抽出", "コード／用語の正規化・検証"]),
       ("/search", "azure:search", "SQL・全文・ベクトル検索 ＋ RRF", ["RDB（SQL検索）", "ファイル（全文検索・ベクトル検索）", "RRFによる統合ランキング"]),
       ("/version-check", "azure:versions", "版・適用判定", ["版の新旧判定", "適用範囲の確認", "旧版・適用外の警告"]),
       ("/evidence", "azure:private-link", "source_ref 組立", ["根拠情報の整理", "根拠IDの採番", "出典メタデータの付与"]),
       ("/explain", "azure:azure-openai", "根拠付き説明生成", ["検索結果に基づく回答生成", "根拠IDの引用", "必要に応じた追質問の生成"]),
       ("/log", "azure:activity-log", "F-07 記録", ["質問・検索条件・結果の記録", "利用者・時刻・処理内容の保存", "監査・再現に必要な情報の保持"])]
EY = [186 + i * 102 for i in range(6)]
for (ep, ic, head, bl), y in zip(eps, EY):
    s.rect([594, y, 574, 92], fill="#FFFFFF", line={"color": "#9DBBE0", "width_px": 1.2}, r=4)
    s.rect([594, y, 160, 92], fill="#DCEBFA", r=4)
    s.text([600, y, 150, 92], ep, 23 if len(ep) < 11 else 17, bold=True, color="#1356B0", align="c")
    s.icon(ic, [766, y + 22, 48, 48])
    s.text([836, y + 4, 330, 26], head, 16.5, bold=True, color=HEAD)
    s.add(type="text", box=[836, y + 30, 330, 60], text="\n".join(bl), size_px=13.5, color=INK, valign="t", bullet=True, bullet_indent_px=14, line_pitch_px=19)

# ---- data sources
s.rect([1230, 94, 428, 692], fill="#E6F1FB", r=10)
s.text([1230, 100, 428, 50], "データソース・AIリソース", 27, bold=True, color=HEAD, align="c")
srcs = [("azure:azure-database-postgresql-server", "PostgreSQL", "（構造化データ）", ["工程設計データ\v（N-PLUS／TOS 等）", "マスタ・コード情報"]),
        ("azure:cognitive-search", "OpenSearch", "（非構造化データ）", ["社内ドキュメント\v（ファイルサーバー等）", "全文検索・ベクトル検索"]),
        ("azure:azure-openai", "LLM", "（推論・生成）", ["質問解釈", "回答生成", "コード検証支援"]),
        ("azure:cognitive-services", "Embedding", "（ベクトル化）", ["文書のベクトル化", "類似検索"]),
        ("azure:metrics", "Reranker", "（再ランキング）", ["検索結果の再順位付け", "関連度スコアの最適化"])]
SY = [158, 282, 410, 540, 666]
for (ic, t1, t2, bl), y in zip(srcs, SY):
    h = 102 if y != 540 else 96
    s.rect([1246, y, 398, h], fill="#FFFFFF", line={"color": "#C4D6EA", "width_px": 1.2}, r=6)
    s.icon(ic, [1258, y + (h - 54) / 2, 54, 54])
    s.rich([1322, y + 12, 140, h - 24], [[{"text": t1, "size_px": 18 if len(t1) > 8 else 19, "bold": True}], [{"text": t2, "size_px": 14}]], color=HEAD, line_pitch_px=28)
    s.add(type="text", box=[1466, y + 8, 176, h - 16], text="\n".join(bl), size_px=13.5, color=INK, valign="m", bullet=True, bullet_indent_px=14, line_pitch_px=22)
    cy = y + h / 2
    s.arrow([[1188, cy], [1242, cy]], w=2.5, head="both")

# ---- bottom: traceability
s.rect([24, 812, 1624, 118], fill="#E6EDF5", r=8)
s.rect([42, 826, 302, 90], fill="#0E3F82", r=6, text="根拠IDとログの横串管理\n（トレーサビリティ）", size_px=21, bold=True, color="#FFFFFF", line_pitch_px=34)
bots = [(384, 390, "azure:file", "検索結果", "（候補リスト）", ["根拠ID（source_ref_id）", "出典情報・スコア・版・適用"]),
        (836, 418, "azure:private-link", "根拠ID", "（source_ref_id）", ["/evidence で採番", "各エンドポイントで共通利用", "回答・ログに引用"]),
        (1310, 320, "azure:log-analytics-workspaces", "利用ログ（F-07）", None, ["/log で記録", "質問・検索条件・結果", "根拠ID・時刻・利用者 等"])]
for x, w, ic, t1, t2, bl in bots:
    s.rect([x, 828, w, 88], fill="#FFFFFF", line={"color": "#C4D6EA", "width_px": 1.2}, r=6)
    s.icon(ic, [x + 16, 846, 50, 50])
    if t2:
        s.rich([x + 72, 836, 132, 72], [[{"text": t1, "size_px": 18, "bold": True}], [{"text": t2, "size_px": 13}]], color=HEAD, line_pitch_px=28)
        s.add(type="text", box=[x + 206, 834, w - 208, 78], text="\n".join(bl), size_px=12.5, color=INK, valign="m", bullet=True, bullet_indent_px=13, line_pitch_px=21)
    else:
        s.text([x + 76, 832, w - 80, 26], t1, 18, bold=True, color=HEAD)
        s.add(type="text", box=[x + 80, 856, w - 84, 60], text="\n".join(bl), size_px=13, color=INK, valign="t", bullet=True, bullet_indent_px=13, line_pitch_px=19)
s.arrow([[774, 872], [836, 872]], w=2.5)
s.arrow([[1254, 872], [1310, 872]], w=2.5)
# API -> bottom
s.arrow([[662, 796], [662, 828]], w=2.5)
s.arrow([[938, 796], [938, 828]], w=2.5, head="both")
s.arrow([[1126, 796], [1126, 806], [1444, 806], [1444, 828]], w=2.5)
dump(s)
