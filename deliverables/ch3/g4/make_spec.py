import json
HEADF = "#002B65"; INK = "#1E2440"; HEAD = "#1F3A6E"; ICON = "#1F3F7A"; RED = "#D82030"
ys = [72, 138, 247, 361, 477, 577, 686, 772, 872]
cols = [329, 457, 481, 370]
x0 = 18
rows = [
    ("REV", "（改訂版）", ["最新版の特定ができず、古い工程・図面・WPS\vを参照するリスクがある。", "変更差分の追跡や類似検索の精度が低下する。"],
     ["各テーブルでのREVの有無と定義・採番ルール", "関連テーブル間のREVの紐付け方法", "最新版の判定ロジック（最大値？有効日？ステータス？）"],
     "REVを前提とした絞り込みは\v行わない。", "検索結果に版の情報を付与できない\v旨を明示し、要確認として扱う。"),
    ("ED", "（設計変更）", ["設計変更の反映状況が分からず、", "適用外のデータを提示する可能性がある。", "変更影響の分析（過去→現行）ができない。"],
     ["EDの項目有無、管理テーブル・採番ルール", "対象データ（部品／工程／図面／WPS等）との紐付け方法", "有効期間・適用範囲との関係"],
     "EDを考慮したフィルタリングは\v行わない。", "該当有無は不明として、\v結果に注意書きを付与する。"),
    ("適用単位", "（機体・型式・号機など）", ["データの適用範囲が不明で、\v特定機体・型式向けかの判断ができない。", "類似工程の検索時に誤った候補を提示する\vリスクがある。"],
     ["適用単位の項目有無（機体／型式／号機／ブロック等）", "管理テーブル・コード体系", "工程・図面・WPSとの紐付け方法", "適用範囲の優先順位・判定ロジック"],
     "適用単位による絞り込みは行わない。", "適用範囲は不明として、\v結果に注意書きを付与する。"),
    ("文書の有効日", "（発行日・有効開始／終了日）", ["文書が現行有効か判断できず、\v失効した図面・WPS・SPECを参照する\v可能性がある。"],
     ["各文書の有効日項目の有無・定義", "有効開始日・終了日の管理方法", "日付に基づく検索・フィルタの可否"],
     "有効日を考慮した絞り込みは行わない。", "文書の有効性は不明として、\v結果に注意書きを付与する。"),
    ("文書のステータス", "（作成中・承認・発行・廃止等）", ["承認前や廃止済みの文書を提示する\vリスクがある。", "業務で使用できないドキュメントを\v参照する可能性がある。"],
     ["ステータスの項目有無・ステータス区分", "承認フローとの関係（承認者・承認日等）", "ステータスによる検索・フィルタ条件"],
     "ステータスによる絞り込みは行わない。", "文書の状態は不明として、\v結果に注意書きを付与する。"),
    ("正本ソース", "（正本データの所在）", ["どのシステム／テーブルの情報を\v正とするか不明で、データの不整合や\v重複が発生する。"],
     ["各項目の正本ソース（テーブル・システム）の特定", "同一情報の重複管理の有無と優先順位", "マスタとトランザクションの役割分担"],
     "正本の断定は行わない。", "複数ソースが存在する場合は、\v出典を併記し、要確認として扱う。"),
    ("更新条件", "（データ更新のタイミング・ルール）", ["データの鮮度が不明で、最新情報を\v反映できない可能性がある。", "更新差分の取り込みタイミングを誤ると、\v検索結果の信頼性が低下する。"],
     ["各テーブルの更新頻度・トリガー条件", "バッチ更新／リアルタイム更新の別", "更新履歴の取得可否", "PoC期間中のデータ更新の扱い"],
     "更新の前提は置かない。", "取得時点のデータでの検索に限定し、\v鮮度に関する注意書きを付与する。"),
]
BUL = {"bullet": True, "bullet_indent_px": 20, "line_pitch_px": 25.5, "size_px": 16.5, "color": INK, "align": "l", "inset_px": [18, 2, 4, 2]}
hdr = lambda t1, t2=None: {"fill": HEADF, "color": "#FFFFFF", "align": "c", "line_pitch_px": 24,
                           "paras": [[{"text": t1, "size_px": 20, "bold": True}]] + ([[{"text": t2, "size_px": 15.5, "bold": True}]] if t2 else [])}
cells = [[hdr("不足情報"), hdr("影響", "（何ができない／どのようなリスクがあるか）"), hdr("Gate 1で確認すること", "（確認内容・論点）"), hdr("未確認時の扱い", "（PoCでの方針）")]]
for name, sub, impact, check, red, note in rows:
    long_sub = len(sub) > 12
    cells.append([
        {"fill": "#E9F5FD", "align": "l", "inset_px": [94, 2, 2, 2], "color": HEAD, "line_pitch_px": 30,
         "paras": [[{"text": name, "size_px": 22, "bold": True}], [{"text": sub, "size_px": (13 if len(sub) > 15 else 14.5) if long_sub else 17, "bold": True}]]},
        {"fill": "#FFFFFF", "text": "\n".join(impact), **BUL},
        {"fill": "#FFFFFF", "text": "\n".join(check), **{**BUL, "size_px": 15.5}},
        {"fill": "#E4F1FC", "align": "l", "inset_px": [28, 2, 4, 2], "line_pitch_px": 24.5, "color": INK,
         "paras": [[{"text": red, "size_px": 16.5, "bold": True, "color": RED}]] + [[{"text": t, "size_px": 16.5}] for t in note.split("\v")]},
    ])
E = [
    {"type": "text", "box": [30, 6, 1300, 62], "paras": [[{"text": "表3-2　不足情報リスト", "size_px": 44}, {"text": "（現時点の定義にない／根拠が薄い項目）", "size_px": 37}]],
     "bold": True, "color": HEAD, "name": "title"},
    {"type": "table", "box": [x0, ys[0], sum(cols), ys[-1] - ys[0]], "col_widths_px": cols,
     "row_heights_px": [b - a for a, b in zip(ys, ys[1:])], "cells": cells, "border": {"color": "#D3DEEB", "width_px": 1.2}, "name": "shortage-table"},
]
icons = [("lucide:file-text", None), ("lucide:file", "ED"), ("material:flight-fill", None), ("lucide:calendar-days", None),
         ("lucide:file-search", None), ("material:database-fill", None), ("lucide:refresh-cw", None)]
for i, (ic, label) in enumerate(icons):
    cy = (ys[i + 1] + ys[i + 2]) / 2
    el = {"type": "icon", "icon": ic, "box": [38, cy - 28, 56, 56], "color": ICON}
    if ic.startswith("lucide"):
        el["stroke_width"] = 2.2
    E.append(el)
    if label:
        E.append({"type": "text", "box": [38, cy - 12, 56, 30], "text": label, "size_px": 15, "bold": True, "color": ICON, "align": "c"})
    if i == 0:
        E.append({"type": "roundRect", "box": [56, cy + 4, 38, 20], "radius_px": 9, "fill": ICON, "line": None,
                  "text": "REV", "size_px": 11.5, "bold": True, "color": "#FFFFFF"})
E += [
    {"type": "roundRect", "box": [18, 879, 1637, 58], "radius_px": 6, "fill": "#FDEEF1", "line": {"color": "#E05060", "width_px": 1.5}},
    {"type": "icon", "icon": "material:error-fill", "box": [30, 880, 56, 56], "color": "#E02030"},
    {"type": "text", "box": [110, 881, 1530, 54], "text": "上記項目が未確認の場合、検索結果について版・適用範囲・有効性等を断定せず、「要確認」として扱う。\nGate 1にて必要な項目の有無・テーブル定義・取得方法を確認し、TOS検索単位および文書チャンクの構築方針を確定する。",
     "size_px": 19.5, "bold": True, "color": RED, "line_pitch_px": 26},
]
json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
