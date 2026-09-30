import json
NAVY = "#173A6E"; INK = "#1F2F4F"; HEAD = "#1F3A6E"; ICON = "#1F3F7A"; LINE = "#D6E0EC"
PALE = "#EEF3F9"; BAND = "#E6EEF8"
E = []
def add(**k): E.append(k); return k
def T(box, text, size, bold=False, color=INK, align="l", valign="m", **k):
    return add(type="text", box=box, text=text, size_px=size, bold=bold, color=color, align=align, valign=valign, **k)
def R(box, fill="#FFFFFF", line=None, r=None, **k):
    d = dict(type="roundRect" if r is not None else "rect", box=box, fill=fill, line=line, **k)
    if r is not None: d["radius_px"] = r
    return add(**d)
def L(c, w=1.2, dash=None): return {"color": c, "width_px": w, **({"dash": dash} if dash else {})}
def I(icon, box, color=ICON, **k): return add(type="icon", icon=icon, box=box, color=color, **k)
def BUL(box, items, size=16.5, pitch=24, space=9):
    return add(type="text", box=box, text="\n".join(items), size_px=size, color=INK, valign="t", bullet=True,
               line_pitch_px=pitch, para_space_px=space, bullet_indent_px=18)
def chip(x, y, w, h, text, size=15):
    R([x, y, w, h], fill=PALE, r=2)
    T([x + 14, y, w - 14, h], text, size)
def bracket(x, y1, y2, tick=True):
    add(type="line", points=[[x, y1], [x + 8, y1 + 4], [x + 8, y2 - 4], [x, y2]], color="#5A7196", width_px=1.5)
    if tick:
        m = (y1 + y2) / 2
        add(type="line", points=[[x + 8, m], [x + 16, m]], color="#5A7196", width_px=1.5)
def unit_box(x, y, w, h, label):
    R([x, y, w, h], fill="#2E5A8E", r=6)
    I("lucide:file-text", [x + w / 2 - 20, y + 8, 40, 40], "#FFFFFF", stroke_width=2)
    T([x, y + 50, w, h - 54], label, 16, bold=True, color="#FFFFFF", align="c", line_pitch_px=21)

# title + lead
R([0, 18, 26, 52], fill="#18356B")
T([46, 12, 820, 64], "検索に使えるデータへどう整えるか", 42, bold=True, color=HEAD)
add(type="image", path="logo.png", box=[1512, 12, 146, 34], name="logo")
R([24, 84, 1624, 82], fill="#EDEEF1", r=6)
T([52, 92, 1580, 68], "N-PLUSと共有文書をそのまま検索するのではなく、業務上意味のある「検索単位」に加工する。\n検索に必要な情報だけでなく、版・適用・根拠まで紐付け、正確検索と類似検索の双方で利用できる状態にする。",
  23, color="#2A3550", line_pitch_px=34)

# column headers + frames
cols = [(25, 532, "1", "現状の課題", " — 元データのままでは検索に使いにくい"),
        (571, 533, "2", "どう整えるか", " — 業務上の意味が通る検索単位を作る"),
        (1118, 530, "3", "検索基盤でどう保持するか", " — 検索情報と根拠情報をセットで持つ")]
for x, w, n, t1, t2 in cols:
    R([x, 226, w, 674], fill="#FFFFFF", line=L(LINE, 1.2), r=4)
    R([x, 180, w, 46], fill=NAVY)
    add(type="ellipse", box=[x + 17, 186, 34, 34], fill="#FFFFFF", line=None, text=n, size_px=22, bold=True, color=NAVY)
    add(type="text", box=[x + 62, 180, w - 66, 46], paras=[[{"text": t1, "size_px": 22, "bold": True}, {"text": t2, "size_px": 15 if n != "3" else 12}]],
        color="#FFFFFF")
for x in (551, 1106):
    for y in (425, 723):
        add(type="chevron", box=[x, y, 24, 62], point_px=16, fill="#1F4E8C", line=None)

# ---- column 1
R([36, 240, 510, 386], fill="#F7FAFD", r=6)
R([36, 240, 510, 44], fill=BAND, r=6)
T([52, 240, 400, 44], "N-PLUS（構造化データ）", 20, bold=True, color=HEAD)
R([42, 294, 238, 38], fill="#DCE8F5", r=2)
T([42, 294, 238, 38], "情報が複数テーブルに分散", 17, bold=True, color=HEAD, align="c")
I("material:database-fill", [44, 408, 80, 80])
for i, t in enumerate(["部品", "作業工程（TOS）", "WPS", "作業工程履歴", "ロードセンター", "図面／ドキュメント", "版・適用情報", "MBOM／EBOM", "CSC", "…"]):
    chip(146, 343 + i * 27.5, 134, 24, t)
R([296, 294, 244, 324], fill=PALE, r=4)
BUL([312, 306, 226, 310], ["部品・作業工程・WPS・\v履歴・図面・MBOM等が\v別テーブルに分散", "1レコードだけでは「どの\v部品の、どの工程で、何を\vするのか」が揃わない",
                        "コード値や関連情報を\v横断しないと意味が分\vからない", "REV・適用号機等は、現時点\vの定義書では所在が確認\vできないものがある"])
R([36, 640, 510, 250], fill="#F7FAFD", r=6)
R([40, 645, 242, 70], fill=BAND, r=4)
T([52, 648, 230, 64], "共有文書\n（Word／Excel／PDF）", 20, bold=False, color=HEAD, line_pitch_px=32,
  )
E[-1]["paras"] = [[{"text": "共有文書", "bold": True}], [{"text": "（Word／Excel／PDF）"}]]; E[-1].pop("text")
for x, letter in [(58, "W"), (140, "X"), (214, "PDF")]:
    I("lucide:file", [x, 748, 54, 60], ICON, stroke_width=2.4)
    T([x, 764, 54, 40], letter if letter != "PDF" else "⅄", 22 if letter != "PDF" else 20, bold=True, color=ICON, align="c")
T([56, 818, 240, 60], "形式・構成がバラバラで、\n必要箇所の特定が難しい", 18, bold=True, color=HEAD, line_pitch_px=28)
R([296, 648, 244, 236], fill=PALE, r=4)
BUL([312, 660, 226, 220], ["Word／Excel／PDFなど\v形式が異なる", "文書全体をそのまま検索\v単位にすると、必要箇所を\v特定しづらい", "表・見出し・ページ等の\v構造を失うと、根拠箇所\vまで戻れない"])

# ---- column 2 (upper)
R([580, 240, 514, 344], fill="#F7FAFD", r=6)
R([580, 240, 514, 44], fill=BAND, r=6)
T([596, 240, 490, 44], "N-PLUSを統合し、TOSを起点とした検索単位に加工", 19, bold=True, color=HEAD)
for y in (312, 390, 478):
    I("material:database-fill", [598, y, 52, 52])
for i, t in enumerate(["部品", "作業工程（TOS）", "WPS", "作業工程履歴", "ロードセンター", "図面／ドキュメント", "MBOM／EBOM", "CSC", "…"]):
    chip(656, 299 + i * 28.3, 128, 24, t)
bracket(786, 316, 536)
unit_box(808, 380, 76, 100, "TOS\n検索単位")
R([888, 292, 204, 286], fill=PALE, r=4)
BUL([898, 296, 196, 280], ["作業工程を起点に関連\vテーブルをJOIN", "部品番号・工程番号等の\vキーで、部品／WPS／履\v歴／図面／MBOM等を\v紐付け", "コードを業務名称へ変換",
                        "部品・工程・作業内容・職\v場・WPS・変更履歴等を\v1つの文脈に統合", "基本は「作業工程1行＝\v1検索候補」"], size=16, pitch=22.3, space=6, )
E[-1]["bullet_indent_px"] = 16

# ---- column 2 (lower)
R([580, 598, 514, 292], fill="#F7FAFD", r=6)
R([580, 598, 514, 44], fill=BAND, r=6)
T([596, 598, 490, 44], "共有文書を意味のある単位に分割し、メタデータを付与", 19, bold=True, color=HEAD)
I("lucide:file-text", [602, 690, 38, 42], ICON, stroke_width=2)
T([592, 730, 60, 22], "Word", 15, bold=True, color=ICON, align="c")
I("lucide:file-spreadsheet", [604, 754, 34, 38], ICON, stroke_width=2)
T([592, 788, 60, 18], "Excel", 12, bold=True, color=ICON, align="c")
I("lucide:file", [604, 812, 34, 38], ICON, stroke_width=2)
T([592, 850, 60, 22], "PDF", 15, bold=True, color=ICON, align="c")
add(type="line", points=[[667, 672], [667, 855]], color="#5A7196", width_px=1.5)
for i, t in enumerate(["章", "節", "項番", "表（行単位）", "図・図面", "1ページ", "…"]):
    y = 673 + i * 30.3
    add(type="arrow", points=[[667, y], [690, y]], color="#5A7196", width_px=1.3, head_size="sm")
    chip(694, y - 12, 90, 24, t)
bracket(786, 678, 850)
unit_box(808, 714, 76, 94, "文書\n検索単位")
R([888, 650, 204, 236], fill=PALE, r=4)
BUL([898, 652, 196, 232], ["章・節・項番の階層を保\v持して分割", "表はヘッダと各行の関係\vを保持", "Excelはシート・セル、\vWordは表番号、PDFは\vページを保持",
                        "文書番号・REV・発効日・\v取得元等を付与", "「意味が通る文書チャンク」\vを検索単位として作る"], size=16, pitch=22, space=0)
E[-1]["bullet_indent_px"] = 16

# ---- column 3
def kv_table(y, rows, last, h=22.1):
    add(type="table", box=[1236, y, 280, h * len(rows)], col_widths_px=[106, 174], row_heights_px=[h] * len(rows),
        cells=[[{"text": k}, {"text": v}] for k, v in rows], size_px=13.2, align="l", color=INK,
        border={"color": "#DDE5EF", "width_px": 1}, cell_pad_px=5)
    add(type="table", box=[1236, y + h * len(rows), 400, h], col_widths_px=[106, 294], row_heights_px=[h],
        cells=[[{"text": last[0]}, {"text": last[1]}]], size_px=13.2, align="l", color=INK,
        border={"color": "#DDE5EF", "width_px": 1}, cell_pad_px=5)
def side_label(y, t1, t2):
    add(type="text", box=[1546, y, 110, 52], paras=[[{"text": t1, "size_px": 18, "bold": True}], [{"text": t2, "size_px": 15.5}]],
        color=HEAD, line_pitch_px=26)

R([1134, 240, 502, 36], fill=BAND, r=4)
T([1150, 240, 480, 36], "TOS検索単位（構造化データ）", 20, bold=True, color=HEAD)
I("lucide:file-text", [1144, 364, 84, 84], ICON, stroke_width=1.8)
kv_table(277, [("部品番号", "A12345"), ("部品名称", "ブラケット"), ("材質", "Ti合金"), ("工程番号", "LC001"), ("工程名", "バリ取り"), ("作業内容", "機械加工"),
               ("WPS", "W-55 Rev.C"), ("図面", "D-12345 Rev.C"), ("上位組立", "A320 001～050"), ("変更日／理由", "2025-06／治具変更"),
               ("版・適用情報", "REV B、001～050"), ("元テーブル/PK", "作業工程 (A,10)")], ("検索用テキスト", "部品A ブラケット(SUS) の工程10…"))
bracket(1520, 286, 408); side_label(322, "業務情報", "（検索に使う）")
bracket(1520, 418, 530); side_label(458, "根拠情報", "（元データへ戻る）")

R([1134, 590, 502, 36], fill=BAND, r=4)
T([1150, 590, 480, 36], "文書検索単位（非構造化データ）", 20, bold=True, color=HEAD)
I("lucide:file-text", [1144, 694, 84, 84], ICON, stroke_width=1.8)
kv_table(629, [("本文", "作業手順として…"), ("見出しパス", "第3章 ＞3.2 ＞注意事項"), ("文書番号", "D-12345"), ("REV", "B"), ("発効日", "2024-06-01"),
               ("ページ／項番", "p.15 ／ 第3章 3.2"), ("シート／セル", "Sheet1 ／ B5"), ("ファイルパス", "/folder/…/作業手順書.pdf"),
               ("抽出方式", "章・節・項番で分割"), ("抽出品質", "正常（表構造保持）")], ("検索用テキスト", "穴あけ加工時の注意事項…"), h=23)
bracket(1522, 634, 752); side_label(670, "業務情報", "（検索に使う）")
bracket(1522, 770, 868); side_label(800, "根拠情報", "（元文書へ戻る）")

T([1600, 906, 44, 26], "6", 14, color="#6B7385", align="r")
json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
