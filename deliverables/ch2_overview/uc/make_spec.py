import json
NAVY = "#00295B"; BLUE = "#1665AE"; ICON = "#1A62AC"; INK = "#1B2E55"; SUB = "#2F4468"
PANEL = "#EAF4FC"; CARD = "#D9EDFC"; GRAY = "#EEF1F5"; GRAYP = "#E6E8EB"; BORDER = "#C9D8E8"
E = []
def add(**k): E.append(k); return k
def T(box, text, size, bold=True, color=INK, align="l", valign="m", **k):
    return add(type="text", box=box, text=text, size_px=size, bold=bold, color=color, align=align, valign=valign, **k)
def R(box, fill="#FFFFFF", line=None, r=None, **k):
    d = dict(type="roundRect" if r is not None else "rect", box=box, fill=fill, line=line, **k)
    if r is not None: d["radius_px"] = r
    return add(**d)
def A(pts, color=BLUE, w=4, **k): return add(type="arrow", points=pts, color=color, width_px=w, **k)
def I(icon, box, color=ICON, **k): return add(type="icon", icon=icon, box=box, color=color, **k)
def L(c, w=1.5, dash=None): return {"color": c, "width_px": w, **({"dash": dash} if dash else {})}
def bullets(box, items, size=18, pitch=27, color=INK):
    return add(type="text", box=box, text="\n".join("•  " + t for t in items), size_px=size, bold=False,
               color=color, valign="t", line_pitch_px=pitch)

# outer frame
R([12, 10, 1648, 920], fill="#FFFFFF", line=L(BORDER, 1.5), r=14, name="frame")

# UC1 header
R([12, 10, 598, 58], fill=NAVY, r=6, name="uc1-header")
T([12, 10, 598, 58], "UC1：確定キーからの構造化検索（N-PLUS／TOS）", 21, color="#FFFFFF", align="c")
R([12, 68, 598, 112], fill="#EEF5FC")
T([12, 78, 598, 92], "部品番号・工程番号などの確定キーから、\nN-PLUSのTOS検索単位1行を構造化検索で取得\n→ 版・適用 → 根拠提示", 19, align="c", line_pitch_px=29)

# UC2 header
R([1067, 10, 593, 78], fill=NAVY, r=6, name="uc2-header")
T([1067, 14, 593, 70], "UC2：自然言語からの全文＋ベクトル検索\n（共有文書）", 22, color="#FFFFFF", align="c", line_pitch_px=33)
R([1067, 88, 593, 93], fill="#EEF5FC", line=L(BORDER, 1))
T([1067, 100, 593, 70], "自然言語の問いから、共有文書の見出し付きチャンクを\n全文BM25＋ベクトルで検索 → RRF → 根拠箇所を提示", 19, align="c", line_pitch_px=33)

# user (center)
R([714, 40, 244, 157], fill="#E3F2FB", line=L("#9CC2E8", 1.5), r=12)
T([714, 52, 244, 32], "利用者", 24, color="#1F5FA8", align="c")
T([714, 84, 244, 28], "（生産技術部員）", 19, align="c")
I("material:groups-fill", [778, 94, 116, 116], "#123A6E")
A([[800, 199], [800, 294]], w=4)
A([[870, 199], [870, 294]], w=4)
T([640, 213, 165, 50], "確定キーで検索\n（UC1）", 17, align="c", line_pitch_px=25)
T([878, 213, 150, 50], "自然言語で質問\n（UC2）", 17, align="c", line_pitch_px=25)

# Dify
R([536, 297, 600, 203], fill="#F3F9FE", line=L("#3F87D6", 2), r=8, name="dify")
R([536, 297, 600, 72], fill=BLUE, r=8)
R([536, 340, 600, 29], fill=BLUE)
T([536, 302, 600, 36], "Dify", 30, color="#FFFFFF", align="c")
T([536, 336, 600, 30], "（表示・オーケストレーション）", 20, color="#FFFFFF", align="c")
for x, w, ic, t1, t2 in [(550, 186, "lucide:message-square-more", "ユーザーインターフェース", "（入力・結果表示）"),
                         (752, 180, "lucide:network", "ワークフロー制御", "（検索・生成の連携）"),
                         (948, 178, "lucide:file-text", "プロンプト管理", "（テンプレート・履歴）")]:
    R([x, 380, w, 108], fill="#E4F1FC", r=6)
    I(ic, [x + w / 2 - 24, 388, 48, 46], ICON, stroke_width=2)
    T([x, 440, w, 44], t1 + "\n" + t2, 14.5, bold=False, align="c", color=SUB, line_pitch_px=22)
A([[836, 503], [836, 555]], w=6, head="both")

# common search API
R([536, 558, 600, 166], fill="#E3F2FC", line=L("#3F87D6", 2), r=8, name="search-api")
I("material:dns-fill", [616, 566, 66, 66], "#1F4E8C")
T([690, 568, 310, 34], "共通検索API", 26, align="c")
T([690, 600, 310, 30], "（検索・取得・確定処理）", 19, align="c")
for x, w, paras in [(550, 198, [("検索処理", 17, True), ("（構造化／全文／ベクトル）", 15.5, False)]),
                    (765, 165, [("RRF による", 17, True), ("結果統合", 15.5, False), ("（UC2）", 15.5, False)]),
                    (946, 176, [("確定処理", 17, True), ("（版・適用判定 等）", 15.5, False)])]:
    add(type="roundRect", box=[x, 640, w, 76], radius_px=6, fill="#EFF7FE", line=None,
        paras=[[{"text": t, "size_px": s, "bold": b}] for t, s, b in paras], color=INK,
        line_pitch_px=24 if len(paras) == 2 else 21)
A([[703, 757], [703, 727]], w=5)
A([[973, 757], [973, 727]], w=5)

# data sources
R([537, 760, 605, 162], fill=GRAYP, r=8, name="data-sources")
T([552, 764, 300, 30], "データソース（保存単位）", 18)
for x, w, ic, t1, t2, s1, s2 in [(552, 284, "material:database-fill", "N-PLUS／TOS", "（構造化データ）", "保存単位：テーブルの1行", "（部品、工程、版、適用 など）"),
                                 (851, 276, "material:file_copy-fill", "共有ファイル／JP 等", "（非構造化データ）", "保存単位：ドキュメント", "（ファイル、ページ、見出し、段落）")]:
    R([x, 798, w, 114], r=6)
    I(ic, [x + 14, 808, 52, 54], ICON)
    T([x + 60, 804, w - 60, 56], t1 + "\n" + t2, 18, align="c", line_pitch_px=26)
    T([x, 862, w, 44], s1 + "\n" + s2, 14, bold=False, align="c", color=SUB, line_pitch_px=21)

# UC1 column
R([44, 208, 444, 168], fill=PANEL, r=8, name="uc1-input")
T([60, 216, 300, 32], "ユーザー入力（確定キー）", 19, color="#1F4E8C")
R([58, 258, 78, 100], r=8)
I("material:person-fill", [62, 270, 70, 72], "#123A6E")
R([170, 257, 302, 102], line=L("#9DB5D2", 1.5), r=12)
bullets([186, 266, 284, 88], ["部品番号：12345-678", "工程番号：PRC-010", "その他の条件（必要に応じて）"], size=18, pitch=28)
A([[268, 378], [268, 422]], w=3)
R([64, 425, 410, 104], fill=CARD, r=8)
I("lucide:search", [96, 441, 62, 62], ICON, stroke_width=2.5)
I("material:database-fill", [138, 468, 38, 44], ICON)
T([206, 450, 250, 60], "構造化検索\n（N-PLUS／TOS）", 20, line_pitch_px=29)
A([[268, 531], [268, 556]], w=3)
R([64, 559, 410, 104], fill=CARD, r=8)
I("lucide:file-spreadsheet", [94, 576, 70, 70], ICON, stroke_width=1.8)
T([190, 582, 270, 60], "TOS検索単位 1行を取得\n（構造化データ）", 20, line_pitch_px=29)
A([[268, 665], [268, 705]], w=3)
R([42, 708, 444, 184], fill=GRAY, r=8, name="uc1-result")
T([58, 718, 300, 32], "結果提示（Dify の画面）", 19)
R([58, 752, 414, 124], r=6)
I("lucide:table", [80, 770, 64, 66], ICON, stroke_width=2)
bullets([186, 762, 290, 110], ["取得した1行の内容", "版情報・適用情報", "取得元（システム／テーブル等）", "根拠の表示"], size=17, pitch=27)

# connectors Dify -> columns
add(type="arrow", points=[[536, 352], [514, 352], [514, 622], [488, 622]], color=BLUE, width_px=3)
add(type="arrow", points=[[1136, 352], [1158, 352], [1158, 628], [1188, 628]], color=BLUE, width_px=3)

# UC2 column
R([1184, 210, 448, 160], fill=PANEL, r=8, name="uc2-input")
T([1200, 218, 400, 32], "ユーザー入力（自然言語の問い）", 19, color="#1F4E8C")
R([1198, 265, 78, 92], r=8)
I("material:person-fill", [1202, 274, 70, 72], "#123A6E")
R([1303, 265, 314, 88], line=L("#9DB5D2", 1.5), r=12)
T([1303, 272, 314, 74], "「この部品の過去の不具合事例と\n対応方法を教えてください」", 18, bold=False, align="c", line_pitch_px=27)
A([[1413, 372], [1413, 402]], w=3)
R([1195, 405, 437, 146], fill=CARD, r=8)
T([1195, 416, 437, 32], "見出し付きチャンクに対する検索", 19, align="c")
for x, ic, t1, t2 in [(1212, "lucide:search", "全文検索", "（BM25）"), (1422, "material:hub-fill", "ベクトル検索", "（意味的類似）")]:
    R([x, 458, 194, 78], r=6)
    I(ic, [x + 20, 472, 52, 52], ICON, **({"stroke_width": 2.5} if ic.startswith("lucide") else {}))
    add(type="text", box=[x + 72, 470, 122, 56], paras=[[{"text": t1, "bold": True}], [{"text": t2}]],
        size_px=16, color=INK, align="c", line_pitch_px=24)
A([[1413, 553], [1413, 580]], w=3)
R([1195, 584, 437, 104], fill=CARD, r=8)
I("lucide:list", [1218, 606, 60, 60], ICON, stroke_width=3)
T([1298, 594, 320, 30], "RRF による結果統合", 20)
T([1298, 626, 330, 54], "全文検索とベクトル検索の結果を\nRRF で統合し、関連度順にランキング", 17, bold=False, line_pitch_px=26)
A([[1413, 690], [1413, 718]], w=3)
R([1190, 722, 444, 184], fill=GRAY, r=8, name="uc2-result")
T([1206, 732, 300, 32], "結果提示（Dify の画面）", 19)
R([1204, 768, 414, 120], r=6)
I("lucide:file-text", [1220, 784, 62, 66], ICON, stroke_width=1.8)
bullets([1304, 776, 314, 110], ["関連する文書の一覧（タイトル・見出し）", "該当箇所の抜粋（ハイライト）", "取得元（ファイル名・パス 等）", "根拠箇所の表示"], size=16.5, pitch=26)

json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
