import json
HEADF = "#05306E"; INK = "#1E2440"; HEAD = "#1F3A6E"; ICON = "#1F3F7A"; RED = "#D82030"
ys = [74, 138, 235, 339, 473, 576, 683, 779, 872]
cols = [60, 303, 365, 297, 261, 351]
x0 = 18
rows = [
    ("12テーブルの基本情報", "（件数・NULL率・PK/結合キー）",
     ["各テーブルの件数、NULL率、データ型を取得", "PK/結合キーの定義を確認", "サンプルデータで内容を確認"],
     ["テーブル別データプロファイル\v（件数・NULL率・主要項目）", "PK/結合キー一覧"],
     ["全12テーブルの情報が取得できる", "PK/結合キーが特定できる"],
     ["全項目を確認", "一部不明だが代替可能", "主要テーブルが取得不可"]),
    ("JOIN到達率とキー一意性", "（テーブル間の関連性）",
     ["定義に基づくJOINを実行し到達率を測定", "キーの一意性（重複の有無）を確認", "サンプル部品でエンドツーエンドの結合確認"],
     ["テーブル結合図（ER図の実データ検証）", "JOIN到達率レポート", "キー一意性チェック結果"],
     ["主要なテーブル結合が可能（例：\v部品→作業工程→WPS→文書）", "キーの一意性が確保されている"],
     ["想定通り結合可能", "一部結合不可（代替案あり）", "主要な結合ができない"]),
    ("REV・ED・適用情報の有無", "（定義・取得方法・根拠）",
     ["各テーブルの項目にREV・ED・適用号機等の\v情報があるか確認", "情報の意味・採番ルール・更新ルールをヒアリング", "サンプルデータで実在性を確認"],
     ["REV・ED・適用情報 一覧", "取得方法・項目定義書", "サンプルデータ"],
     ["REV・ED・適用情報の有無と意味\vが明確である", "業務で利用可能な根拠がある"],
     ["情報あり・業務利用可能", "一部情報のみ（代替案あり）", None]),
    ("過去版本文の取得可否", "（版管理・履歴の参照）",
     ["過去版の文書・WPS等が取得できるか確認", "版の履歴・格納場所・アクセス方法を調査", "サンプルで複数版の取得を検証"],
     ["過去版取得検証結果", "版管理の仕組み整理資料"],
     ["過去版の本文が取得できる", "版の対応関係が特定できる"],
     ["過去版を取得可能", "一部のみ取得可能", "過去版が取得できない"]),
    ("工程名と工程タイトルの対応", "（マスタ一致性）",
     ["作業工程の工程名とロードセンターの工程\vタイトルの対応関係を確認", "コード→名称変換のルールを検証", "サンプルで不一致データの有無を確認"],
     ["工程名－工程タイトル 対応表", "コード変換ルール", "不一致データの一覧"],
     ["工程名と工程タイトルの対応が\v明確である", "コード→名称変換が可能である"],
     ["対応関係が明確", "一部不一致（対応ルールあり）", "対応関係が不明"]),
    ("文書ファイルパス実体と\v抽出精度", "（図面・WPS・SPEC 等）",
     ["ファイルパスの実体（ファイルの存在）を確認", "ファイルの種別・リビジョン・ステータスを確認", "抽出処理の精度をサンプルで検証"],
     ["ファイルパス検証結果", "文書メタデータ抽出精度レポート", "アクセス可否一覧"],
     ["ファイルが実在しアクセス可能", "タイトル・リビジョン等の\vメタデータが正しく抽出できる"],
     ["実在・抽出精度良好", "一部欠損（影響限定的）", "ファイル未存在が多い"]),
    ("代表質問の期待候補・\v必要根拠の存在", "（検索成立性の確認）",
     ["代表質問（例：部品Aの工程10、WPS番号、\v図面番号 等）を実際に実行", "期待される候補と必要な根拠情報の取得可否\vを確認"],
     ["代表質問の実行結果一覧", "候補データと根拠情報の取得状況", "検索成立性の評価レポート"],
     ["想定する候補が取得できる", "必要な根拠情報（作業内容・版・\v文書リンク等）が揃っている"],
     ["主要な質問で取得可能", "一部質問で不足（代替案あり）", "候補・根拠が取得できない"]),
]
BUL = {"bullet": True, "bullet_indent_px": 18, "line_pitch_px": 22.5, "size_px": 14, "color": INK, "align": "l", "inset_px": [12, 2, 4, 2]}
hdr = lambda t1, t2=None: {"fill": HEADF, "color": "#FFFFFF", "align": "c", "line_pitch_px": 26,
                           "paras": [[{"text": t1, "size_px": 19.5, "bold": True}]] + ([[{"text": t2, "size_px": 17.5, "bold": True}]] if t2 else [])}
cells = [[hdr("No."), hdr("診断項目", "（確認内容）"), hdr("確認方法", "（サンプル確認・分析方法）"), hdr("成果物", "（Gate 1での提出物）"), hdr("判定基準"),
          hdr("判定", "（成立／条件付き／不成立）")]]
for i, (t1, t2, how, out, crit, _) in enumerate(rows):
    cells.append([
        {"fill": "#E4EDF2", "text": str(i + 1), "size_px": 26, "bold": True, "color": HEAD, "align": "c"},
        {"fill": "#EEF5FA", "align": "l", "inset_px": [80, 2, 2, 2], "color": HEAD, "bold": True, "line_pitch_px": 24,
         "paras": [[{"text": t1, "size_px": 16}], [{"text": t2, "size_px": 15 if len(t2) < 14 else 13}]]},
        {"fill": "#FFFFFF", "text": "\n".join(how), **BUL},
        {"fill": "#FFFFFF", "text": "\n".join(out), **{**BUL, "size_px": 13, "line_pitch_px": 25}},
        {"fill": "#FFFFFF", "text": "\n".join(crit), **{**BUL, "size_px": 13, "line_pitch_px": 25}},
        {"fill": "#EBF3F8", "text": ""},
    ])
E = [
    {"type": "text", "box": [30, 6, 1300, 62], "text": "表3-3　Gate 1 診断項目 × 確認方法 × 成果物 × 判定", "size_px": 45, "bold": True, "color": HEAD, "name": "title"},
    {"type": "table", "box": [x0, ys[0], sum(cols), ys[-1] - ys[0]], "col_widths_px": cols,
     "row_heights_px": [b - a for a, b in zip(ys, ys[1:])], "cells": cells, "border": {"color": "#D3DEEB", "width_px": 1.2}, "name": "gate1-table"},
]
icons = ["material:database-fill", "lucide:network", "lucide:file-text", "lucide:copy", "material:settings-fill", "lucide:file-text", "lucide:search"]
for i, ic in enumerate(icons):
    cy = (ys[i + 1] + ys[i + 2]) / 2
    el = {"type": "icon", "icon": ic, "box": [88, cy - 28, 56, 56], "color": ICON}
    if ic.startswith("lucide"):
        el["stroke_width"] = 2.4
    E.append(el)
    if i == 2:
        E.append({"type": "roundRect", "box": [104, cy + 4, 40, 20], "radius_px": 9, "fill": ICON, "line": None,
                  "text": "REV", "size_px": 11.5, "bold": True, "color": "#FFFFFF"})
# judgment pills
PILLS = [("成立", "#61B982", "#FFFFFF"), ("条件付き", "#F9D647", "#3A2E00"), ("不成立", "#FCCED5", "#C0303A")]
for i, row in enumerate(rows):
    top, bot = ys[i + 1], ys[i + 2]
    labels = row[5]
    if labels[2] is None:  # row 3: 不成立 has a 3-line red note
        centers = [top + 20, top + 52, top + 86]
    else:
        h = bot - top
        centers = [top + h * 0.19, top + h * 0.5, top + h * 0.81]
    for (name, fill, color), cy, text in zip(PILLS, centers, labels):
        E.append({"type": "rect", "box": [1314, cy - 12, 96, 25], "fill": fill, "line": None, "text": name, "size_px": 15.5, "bold": True, "color": color})
        if text:
            E.append({"type": "text", "box": [1428, cy - 13, 224, 26], "text": text, "size_px": 15, "color": INK})
    if labels[2] is None:
        E.append({"type": "text", "box": [1428, centers[2] - 14, 224, 62], "text": "情報なし\n→ F-09/12.2 評価不可\n（範囲縮小・中止協議）",
                  "size_px": 15.5, "bold": True, "color": RED, "valign": "t", "line_pitch_px": 20})
E += [
    {"type": "roundRect", "box": [18, 877, 1637, 60], "radius_px": 6, "fill": "#FDEEF1", "line": {"color": "#E05060", "width_px": 1.5}},
    {"type": "icon", "icon": "material:error-fill", "box": [30, 879, 58, 58], "color": "#E02030"},
    {"type": "text", "box": [118, 879, 1530, 56], "text": "REV・ED・適用情報が確認できない場合、要求仕様の F-09（版・適用の追跡）および 12.2（適用範囲を考慮した検索・提示）を評価できないため、\nPoC の範囲縮小または中止について協議する。その他の項目も、不成立の場合は代替案の検討または範囲の見直しを行う。",
     "size_px": 18.5, "bold": True, "color": RED, "line_pitch_px": 26},
]
json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
