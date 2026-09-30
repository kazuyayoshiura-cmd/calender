import sys
sys.path.insert(0, "..")
from lib import *

s = Slide()
s.title("4.3  UC2：N-PLUS／TOS検索の処理フロー（図4-3）")
s.rect([24, 68, 1624, 62], fill="#F2F8FE", line={"color": "#9CC2E8", "width_px": 1.2}, r=4)
s.text([24, 70, 1624, 58], "UC2では、N-PLUSのTOSデータを対象に、「部品・工程を指定して検索」「類似作業工程を探索」「両者を併用した検索」の3つのパターンを実現する。\nいずれのパターンでも、構造化検索・全文検索・ベクトル検索を適切に組み合わせ、版・適用判定を行い、根拠付きで候補を提示する。",
       17, align="c", line_pitch_px=26, color=HEAD)

W = 536
XS = [24, 568, 1112]


def panel(x, title, desc):
    s.rect([x, 138, W, 786], fill="#FFFFFF", line={"color": NAVY, "width_px": 1.5})
    s.rect([x, 138, W, 44], fill=NAVY)
    s.text([x + 14, 138, W - 20, 44], title, 19.5, bold=True, color="#FFFFFF")
    s.text([x + 14, 186, W - 24, 50], desc, 15.5, line_pitch_px=23)


def user_input(x, example, h=112):
    s.icon("material:person-fill", [x + 10, 256, 32, 32])
    s.add(type="roundRect", box=[x + 46, 248, 150, h], radius_px=6, fill="#FFFFFF", line={"color": "#3A5F8F", "width_px": 1.5},
          paras=[[{"text": "質問入力", "size_px": 15.5, "bold": True, "color": HEAD}], [{"text": "例：", "size_px": 12.5}]] +
                [[{"text": t, "size_px": 12}] for t in example], color=SUB, align="l", valign="t", line_pitch_px=19, inset_px=[10, 6, 6, 4])
    s.arrow([[x + 196, 289], [x + 214, 289]])


def nplus(x, y):
    s.rect([x + 14, y, 172, 70], fill="#FFFFFF", line={"color": "#5B8FD0", "width_px": 1.5}, r=6)
    s.icon("material:database-fill", [x + 20, y + 13, 42, 44], "#2A5CA8")
    s.rich([x + 64, y + 4, 120, 62], [[{"text": "N-PLUS", "size_px": 13.5, "bold": True}], [{"text": "（TOS／Sequence／", "size_px": 11}], [{"text": "　MakeProcess 等）", "size_px": 11}]],
           color=SUB, line_pitch_px=18)


def not_found(x, y):
    s.node([x + 410, y, 120, 80], "該当なし", "（類似で埋めない）\n・入力キーの\n　再確認を依頼", kind="pink", tsize=15, ssize=11, pitch=16)


CX = 332  # spine center (panel-relative)

# ---------------- pattern 1
x = XS[0]
panel(x, "パターン1：部品・工程指定で検索（正確検索）", "部品番号や工程番号などの確定キーを指定し、\nN-PLUSのTOSを正確に検索する。")
user_input(x, ["「部品番号Aの工程", "100のTOSを確認", "したい」"])
s.node([x + 214, 248, 236, 82], "質問解釈", "（LLMでJSON抽出）\npart_no, process_no\nintent=tos_search", ssize=12.5, pitch=17, tsize=15)
s.node([x + 214, 350, 236, 66], "コード検証", None, bullets=["部品番号の実在チェック", "工程番号の実在チェック"], kind="yellow", ssize=13, pitch=19, tsize=15)
s.diamond([x + 270, 434, 124, 78], "キーは\nマスタに実在？", size=13)
not_found(x, 433)
s.node([x + 214, 532, 236, 98], "構造化検索", "（完全一致・フィルタ）\nSELECT … FROM TOS\nWHERE part_no=?\nAND process_no=?", ssize=12.5, pitch=17, tsize=15, kind="blue")
nplus(x, 546)
s.node([x + 214, 650, 236, 86], "版・適用判定", "（第6章のルール）", bullets=["最新版の特定", "適用範囲の確認"], kind="yellow", ssize=13, pitch=18, tsize=15)
s.node([x + 30, 758, 476, 150], "結果表示（取得データを直接表示）", None, bullets=["TOS基本情報", "関連シーケンス／工程一覧", "版・適用ラベル", "原本リンク（N-PLUS画面）"],
       kind="green", tsize=16, ssize=14, pitch=25, align="l")
for a, b in [(330, 350), (416, 434), (512, 532), (630, 650), (736, 758)]:
    s.arrow([[x + CX, a], [x + CX, b]])
s.label([x + CX + 8, 512, 80, 20], "存在する", 12.5)
s.arrow([[x + 394, 473], [x + 410, 473]])
s.label([x + 410, 412, 120, 20], "存在しない", 12, align="c")
s.arrow([[x + 270, 473], [x + 121, 473], [x + 121, 360]], dash="dash", w=1.4)
s.arrow([[x + 186, 581], [x + 214, 581]])

# ---------------- pattern 2
x = XS[1]
panel(x, "パターン2：類似作業工程探索（類似検索）", "作業内容などの自然言語から、過去に類似する作業工程で\n使われたTOSを探索する。")
user_input(x, ["「過去に類似工程で", "使われたTOSを", "探したい」"])
s.node([x + 214, 248, 236, 82], "質問解釈", "（LLMでJSON抽出）\nkeywords, free_text\nintent=similar_search", ssize=12.5, pitch=17, tsize=15)
s.node([x + 214, 350, 236, 70], "用語辞書で正規化・拡張", "（工程名、作業内容、略語 等）\n例：穴あけ ＝ 穴加工、ドリル 等", kind="yellow", ssize=12, pitch=17, tsize=15)
s.node([x + 214, 440, 236, 106], "ハイブリッド検索", None, bullets=["全文検索（BM25：kuromoji）", "ベクトル検索（工程文脈テキスト）", "RRF統合 ＋ 必須条件フィルタ", "（リランク：任意）"],
       kind="blue", ssize=12.5, pitch=19, tsize=15, align="l")
s.E[-1]["paras"][-1][0]["text"] = "　　（リランク：任意）"
nplus(x, 458)
s.node([x + 30, 578, 250, 90], "版・適用判定", "（第6章のルール）", bullets=["適用範囲の確認", "旧版・適用外の除外／警告"], kind="yellow", ssize=13, pitch=19, tsize=15)
s.node([x + 300, 570, 220, 112], "LLMで説明・比較生成", "（参照ID付き）", bullets=["作業内容の要約", "類似点／相違点", "適用上の注意 等"], ssize=12.5, pitch=19, tsize=14)
s.node([x + 30, 740, 490, 168], "結果表示（候補一覧＋比較）", None, bullets=["類似TOSの候補一覧（スコア順）", "主要項目の比較（作業内容・工程・工数 等）", "根拠／類似する点／未確認事項", "原本リンク（N-PLUS画面）"],
       kind="green", tsize=16, ssize=14, pitch=25, align="l")
s.arrow([[x + CX, 330], [x + CX, 350]])
s.arrow([[x + CX, 420], [x + CX, 440]])
s.arrow([[x + 186, 493], [x + 214, 493]])
s.arrow([[x + CX, 546], [x + CX, 560], [x + 155, 560], [x + 155, 578]])
s.arrow([[x + 280, 623], [x + 300, 623]])
s.arrow([[x + 155, 668], [x + 155, 740]])
s.arrow([[x + 410, 682], [x + 410, 740]])
s.arrow([[x + 121, 360], [x + 121, 450], [x + 214, 450]], dash="dash", w=1.4, head="both")

# ---------------- pattern 3
x = XS[2]
panel(x, "パターン3：部品・工程 ＋ 作業内容の併用検索", "部品番号や工程番号などの確定キーで検索範囲を絞り込み、\n作業内容の類似度を用いて関連するTOSを探索する。")
user_input(x, ["「部品番号Aで、溶接", "工程に近い過去の", "TOSを探したい」"])
s.node([x + 214, 248, 236, 82], "質問解釈", "（LLMでJSON抽出）\npart_no, keywords\nintent=hybrid_search", ssize=12.5, pitch=17, tsize=15)
s.node([x + 214, 350, 236, 66], "コード検証・正規化", None, bullets=["部品番号の実在チェック", "用語辞書で正規化・拡張"], kind="yellow", ssize=13, pitch=19, tsize=15)
s.diamond([x + 270, 434, 124, 78], "部品番号は\nマスタに実在？", size=12.5)
not_found(x, 433)
s.node([x + 214, 532, 236, 80], "構造化で絞り込み", "（部品番号で候補を限定）\nSELECT … WHERE part_no=?", ssize=12.5, pitch=18, tsize=15, kind="blue")
nplus(x, 537)
s.node([x + 30, 642, 250, 90], "全文 ＋ ベクトル検索", "（工程・作業内容の類似検索）\nRRF統合 ＋ 必須条件フィルタ", kind="blue", ssize=12.5, pitch=19, tsize=15)
s.node([x + 300, 632, 220, 112], "LLMで説明・比較生成", "（参照ID付き）", bullets=["類似工程の理由", "候補の比較", "適用上の注意 等"], ssize=12.5, pitch=19, tsize=14)
s.node([x + 30, 770, 490, 136], "結果表示（絞り込み後の候補一覧＋比較）", None, bullets=["候補一覧（類似度順）", "一致した条件／類似する点／未確認事項", "原本リンク（N-PLUS画面）"],
       kind="green", tsize=16, ssize=14, pitch=25, align="l")
for a, b in [(330, 350), (416, 434), (512, 532)]:
    s.arrow([[x + CX, a], [x + CX, b]])
s.label([x + CX + 8, 512, 80, 20], "存在する", 12.5)
s.arrow([[x + 394, 473], [x + 410, 473]])
s.label([x + 410, 412, 120, 20], "存在しない", 12, align="c")
s.arrow([[x + 270, 473], [x + 121, 473], [x + 121, 360]], dash="dash", w=1.4)
s.arrow([[x + 186, 572], [x + 214, 572]])
s.arrow([[x + CX, 612], [x + CX, 626], [x + 155, 626], [x + 155, 642]])
s.arrow([[x + 280, 687], [x + 300, 687]])
s.arrow([[x + 155, 732], [x + 155, 770]])
s.arrow([[x + 410, 744], [x + 410, 770]])
slide1 = s.E

# ---------------- slide 2: output images
o = Slide()
o.title("4.3  UC2：N-PLUS／TOS検索の出力イメージ（図4-3）")


def band(box, title):
    o.rect(box, fill="#FFFFFF", line={"color": NAVY, "width_px": 1.5})
    o.rect([box[0], box[1], box[2], 42], fill=NAVY)
    o.text([box[0] + 16, box[1], box[2] - 20, 42], title, 19, bold=True, color="#FFFFFF")


def sub_head(box, text):
    o.rect([box[0], box[1], 6, box[3]], fill=NAVY)
    o.text([box[0] + 14, box[1], box[2] - 14, box[3]], text, 17, bold=True, color=HEAD)


HDR = {"bold": True, "fill": "#E6EEF8", "color": HEAD}
band([24, 72, 1624, 318], "パターン1：部品・工程指定（取得データの直接表示）")
sub_head([44, 126, 600, 30], "TOS 基本情報")
o.add(type="table", box=[44, 162, 640, 216], col_widths_px=[150, 490], row_heights_px=[24] * 9,
      cells=[[{"text": k, "bold": True, "color": HEAD, "fill": "#F3F6FA"}, {"text": v, **({"color": "#1F5FD0"} if k == "原本リンク" else {})}]
             for k, v in [("LTS", "LTS-000123"), ("TOS", "TOS-456789"), ("部品番号", "A123-45678"), ("工程番号", "100"), ("作業内容", "穴あけ加工"),
                          ("ステータス", "有効"), ("版", "Rev.3（2024/10/01）"), ("適用範囲", "S/N 001～100"), ("原本リンク", "N-PLUSで開く")]],
      size_px=14, align="l", color=INK, border={"color": "#DDE5EF", "width_px": 1}, cell_pad_px=10)
sub_head([724, 126, 900, 30], "関連シーケンス／工程一覧")
o.add(type="table", box=[724, 162, 900, 150], col_widths_px=[110, 200, 400, 190], row_heights_px=[30] * 5,
      cells=[[dict(text=t, **HDR) for t in ["Seq", "工程番号", "作業内容", "工数(h)"]],
             ["1", "100", {"text": "穴あけ加工", "align": "l"}, "2.0"], ["1", "110", {"text": "面取り", "align": "l"}, "0.5"],
             ["1", "120", {"text": "検査", "align": "l"}, "0.3"], ["…", "", "", ""]],
      size_px=15, align="c", color=INK, border={"color": "#C9D6E6", "width_px": 1}, cell_pad_px=8)


def cand_panel(x, title, table_title, rows, notes):
    band([x, 404, 806, 520], title)
    sub_head([x + 20, 458, 766, 30], table_title)
    o.add(type="table", box=[x + 20, 494, 766, 176], col_widths_px=[50, 124, 90, 212, 86, 90, 114], row_heights_px=[36, 35, 35, 35, 35],
          cells=[[dict(text=t, **HDR) for t in ["No.", "部品番号" if rows[0][1][0] != "T" else "TOS", "工程番号", "作業内容（要約）", "類似度", "版", "適用範囲"]]] +
                [[str(i + 1), r[0 if False else 1], r[2], {"text": r[3], "align": "l"}, r[4], r[5], r[6]] for i, r in enumerate(rows)] + [["…", "", "", "", "", "", ""]],
          size_px=14.5, align="c", color=INK, border={"color": "#C9D6E6", "width_px": 1}, cell_pad_px=6)
    sub_head([x + 20, 694, 766, 30], "LLMによる比較説明（抜粋）")
    o.add(type="text", box=[x + 28, 732, 750, 180], text="\n".join(notes), size_px=15, color=INK, valign="t", bullet=True,
          line_pitch_px=23, para_space_px=6, bullet_indent_px=20)


cand_panel(24, "パターン2：類似作業工程探索（候補一覧＋比較）", "類似 TOS 候補一覧",
           [(None, "B987-65432", "100", "穴あけ加工（治具使用）", "0.92", "Rev.2", "001～"), (None, "A123-45678", "120", "穴明け・リーマ", "0.87", "Rev.3", "001～"),
            (None, "C111-22222", "100", "穴あけ加工", "0.82", "Rev.1", "050～")],
           ["No.1は治具を使用した穴あけ加工で、工程条件が近似しています。\v（参照：TOS-xxxxx）", "No.2は同一部品の類似工程で、作業手順が参考になります。\v（参照：TOS-xxxxx）",
            "No.3は材質が異なるため、適用可否の確認が必要です。\v（参照：TOS-xxxxx）"])
cand_panel(842, "パターン3：部品・工程＋作業内容（絞り込み後の候補一覧＋比較）", "絞り込み後の類似 TOS 候補",
           [(None, "TOS-456789", "200", "溶接（TIG）", "0.95", "Rev.3", "001～"), (None, "TOS-123456", "210", "溶接（スポット）", "0.88", "Rev.2", "001～"),
            (None, "TOS-789012", "200", "溶接（TIG・治具）", "0.83", "Rev.1", "050～")],
           ["No.1は同一部品番号で溶接工程の作業条件が最も近いです。\v（参照：TOS-xxxxx）", "No.2は工程番号が異なりますが、作業内容が類似しています。\v（参照：TOS-xxxxx）",
            "治具の有無や適用範囲が異なるため、適用可否の確認が必要です。"])

Slide().dump(slides=[{"background": "#FFFFFF", "elements": slide1}, {"background": "#FFFFFF", "elements": o.E}])
