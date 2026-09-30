import json
NAVY = "#0F4592"; INK = "#1F2F4F"; HEAD = "#1F3A6E"; ICON = "#1F63C8"; LINE = "#D6E0EC"; STEP = "#E1F0FD"
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
def BUL(box, items, size=17, pitch=25, space=12):
    return add(type="text", box=box, text="\n".join(items), size_px=size, color=INK, valign="t", bullet=True,
               bullet_color=HEAD, line_pitch_px=pitch, para_space_px=space, bullet_indent_px=24)
def step(x, w, icon, lines):
    R([x, 248, w, 92], fill=STEP, r=4)
    if icon:
        I(icon, [x + 6, 254, 42, 42], ICON, stroke_width=2)
    add(type="text", box=[x + (40 if icon else 0), 252, w - (40 if icon else 0), 84],
        paras=[[{"text": t, "size_px": s, "bold": True}] for t, s in lines], color=HEAD, align="c",
        line_pitch_px=28 if len(lines) == 3 else 38)
def arrowhead(x):
    add(type="chevron", box=[x, 260, 14, 30], point_px=14, fill="#1F3A6E", line=None)
def kv(box, rows, heights, key_w, size=14):
    add(type="table", box=box, col_widths_px=[key_w, box[2] - key_w], row_heights_px=heights,
        cells=[[{"text": k, "fill": "#F3F6FA"}, {"text": v, "fill": "#FFFFFF"}] for k, v in rows],
        size_px=size, align="l", color=INK, border={"color": "#DCE3EC", "width_px": 1}, cell_pad_px=5,
        line_pitch_px=size * 1.45)

# title + lead
R([24, 18, 18, 50], fill="#1F3F7A")
T([62, 12, 1200, 62], "N-PLUS／共有文書を具体的にどう検索単位へ変換するか", 42, bold=True, color=HEAD)
add(type="image", path="logo.png", box=[1512, 12, 146, 34], name="logo")
R([24, 84, 1624, 78], fill="#EDEEF1", r=6)
T([52, 90, 1580, 66], "N-PLUSは作業工程を起点に関連テーブルをJOINし、1件の作業工程を業務上意味のあるTOS検索単位に変換する。\n共有文書は、章・節・項番の構造を保持して分割し、文書番号・REV・ページ等のメタデータを付与して検索単位を作る。",
  22, color="#2A3550", line_pitch_px=33)

# section frames
for x, w, n, t1, t2 in [(18, 816, "1", "N-PLUS：", "作業工程を起点に関連情報を統合し、TOS検索単位を作る"),
                        (850, 804, "2", "共有文書：", "文書の構造を保持して分割し、検索単位を作る")]:
    R([x, 180, w, 728], fill="#FFFFFF", line=L(LINE, 1.2), r=4)
    R([x, 180, w, 48], fill=NAVY, r=4)
    add(type="ellipse", box=[x + 14, 188, 34, 34], fill="#FFFFFF", line=None, text=n, size_px=22, bold=True, color=NAVY)
    add(type="text", box=[x + 64, 180, w - 70, 48], paras=[[{"text": t1, "size_px": 23, "bold": True}, {"text": t2, "size_px": 21}]], color="#FFFFFF")

# ---- section 1
step(36, 244, "lucide:clipboard-list", [("STEP1", 19), ("元データ", 20), ("（主要テーブル）", 20)])
arrowhead(288)
step(310, 230, None, [("STEP2", 19), ("加工（統合・変換・文脈化）", 17)])
arrowhead(548)
step(572, 252, "lucide:clipboard-pen", [("STEP3", 19), ("TOS検索単位（例）", 19)])
I("material:database-fill", [22, 374, 58, 58], "#7F95B8")
tables = [("部品テーブル", "（部品番号・名称・材質 等）"), ("作業工程テーブル（TOS）", "（工程番号・作業内容 等）"), ("ロードセンターテーブル", "（L/Cコード・工程名 等）"),
          ("WPSテーブル", "（WPS番号・リビジョン 等）"), ("作業工程履歴テーブル", "（変更日・変更理由 等）"), ("CSC／ドキュメント", "（図面番号・文書番号 等）"),
          ("MBOM／EBOM", "（親子部品・有効開始/終了日 等）")]
for i, (t1, t2) in enumerate(tables):
    y = 357 + i * 62
    R([82, y, 200, 52], fill="#F2F7FD", line=L("#DCE6F2", 1), r=4)
    add(type="text", box=[92, y + 2, 190, 48], paras=[[{"text": t1, "size_px": 16.5, "bold": True, "color": HEAD}], [{"text": t2, "size_px": 13.5}]],
        color=INK, line_pitch_px=22)
T([88, 796, 60, 24], "…", 16, color="#6B7385")
BUL([318, 352, 234, 380], ["部品番号・工程番号等で\v関連テーブルをJOIN", "最新の作業工程履歴を取得\v（変更日・変更理由）", "コード値を業務名称へ変換\v（L/Cコード → 工程名 など）",
                        "略語・同義語を辞書で展開", "部品・工程・作業内容・職場・\vWPS・図面・上位組立・版/適用\v等を1つの文脈に統合", "基本は「作業工程1行＝1検索\v候補」とする"],
    size=15, pitch=25, space=11)
for x, y in [(316, 748), (316, 796), (370, 768)]:
    I("lucide:table", [x, y, 46, 46], "#5E7598", stroke_width=1.6)
add(type="rightArrow", box=[420, 778, 40, 26], fill="#9DBDE3", line=None)
I("lucide:file-text", [460, 752, 66, 66], ICON, stroke_width=1.8)
T([320, 842, 200, 50], "複数テーブルをJOINし\n1件に統合", 17, color=INK, align="c", line_pitch_px=26)
R([566, 352, 258, 34], fill=STEP, r=2)
T([566, 352, 258, 34], "作業工程1件を検索単位として保持", 14.5, bold=True, color=HEAD, align="c")
rows1 = [("部品番号", "A12345"), ("部品名称", "ブラケット"), ("材質", "AL"), ("工程番号", "10"), ("工程名", "バリ取り"), ("作業区分", "機械加工"),
         ("作業内容", "バリ取り作業を行う…"), ("ロードセンター", "L001（機械加工）"), ("WPS", "W-55 Rev.C"), ("図面", "D-12345 Rev.C"),
         ("上位組立", "A320 001 ～ 050"), ("最終変更日", "2025-06"), ("変更理由", "治具変更"), ("版・適用情報", "REV B / 001～050"),
         ("元テーブル/PK", "作業工程 (A,10)"), ("検索用テキスト", "部品A ブラケット(AL)の\v工程10 バリ取り…")]
kv([566, 392, 258, 466], rows1, [26.6] * 15 + [67], 106, size=12.3)

# ---- section 2
step(868, 210, "lucide:file-text", [("STEP1", 19), ("元文書", 20), ("（Word／Excel／PDF）", 14.5)])
arrowhead(1082)
step(1106, 246, None, [("STEP2", 19), ("加工", 20), ("（分割・構造化・メタデータ付与）", 14.5)])
arrowhead(1362)
step(1386, 254, "lucide:file-text", [("STEP3", 19), ("文書検索単位（例）", 19)])
for y, fill, glyph, name, sub in [(388, "#2B6CD6", "W", "Word", "（作業手順書・仕様書 等）"), (472, "#1E7B4E", "X", "Excel", "（一覧表・管理表 等）"),
                                  (560, "#D93A30", None, "PDF", "（マニュアル・図面説明 等）")]:
    if glyph:
        R([872, y, 54, 54], fill=fill, r=8, text=glyph, size_px=27, bold=True, color="#FFFFFF")
    else:
        R([872, y, 54, 54], fill=fill, r=8)
        I("material:picture_as_pdf", [881, y + 9, 36, 36], "#FFFFFF")
    add(type="text", box=[936, y + 2, 150, 52], paras=[[{"text": name, "size_px": 17, "bold": True, "color": HEAD}], [{"text": sub, "size_px": 13}]],
        color=INK, line_pitch_px=25)
# page mock (native)
R([880, 670, 176, 168], fill="#FFFFFF", line=L("#B9C2CE", 2))
for i in range(6):
    add(type="line", points=[[896, 688 + i * 10], [1040 - (30 if i % 3 == 2 else 0), 688 + i * 10]], color="#A7B0BD", width_px=2)
for x, w in [(896, 78), (980, 56)]:
    R([x, 752, w, 42], fill=None, line=L("#E03030", 2))
    add(type="line", points=[[x, 766], [x + w, 766]], color="#C9D0DA", width_px=1)
    add(type="line", points=[[x, 780], [x + w, 780]], color="#C9D0DA", width_px=1)
for i in range(2):
    add(type="line", points=[[896, 808 + i * 10], [1040, 808 + i * 10]], color="#A7B0BD", width_px=2)
T([888, 850, 40, 22], "…", 16, color="#6B7385")
BUL([1114, 352, 244, 330], ["見出し（章／節／項番）の\v階層構造を保持して分割", "表はヘッダと各行の関係を保持\v（1表の1行を1単位に）", "Excelはシート・セル、\vWordは表番号、PDFはページ\vなど、原文上の位置情報を保持",
                         "文書番号・REV・発効日・\v取得元パス等のメタデータを付与", "意味が通る文書チャンクを\v検索単位として作る"], size=15, pitch=25, space=12)
R([1104, 690, 96, 130], fill="#FFFFFF", line=L("#B9C2CE", 2))
for y in (712, 760):
    R([1112, y, 80, 40], fill=None, line=L("#E03030", 2))
    add(type="line", points=[[1112, y + 13], [1192, y + 13]], color="#C9D0DA", width_px=1)
    add(type="line", points=[[1112, y + 26], [1192, y + 26]], color="#C9D0DA", width_px=1)
for y in (710, 758, 806):
    add(type="arrow", points=[[1200, 756], [1232, 756], [1232, y], [1262, y]], color="#3B7DD8", width_px=2, head_size="sm")
    R([1266, y - 20, 74, 40], fill="#FFFFFF", line=L("#B9C2CE", 1.5))
    I("lucide:file-text", [1272, y - 14, 28, 28], "#5E7598", stroke_width=2)
    for k in range(3):
        add(type="line", points=[[1304, y - 8 + k * 8], [1334, y - 8 + k * 8]], color="#A7B0BD", width_px=1.5)
T([1110, 838, 240, 50], "章・節・項番・表などで分割し\nメタデータを付与", 17, color=INK, align="c", line_pitch_px=26)
R([1368, 352, 274, 36], fill=STEP, r=2)
T([1368, 352, 274, 36], "文書の一部（チャンク）を検索単位として保持", 12.5, bold=True, color=HEAD, align="c")
rows2 = [("見出しパス", "第3章 > 3.2 > 注意事項"), ("本文", "作業時の注意事項は\v以下のとおり…\v・必ず保護具を着用する…\v・電源を切ってから作業…"), ("文書番号", "D-12345"), ("REV", "B"),
         ("発効日", "2024-06-01"), ("ページ", "p.15"), ("項番", "3.2"), ("シート／セル", "Sheet1 / B5"), ("元ファイルパス", "/folder/…/作業手順書.pdf"),
         ("抽出方式", "章・節・項番で分割"), ("抽出品質", "正常（表構造保持）"), ("検索用テキスト", "作業時の注意事項 保護具\v電源を切ってから作業…")]
kv([1368, 394, 274, 440], rows2, [42, 96] + [27] * 9 + [59], 98, size=12.3)

json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
