import sys
sys.path.insert(0, "..")
from lib import *

LANE = "#D6E6F7"


def panel(s, x, title, example, desc):
    s.rect([x, 138, 806, 790], fill="#FFFFFF", line={"color": NAVY, "width_px": 1.5})
    s.rect([x, 138, 806, 44], fill=NAVY)
    s.text([x + 14, 138, 530, 44], title, 19.5, bold=True, color="#FFFFFF")
    s.rect([x + 548, 145, 250, 30], fill="#FFFFFF", r=3, text=example, size_px=12, color=HEAD)
    s.text([x + 16, 186, 780, 50], desc, 16, line_pitch_px=24)


def lanes(s, x, names):
    xs = [x + 10, x + 156, x + 482, x + 648, x + 796]
    for (a, b), n in zip(zip(xs, xs[1:]), names):
        s.rect([a, 240, b - a - 4, 40], fill=LANE, paras=[[{"text": t, "size_px": 15 if i == 0 else 12.5, "bold": True}] for i, t in enumerate(n.split("\n"))],
               color=HEAD, align="c", line_pitch_px=18)
    for a in xs[1:-1]:
        s.line([[a - 2, 286], [a - 2, 924]], w=1, color="#C9D6E6", dash="dash")


def user_input(s, x, box, example):
    s.icon("material:person-fill", [box[0] + box[2] / 2 - 16, box[1] - 36, 32, 32])
    s.add(type="roundRect", box=box, radius_px=6, fill="#FFFFFF", line={"color": "#3A5F8F", "width_px": 1.5},
          paras=[[{"text": "質問入力", "size_px": 16, "bold": True, "color": HEAD}], [{"text": "例：", "size_px": 13}]] +
                [[{"text": t, "size_px": 12}] for t in example], color=SUB, align="l", valign="t", line_pitch_px=19, inset_px=[10, 6, 6, 4])


def store(s, box, doc_title, doc_sub):
    s.rect(box, fill="#FFFFFF", line={"color": "#5B8FD0", "width_px": 1.5}, r=6)
    x, y = box[0], box[1]
    s.icon("material:database-fill", [x + 8, y + 10, 36, 36], "#2A5CA8")
    s.rich([x + 48, y + 6, box[2] - 52, 46], [[{"text": "ファイルサーバー", "size_px": 12.5, "bold": True}], [{"text": "（JP / 作業標準 等）", "size_px": 11}]], color=SUB, line_pitch_px=19)
    s.icon("material:description-fill", [x + 8, y + 70, 36, 40], "#2A5CA8")
    s.rich([x + 48, y + 62, box[2] - 52, 70], [[{"text": doc_title, "size_px": 12.5, "bold": True}]] + [[{"text": t, "size_px": 11}] for t in doc_sub],
           color=SUB, line_pitch_px=18, valign="t")


# ------------------------------------------------------------------ slide 1: workflows
s = Slide()
s.title("4.2  UC1：共有ファイル／JP等検索の処理フロー（図4-2）")
s.rect([24, 68, 1624, 62], fill="#F2F8FE", line={"color": "#9CC2E8", "width_px": 1.2}, r=4)
s.text([24, 70, 1624, 58], "UC1では、社内のファイルサーバーに格納された作業標準（JP）等のドキュメントを対象に、\n「文書番号で指定して探す」または「作業内容から関連する標準を探す」の2パターンの検索フローを実現する。",
       18, align="c", line_pitch_px=26, color=HEAD)

# pattern 1
X = 24
panel(s, X, "パターン1：文書番号指定で検索（正確検索）", "例：「作業標準JP-123の最新版を教えて」",
      "文書番号（JP番号等）が明示されている場合は、構造化検索により該当文書を特定し、\n最新版・適用範囲を確認して提示する。")
lanes(s, X, ["ユーザー\n（Dify）", "検索API / アプリケーション", "データストア\n（ファイルサーバー）", "LLM\n（説明生成：任意）"])
CX = X + 319  # api lane center
user_input(s, X, [X + 18, 326, 128, 110], ["「作業標準JP-123の", "最新版を教えて」"])
s.node([CX - 110, 292, 220, 76], "質問解釈", "（LLMでJSON抽出）\ndoc_no=JP-123\nintent=doc_search", ssize=12.5, pitch=17, tsize=15)
s.arrow([[X + 146, 350], [CX - 110, 350]])
s.node([CX - 110, 388, 220, 60], "文書番号の検証", "（マスタ／ファイル一覧で実在チェック）", kind="yellow", ssize=12, tsize=15)
s.arrow([[CX, 368], [CX, 388]])
s.diamond([CX - 76, 468, 152, 74], "文書番号は\n実在する？", size=13.5)
s.arrow([[CX, 448], [CX, 468]])
s.node([X + 500, 473, 290, 64], "該当なし（類似で埋めない）", "・入力キーの再確認依頼", kind="pink", tsize=15, ssize=13)
s.arrow([[CX + 76, 505], [X + 500, 505]])
s.label([CX + 84, 480, 90, 22], "存在しない", 13)
s.node([CX - 110, 562, 220, 80], "構造化検索", "（完全一致・フィルタ）\nSELECT … WHERE JP番号=?", ssize=12.5, pitch=19, tsize=15)
s.arrow([[CX, 542], [CX, 562]])
s.label([CX + 8, 542, 90, 20], "存在する", 13)
store(s, [X + 488, 560, 156, 170], "該当文書の取得", ["（最新版・版履歴・", "　適用範囲）"])
s.arrow([[CX + 110, 602], [X + 488, 602]])
s.node([CX - 110, 662, 220, 80], "版・適用判定", "（第6章のルール）", bullets=["最新版の特定", "適用範囲の確認"], kind="yellow", ssize=12.5, pitch=17, tsize=15)
s.arrow([[CX, 642], [CX, 662]])
s.arrow([[X + 488, 702], [CX + 110, 702]])
s.node([CX - 110, 762, 220, 54], "結果整形", "（該当文書情報・原本リンク）", ssize=12.5, tsize=15)
s.arrow([[CX, 742], [CX, 762]])
s.node([X + 656, 740, 140, 100], "要約生成（任意）", "（参照ID付き）", bullets=["文書の概要説明", "改訂ポイント 等"], kind="dash", tsize=14, ssize=12, pitch=18, align="l")
s.arrow([[CX + 110, 789], [X + 656, 789]], dash="dash", w=1.6)
s.label([CX + 150, 766, 60, 20], "（任意）", 12.5)
s.node([X + 50, 838, 420, 82], "結果表示", None, bullets=["文書情報（最新版・版履歴・適用範囲）", "原本リンク", "必要に応じて要約（任意）"], kind="green", tsize=15, ssize=13, pitch=19, align="l")
s.arrow([[CX, 816], [CX, 838]])
s.arrow([[X + 726, 840], [X + 726, 879], [X + 470, 879]], dash="dash", w=1.6)
s.arrow([[X + 82, 436], [X + 82, 602], [CX - 110, 602]], dash="dash", w=1.4, head="both")

# pattern 2
X = 842
panel(s, X, "パターン2：作業内容から関連標準を探す（類似検索）", "例：「設計変更に関するJP作業標準は？」",
      "作業内容などの自然言語から、全文検索＋ベクトル検索のハイブリッド方式で関連する作業標準を\n検索し、候補を提示する。")
lanes(s, X, ["ユーザー\n（Dify）", "検索API / アプリケーション", "データストア\n（ファイルサーバー）", "LLM\n（説明生成・比較）"])
CX = X + 319
user_input(s, X, [X + 18, 326, 128, 128], ["「設計変更に関して", "指示しているJP", "作業標準の項番を", "教えて」"])
s.node([CX - 110, 292, 220, 86], "質問解釈", "（LLMでJSON抽出）\nintent=doc_search\nkeywords=設計変更, 指示\nfree_text=…", ssize=12.5, pitch=16.5, tsize=15)
s.arrow([[X + 146, 355], [CX - 110, 355]])
s.node([CX - 110, 398, 220, 66], "キーワードの正規化・拡張", "（辞書展開・同義語含む）\n例：設計変更 → 変更管理, DCCB 等", kind="yellow", ssize=11.5, pitch=16.5, tsize=14.5)
s.arrow([[CX, 378], [CX, 398]])
s.node([CX - 120, 484, 240, 108], "ハイブリッド検索", None, bullets=["全文検索（BM25：kuromoji）", "ベクトル検索（文脈化テキスト）", "RRF統合 ＋ 必須条件フィルタ", "（リランク：任意）"],
       kind="blue", ssize=12.5, pitch=19, tsize=15, align="l")
s.E[-1]["paras"][-1][0]["text"] = "　　（リランク：任意）"
s.arrow([[CX, 464], [CX, 484]])
store(s, [X + 488, 484, 156, 150], "関連文書の取得", ["（本文・該当箇所・", "　版情報）"])
s.arrow([[CX + 120, 538], [X + 488, 538]])
s.node([CX - 110, 612, 220, 84], "版・適用判定", "（第6章のルール）", bullets=["適用範囲の確認", "旧版・適用外の除外/警告"], kind="yellow", ssize=12.5, pitch=18, tsize=15)
s.arrow([[CX, 592], [CX, 612]])
s.arrow([[X + 488, 624], [CX + 110, 624]])
s.node([CX - 120, 716, 240, 58], "結果整形", "（候補一覧・一致/類似/未確認の区分）", ssize=12, tsize=15)
s.arrow([[CX, 696], [CX, 716]])
s.node([X + 656, 690, 140, 128], "LLMで説明・比較生成", "（参照ID付き）", bullets=["候補の要約", "共通点／相違点", "適用上の注意 等"], tsize=12.5, ssize=12, pitch=19)
s.arrow([[CX + 120, 745], [X + 656, 745]])
s.node([X + 50, 838, 570, 82], "結果表示", None, bullets=["候補一覧（関連度順）", "一致した条件／類似する点／未確認事項", "原本リンク・版情報・適用ラベル"], kind="green", tsize=15, ssize=13, pitch=19, align="l")
s.arrow([[CX, 774], [CX, 838]])
s.arrow([[X + 726, 818], [X + 726, 879], [X + 620, 879]], dash="dash", w=1.6)
s.arrow([[X + 82, 454], [X + 82, 538], [CX - 120, 538]], dash="dash", w=1.4, head="both")
slide1 = s.E

# ------------------------------------------------------------------ slide 2: output images
o = Slide()
o.title("4.2  UC1：共有ファイル／JP等検索の出力イメージ（図4-2）")


def out_panel(x, title):
    o.rect([x, 76, 806, 846], fill="#FFFFFF", line={"color": NAVY, "width_px": 1.5})
    o.rect([x, 76, 806, 50], fill=NAVY)
    o.icon("material:description-fill", [x + 14, 83, 34, 36], "#FFFFFF")
    o.text([x + 56, 76, 740, 50], title, 21, bold=True, color="#FFFFFF")


def sub_head(box, text):
    o.rect([box[0], box[1], 6, box[3]], fill=NAVY)
    o.text([box[0] + 16, box[1], box[2] - 16, box[3]], text, 19, bold=True, color=HEAD)


X = 24
out_panel(X, "出力イメージ（パターン1：文書番号指定）")
o.rect([X + 24, 150, 758, 340], fill="#F7FAFD", line={"color": "#C9D6E6", "width_px": 1.2}, r=6)
o.rect([X + 24, 150, 8, 340], fill=NAVY)
o.text([X + 52, 170, 300, 40], "作業標準 JP-123", 26, bold=True, color=HEAD)
o.rect([X + 290, 176, 96, 30], fill="#2E9E4F", r=4, text="最新版", size_px=16, bold=True, color="#FFFFFF")
o.add(type="table", box=[X + 52, 230, 700, 220], col_widths_px=[160, 540], row_heights_px=[56] * 4,
      cells=[[{"text": k, "bold": True, "color": HEAD}, {"text": v, **({"color": "#1F5FD0"} if k == "原本リンク" else {})}]
             for k, v in [("版数", "Rev.3（2024/10/01）"), ("適用範囲", "○○工程（機種A/B）"), ("文書種別", "作業標準（JP）"), ("原本リンク", "JP-123_Rev3.pdf")]],
      size_px=19, align="l", color=INK, border={"color": "#DDE5EF", "width_px": 1}, cell_pad_px=14)
sub_head([X + 24, 552, 758, 36], "LLMによる要約（任意）")
o.rect([X + 24, 598, 758, 296], fill="#FFFFFF", line={"color": "#C9D6E6", "width_px": 1.2}, r=6)
o.text([X + 48, 618, 714, 130], "本作業標準は、○○工程における△△作業の手順を規定したものです。\vRev.3では、手順5の検査方法が変更されています。\v主な改訂点は以下のとおりです。",
       19, valign="t", line_pitch_px=34)
o.add(type="text", box=[X + 48, 752, 714, 100], text="…（参照：JP-123 Rev.3、P.3）\n…（参照：JP-123 Rev.3、P.5）", size_px=19, color=INK,
      valign="t", bullet=True, line_pitch_px=34, bullet_indent_px=24)

X = 842
out_panel(X, "出力イメージ（パターン2：作業内容から検索）")
sub_head([X + 24, 150, 758, 36], "候補一覧")
o.add(type="table", box=[X + 24, 196, 758, 280], col_widths_px=[56, 116, 236, 100, 100, 150], row_heights_px=[56] * 5,
      cells=[[{"text": t, "bold": True, "fill": "#E6EEF8", "color": HEAD} for t in ["No.", "文書番号", "文書名", "関連度", "版", "適用範囲"]],
             ["1", "JP-045", {"text": "設計変更時の作業手順", "align": "l"}, "0.92", "Rev.5", "機種A/B"],
             ["2", "JP-078", {"text": "DCCB対応手順", "align": "l"}, "0.85", "Rev.2", "全機種"],
             ["3", "JP-123", {"text": "変更指示書の作成手順", "align": "l"}, "0.78", "Rev.3", "機種A"],
             ["…", "…", "", "", "", ""]],
      size_px=18, align="c", color=INK, border={"color": "#C9D6E6", "width_px": 1}, cell_pad_px=8)
sub_head([X + 24, 508, 758, 36], "LLMによる説明・比較（抜粋）")
o.rect([X + 24, 554, 758, 340], fill="#FFFFFF", line={"color": "#C9D6E6", "width_px": 1.2}, r=6)
o.text([X + 48, 572, 714, 34], "上記のJPは、いずれも設計変更対応に関連する作業標準です。", 19, valign="t")
o.add(type="text", box=[X + 48, 620, 714, 270],
      text="JP-045：設計変更時の基本的な作業手順。\v（参照：JP-045 Rev.5, P.2）\nJP-078：DCCBに関する具体的な指示方法。\v（参照：JP-078 Rev.2, P.1）\nJP-123：変更指示書の作成手順。\v（参照：JP-123 Rev.3, P.4）",
      size_px=19, color=INK, valign="t", bullet=True, line_pitch_px=32, para_space_px=10, bullet_indent_px=24)

Slide().dump(slides=[{"background": "#FFFFFF", "elements": slide1}, {"background": "#FFFFFF", "elements": o.E}])
