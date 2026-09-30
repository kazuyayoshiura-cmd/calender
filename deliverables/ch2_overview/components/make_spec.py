import json
INK = "#0B2350"; SUB = "#2A3F66"; ICON = "#0E3A7A"
ys = [58, 101, 182, 262, 334, 435, 501, 568, 647, 727, 801, 862, 935]
rh = [b - a for a, b in zip(ys, ys[1:])]
cols = [255, 392, 578, 415]

rows = [
    ("Webブラウザ", "（チャットUI）", ["生産技術部員が自然言語や確定キーで質問", "回答結果（テーブル・要約・関連文書・リンク）を閲覧", "認証後、社内ネットワークからアクセス"], ["Edge / Chrome 等", "（社内クライアントPCのWebブラウザ）"]),
    ("Dify CE", "（チャットUI／ワークフロー）", ["チャットUIの提供", "ワークフローDSLによる処理フローの定義（分岐・文言・表示項目）", "検索APIをOpenAPIで呼び出し、結果を表示"], ["Dify Community Edition", "（Docker）"]),
    ("DifyのDSL・設定管理", "（Git）", ["ワークフローのテンプレート管理・バージョン管理", "変更履歴・差分・レビュー・ロールバック"], ["Git（社内Gitサーバ）", "Dify Export/Import（DSL YAML）"]),
    ("検索API", "（FastAPI）", ["質問解釈（LLMによる抽出＋コード検証）", "用語辞書・正規化・ルーティング", "構造化検索（SQL）・全文検索（BM25）・ベクトル検索", "RRFによる結果統合・必須条件フィルタ・版・適用判定・根拠アセンブリ"], ["FastAPI（Docker）", "Python"]),
    ("用語辞書・正規化辞書", "（ドメイン知識）", ["社内用語・略語・部品番号・工程名等の正規化", "検索クエリの拡張・同義語処理"], ["PostgreSQL（辞書テーブル）", "（または設定ファイル）"]),
    ("PostgreSQL", "（中間DB）", ["N-PLUSの構造化データ（TOS検索単位・文書メタ・版・適用情報）", "用語辞書・正規化辞書・ログ・評価データ等の格納"], ["PostgreSQL 16", "（Docker）"]),
    ("OpenSearch", "（全文＋ベクトル検索）", ["共有文書・技術資料の全文検索（BM25）", "文書チャンクのベクトル検索（Embedding）", "検索インデックス・メタデータの管理"], ["OpenSearch 2.x", "（Docker）"]),
    ("文書抽出・チャンク", "（取込バッチ）", ["Word／Excel／PDFから本文・表を抽出", "見出し付きチャンクに分割・メタデータ付与", "N-PLUSのCSV（12表）をJOIN・コード変換・文脈化して取込"], ["Docling / unstructured 等", "Python（バッチ処理）"]),
    ("LLM／Embedding／Reranker", "（推論モデル）", ["LLM：質問解釈・根拠付き説明生成", "Embedding：文書のベクトル化", "Reranker：検索結果の再ランキング（任意）"], ["vLLM（aarch64）／llama.cpp", "日本製・オープンモデル 等", "（Docker）"]),
    ("NVIDIA DGX Spark", "（実行環境）", ["全コンポーネントのコンテナ実行基盤", "GPUによる推論・ベクトル化の高速実行", "外部通信遮断（社内ネットワーク内で完結）"], ["NVIDIA DGX Spark", "（NVIDIA Grace Blackwell, 128GB 統合メモリ）", "Docker / NVIDIA Container Toolkit"]),
    ("ログ・評価データ", "（運用・品質管理）", ["利用ログ（質問・回答・クリック等）の記録", "評価用の正答・許容回答・必要根拠データの管理", "精度評価（RAGAS等）と改善に利用"], ["PostgreSQL（ログ・評価テーブル）", "RAGAS＋自作スクリプト（Python）"]),
]
layers = {0: (1, "#00418F", "#FFFFFF", [("利用者・対話", 19, True), ("（生産技術部員）", 19, True)]),
          1: (2, "#4EAAF4", "#FFFFFF", [("オーケストレーション", 17, True), ("（部員が触る層）", 16.5, True)]),
          3: (2, "#5DADEB", "#FFFFFF", [("ドメインAPI・検索", 17, True), ("（開発者が守る層）", 16.5, True)]),
          5: (3, "#D2EDFE", INK, [("データ", 22, True), ("（検索基盤）", 20, True)]),
          8: (3, "#E4E5E5", INK, [("基盤", 22, True), ("（モデル・インフラ・運用）", 12.5, False)])}
tint = ["#F5FAFE"] * 5 + ["#F3F9FE"] * 3 + ["#F5F6F8"] * 3

cells = [[{"text": t, "fill": "#00275F", "color": "#FFFFFF", "bold": True, "size_px": 20, "align": "c"} for t in ("レイヤ", "コンポーネント", "役割", "代表技術・製品")]]
for i, (name, sub, roles, prods) in enumerate(rows):
    row = []
    if i in layers:
        span, fill, color, paras = layers[i]
        row.append({"span": [span, 1], "fill": fill, "color": color, "align": "l", "inset_px": [72, 2, 1, 2],
                    "paras": [[{"text": t, "size_px": s, "bold": b}] for t, s, b in paras], "line_pitch_px": 29})
    else:
        row.append(None)
    row.append({"fill": tint[i], "align": "l", "inset_px": [120, 2, 4, 2], "color": INK, "line_pitch_px": 26,
                "paras": [[{"text": name, "size_px": 20 if len(name) < 18 else 15.5, "bold": True}], [{"text": sub, "size_px": 18, "color": SUB}]]})
    row.append({"fill": tint[i], "align": "l", "inset_px": [20, 2, 4, 2], "color": INK, "size_px": 15.5,
                "text": "\n".join("•  " + r for r in roles), "line_pitch_px": 22.5})
    row.append({"fill": tint[i], "align": "l", "inset_px": [24, 2, 4, 2], "color": INK, "size_px": 18 if len(prods) < 3 else 16,
                "text": "\n".join(prods), "line_pitch_px": 25 if len(prods) < 3 else 21})
    cells.append(row)

E = [
    {"type": "text", "box": [20, 4, 540, 50], "text": "表2-1　コンポーネント一覧", "size_px": 40, "bold": True, "color": "#0B1F4F", "name": "title"},
    {"type": "table", "box": [17, 58, sum(cols), ys[-1] - ys[0]], "col_widths_px": cols, "row_heights_px": rh,
     "cells": cells, "border": {"color": "#D3DEEB", "width_px": 1.2}, "name": "component-table"},
]
# layer icons
for icon, y, color, extra in [("material:groups-fill", 113, "#FFFFFF", {}), ("material:sms-fill", 228, "#FFFFFF", {}),
                               ("lucide:settings", 390, "#FFFFFF", {"stroke_width": 1.8}), ("lucide:database", 589, ICON, {"stroke_width": 2}),
                               ("lucide:server", 800, ICON, {"stroke_width": 2})]:
    E.append({"type": "icon", "icon": icon, "box": [30, y, 58, 58], "color": color, **extra})
# component icons (vertically centered per row)
comp = ["lucide:laptop", "lucide:workflow", "lucide:file-text", "lucide:settings", "lucide:book-a", "lucide:database",
        "lucide:search", "lucide:file-text", "lucide:brain", "lucide:server", "lucide:clipboard-list"]
for i, icon in enumerate(comp):
    cy = (ys[i + 1] + ys[i + 2]) / 2
    sz = 56
    el = {"type": "icon", "icon": icon, "box": [300, cy - sz / 2, sz, sz]}
    if icon.startswith("lucide"):
        el.update(color=ICON, stroke_width=2.2)
    else:
        el.update(color="#1C5FD6")
    E.append(el)

json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
