import json
NAVY = "#1B3F72"; INK = "#1F2F4F"; HEAD = "#1F3A6E"; LINE = "#D0DBE8"; CARD = "#EBF5FE"; LBL = "#DDEBF8"; GRAYA = "#7A8BA0"
E = []
def add(**k): E.append(k); return k
def T(box, text, size, bold=False, color=INK, align="l", valign="m", **k):
    return add(type="text", box=box, text=text, size_px=size, bold=bold, color=color, align=align, valign=valign, **k)
def R(box, fill="#FFFFFF", line=None, r=None, **k):
    d = dict(type="roundRect" if r is not None else "rect", box=box, fill=fill, line=line, **k)
    if r is not None: d["radius_px"] = r
    return add(**d)
def L(c, w=1.2): return {"color": c, "width_px": w}
def BUL(box, items, size=17, pitch=25, space=0, **k):
    return add(type="text", box=box, text="\n".join(items), size_px=size, color=INK, valign="t", bullet=True,
               line_pitch_px=pitch, para_space_px=space, bullet_indent_px=20, **k)
def num(cx, cy, n, d=40, size=22):
    add(type="ellipse", box=[cx - d / 2, cy - d / 2, d, d], fill=NAVY, line=None, text=n, size_px=size, bold=True, color="#FFFFFF")
def down(x, y, w=26, h=20):
    add(type="downArrow", box=[x, y, w, h], fill=GRAYA, line=None)

# title
R([0, 16, 14, 80], fill="#294D78")
T([40, 8, 760, 62], "Gate 1で何を見極めるか", 48, bold=True, color=HEAD)
T([42, 64, 700, 38], "実データで検索成立性を確認する", 28, color=HEAD)
add(type="image", path="logo.png", box=[1552, 16, 100, 32], name="logo")
R([30, 117, 1615, 79], fill="#E7F3FD")
R([42, 123, 172, 64], fill="#0D3B71", text="キーメッセージ", size_px=19, bold=True, color="#FFFFFF")
T([238, 124, 1400, 64], "代表的な業務質問から必要な情報・元データ・結合キーを逆算し、実データで「正しく検索・回答できる状態を作れるか」を確認する。\n不足や矛盾がある場合は、補正・対象制限で成立するのか、PoCの前提自体を見直す必要があるのかまで判断する。",
  20, line_pitch_px=30)

# ---- left: 5 viewpoints
R([30, 258, 678, 648], fill="#FFFFFF", line=L("#D6E0EC"))
R([30, 214, 678, 44], fill=NAVY)
T([52, 214, 640, 44], "①  Gate 1で見る5つの観点", 24, bold=True, color="#FFFFFF")
R([44, 272, 646, 462], fill="#FFFFFF", line=L("#C9D6E6"), r=4)
R([46, 272, 158, 32], fill="#3E6FA8", r=3, text="1～4：成立条件", size_px=16, bold=True, color="#FFFFFF")
cards = [(306, 92, "1", "必要情報の充足性", ["回答に必要な情報が実データ内に存在するか", "例：作業工程、部品、WPS、文書、REV、発効日、FROM/THRU"]),
         (410, 94, "2", "関係性・結合の成立性", ["正しいキー・条件・粒度で紐付けられるか", "例：部品⇔工程⇔WPS⇔図面、JOIN重複、部品番号だけで足りるか"]),
         (518, 96, "3", "版・適用の判定可能性", ["最新版・適用対象を判断できるか", "例：REV、発効日、号機、適用/非適用/判定不能"]),
         (626, 96, "4", "抽出・トレーサビリティの成立性", ["文書から正しく抽出し、原本へ戻れるか", "例：見出し、ページ、シート/セル、文書番号、元ファイルパス"])]
for y, h, n, title, items in cards:
    R([52, y, 628, h], fill=CARD, r=2)
    num(82, y + 30, n)
    T([126, y + 6, 540, 34], title, 21, bold=True, color=HEAD)
    BUL([122, y + 38, 556, 54], items, size=16.5, pitch=25)
down(334, 732, 38, 30)
R([44, 758, 646, 146], fill="#FFFFFF", line=L("#C9D6E6"), r=4)
R([46, 758, 134, 30], fill="#3E6FA8", r=3, text="5：総合確認", size_px=16, bold=True, color="#FFFFFF")
R([52, 788, 628, 108], fill=CARD, r=2)
num(82, 818, "5")
T([124, 796, 540, 32], "検索単位として成立するか", 21, bold=True, color=HEAD)
T([124, 828, 560, 66], "①～④を満たしたうえで、1件だけを見れば「何についての、\vどの工程で、何をする情報で、どの版・対象に使えるか」が分かり、\vかつ元データまで辿れるか。", 17,
  valign="t", line_pitch_px=23)

# ---- right: how to proceed
R([726, 258, 919, 648], fill="#FFFFFF", line=L("#D6E0EC"))
R([726, 214, 919, 44], fill=NAVY)
T([748, 214, 880, 44], "②  Gate 1をどう進めるか", 24, bold=True, color="#FFFFFF")
steps = [(275, 268, 92), (386, 384, 88), (500, 498, 142), (670, 668, 74), (767, 765, 132)]
for i, (ly, cy, ch) in enumerate(steps):
    R([746, ly, 108, 48], fill=LBL, r=2, text=f"STEP {i + 1}", size_px=19, bold=True, color=HEAD)
    R([862, cy, 768, ch], fill="#FFFFFF", line=L(LINE), r=3)
for y in (363, 474, 642, 744):
    down(1161, y)
# step1
T([876, 274, 420, 34], "代表質問を選ぶ", 22, bold=True, color=HEAD)
T([876, 308, 420, 30], "UC1・UC2から20～30問程度を先行選定", 18)
R([1306, 272, 316, 84], fill="#F0F4F9", r=3)
T([1322, 274, 100, 22], "（例）", 16)
BUL([1326, 294, 290, 60], ["部品AのTOSを確認したい", "類似工程を探したい", "該当箇所と最新版を確認したい"], size=15, pitch=20)
# step2
T([876, 389, 420, 34], "必要データを逆算する", 22, bold=True, color=HEAD)
T([876, 423, 440, 30], "必要情報 → 元データ → 結合キー → 検索単位", 18)
R([1306, 388, 316, 80], fill="#F0F4F9", r=3)
T([1322, 394, 100, 24], "（例）", 16)
T([1316, 418, 304, 46], "部品AのTOS → 作業内容・工程・WPS・履歴\n→ 作業工程/部品/WPS/履歴 → TOS検索単位", 13.5, line_pitch_px=22)
# step3
T([876, 503, 440, 34], "実データで成立条件を確認する", 22, bold=True, color=HEAD)
T([1330, 506, 284, 28], "※左の①～④をここで確認", 16, color="#1F5FB8", align="r")
def flow(x0, w, title, seq):
    R([x0, 541, w, 32], fill=LBL, text=title, size_px=17, bold=True, color=HEAD)
    R([x0, 573, w, 58], fill="#FFFFFF", line=L(LINE))
    x = x0 + 14
    for j, (n, label, lw) in enumerate(seq):
        num(x + 13, 601, n, d=26, size=15)
        T([x + 30, 588, lw, 26], label, 15)
        x += 30 + lw
        if j < len(seq) - 1:
            add(type="arrow", points=[[x + 2, 601], [x + 18, 601]], color="#4A5C78", width_px=1.4, head_size="sm")
            x += 24
flow(874, 360, "N-PLUS", [("1", "必要情報", 70), ("2", "紐付け", 56), ("3", "版・適用", 70)])
flow(1246, 376, "共有文書", [("1", "必要情報", 70), ("4", "抽出・追跡", 84), ("3", "版・適用", 70)])
# step4
T([876, 672, 480, 34], "検索単位として成立するか確認する", 22, bold=True, color=HEAD)
T([1350, 675, 264, 28], "※左の⑤をここで確認", 16, color="#1F5FB8", align="r")
T([872, 706, 756, 28], "・必要な文脈が揃うか  ／  根拠が揃うか  ／  元データまで辿れるか  ／  欠損を無理に補完していないか", 16)
# step5
T([874, 768, 200, 32], "判定", 22, bold=True, color=HEAD)
for x, w, hfill, hcolor, bfill, title, body in [(874, 238, "#D6EFE2", "#1E7A4A", "#F7FBF9", "成立", "必要情報が存在し、\n結合キーで根拠まで到達できる"),
                                              (1126, 246, "#FDF0D5", "#8A6212", "#FFFCF6", "条件付き成立", "補正・除外・追加提供・\n対象制限で評価可能"),
                                              (1384, 238, "#FBE1E5", "#A03040", "#FFF8F9", "不成立", "必須情報がなく、\n要求自体を評価できない")]:
    R([x, 802, w, 86], fill=bfill, line=L("#E3E7EC"))
    R([x, 802, w, 32], fill=hfill, text=title, size_px=18, bold=True, color=hcolor)
    T([x, 836, w, 50], body, 15.5, align="c", line_pitch_px=23)

# footer
R([30, 912, 1568, 26], fill="#EEF2F7")
T([42, 912, 1540, 26], "補足：診断後は、元データ欠損・矛盾などの「データ起因」と、抽出・結合・検索・生成などの「方式起因」を切り分け、改善対象を特定する。", 15.5)
T([1604, 912, 40, 26], "8", 14, color="#6B7385", align="r")

json.dump({"source_size": [1672, 941], "font": "Meiryo", "background": "#FFFFFF", "elements": E},
          open("spec.json", "w"), ensure_ascii=False, indent=1)
print(len(E), "elements")
