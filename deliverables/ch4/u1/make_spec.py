import sys
sys.path.insert(0, "..")
from lib import *

s = Slide()
s.title("4.  ユースケースごとの検索・回答までの処理フロー")
# section header + frame
s.rect([24, 110, 1624, 800], fill="#FFFFFF", line={"color": NAVY, "width_px": 1.5})
s.rect([24, 66, 1624, 44], fill=NAVY)
s.rich([40, 66, 1600, 44], [[{"text": "4.1  共通処理フロー（図4-1）", "size_px": 23, "bold": True},
                            {"text": "　　質問解釈 → ルーティング → 検索 → 版・適用確認 → 根拠組立 → 表示", "size_px": 20}]], color="#FFFFFF")
# lanes
for x, w, t, f in [(34, 352, "Dify（UI / ワークフロー）", "#CFE2F7"), (392, 1030, "検索API / アプリケーション（業務ロジック）", "#B5D3F2"),
                   (1428, 210, "データストア", "#CFE2F7")]:
    s.rect([x, 120, w, 34], fill=f, text=t, size_px=17, bold=True, color=HEAD)
for x in (389, 1425):
    s.line([[x, 160], [x, 896]], w=1, color="#C9D6E6", dash="dash")

# row A (center y 226)
s.icon("material:person-fill", [38, 204, 44, 44])
s.node([88, 192, 150, 68], "質問入力", "（自然言語）")
s.node([256, 180, 128, 92], "検索API", "/interpret\n（構造化抽出依頼）", ssize=13, tsize=16)
s.node([406, 160, 162, 132], "LLMでJSON抽出", "（所定スキーマ）", align="c", tsize=16, ssize=13.5, pitch=19)
s.E[-1]["paras"] += [[{"text": t, "size_px": 12.5, "color": SUB}] for t in ["target_system, intent,", "part_no, process_no,", "doc_no, rev, keywords,", "free_text"]]
s.node([590, 166, 186, 120], "キーの実在チェック", None, align="l", tsize=16, ssize=12.5, pitch=21,
       bullets=["用語辞書で正規化", "（L/C → ロードセンター等）", "同名異義語の文脈判定", "マスタ存在確認"])
s.E[-1]["paras"][2][0]["text"] = "　（L/C → ロードセンター等）"
s.diamond([800, 178, 120, 96], "キーは\nマスタに実在？", size=14)
s.node([1100, 192, 150, 68], "該当なし", "（類似で埋めない）", kind="pink")
s.arrow([[238, 226], [256, 226]])
s.arrow([[384, 226], [406, 226]])
s.arrow([[568, 226], [590, 226]])
s.arrow([[776, 226], [800, 226]])
s.arrow([[920, 226], [1100, 226]])
s.label([940, 198, 120, 24], "存在しない", 14)

# 追加確認 (Dify lane)
s.node([200, 318, 172, 64], "追加確認の質問", "（意図不明・同名異義語等）", kind="dash", tsize=15, ssize=12.5)
s.arrow([[317, 272], [317, 318]], dash="dash", w=1.6)
s.arrow([[200, 350], [163, 350], [163, 260]], dash="dash", w=1.6)

# row B: rules + routing
s.rect([406, 300, 360, 110], fill="#FFFFFF", line={"color": "#9DB5D2", "width_px": 1.2}, r=4)
s.text([418, 304, 340, 24], "ルーティング規則（優先順）", 15, bold=True, color=HEAD)
for i, t in enumerate(["確定キーのみ → 構造化検索", "確定キー＋自然言語 → 構造化で絞ってから全文＋ベクトル", "自然言語のみ → 全文＋ベクトルのハイブリッド", "意図不明 → 追加確認の質問（Dify）"]):
    y = 330 + i * 19.5
    s.add(type="ellipse", box=[420, y + 2, 15, 15], fill="#7FA3CF", line=None, text=str(i + 1), size_px=10, bold=True, color="#FFFFFF")
    s.text([440, y, 322, 19], t, 11.8)
s.node([790, 318, 140, 68], "ルーティング判定", "（優先順の4規則）", tsize=16, ssize=13.5)
s.arrow([[860, 274], [860, 318]])
s.label([868, 284, 130, 24], "存在 / キーなし", 14)
s.line([[790, 352], [766, 352]], w=1.5, dash="dash")

# datastore
s.rect([1438, 166, 190, 214], fill="#FFFFFF", line={"color": "#7FA3CF", "width_px": 1.2, "dash": "dash"}, r=6)
for y, ic, t1, t2 in [(178, "material:database-fill", "N-PLUS", "（TOS / 他テーブル）"), (244, "material:description-fill", "ファイルサーバー", "（JP / 作業標準 等）"),
                      (310, "lucide:database", "マスタ・辞書", "（部品 / 工程 / 用語）")]:
    s.icon(ic, [1446, y + 4, 42, 42], NAVY, **({"stroke_width": 2.2} if ic.startswith("lucide") else {}))
    s.rich([1494, y, 134, 56], [[{"text": t1, "size_px": 14, "bold": True}], [{"text": t2, "size_px": 12}]], color=SUB, line_pitch_px=21)
s.line([[930, 352], [1438, 352]], w=1.5, dash="dash", color="#7FA3CF")

# row C: search trio -> RRF
s.line([[860, 386], [860, 414]])
s.line([[495, 414], [808, 414]])
for x in (495, 654, 808):
    s.arrow([[x, 414], [x, 440]])
s.node([420, 440, 150, 110], "構造化検索", "（完全一致・フィルタ）", tsize=16, ssize=13, pitch=19)
s.E[-1]["paras"] += [[{"text": t, "size_px": 12.5, "color": SUB}] for t in ["SELECT … WHERE", "部品番号=? AND", "工程番号=?"]]
s.node([584, 440, 140, 110], "全文検索", "（BM25・kuromoji）\n辞書展開語を OR", tsize=16, ssize=13, pitch=22)
s.node([738, 440, 140, 110], "ベクトル検索", "（Embedding近傍）\n文脈化テキスト", tsize=16, ssize=13, pitch=22)
for x in (495, 654, 808):
    s.arrow([[x, 550], [x, 592]])
s.node([420, 592, 458, 78], "RRF統合 ＋必須条件フィルタ", "（リランク：任意）", tsize=17, ssize=14)

# 版・適用 -> 根拠 -> 保留条件
s.node([910, 470, 160, 80], "版・適用判定", "（第6章のルール）")
s.arrow([[920, 386], [920, 470]])  # routing -> 版・適用 (bypass for structured-only)
s.arrow([[878, 631], [990, 631], [990, 550]])
s.node([1100, 470, 150, 80], "根拠アセンブリ", "（source_ref付与\n原本リンク生成）", tsize=16, ssize=13, pitch=19)
s.arrow([[1070, 510], [1100, 510]])
s.arrow([[1175, 260], [1175, 470]])  # 該当なし -> 根拠
s.diamond([1276, 466, 108, 88], "保留条件？", size=14)
s.arrow([[1250, 510], [1276, 510]])
s.node([1450, 476, 172, 70], "保留", "（未確認事項＋\n次に確認すること）", kind="pink", ssize=13, pitch=18)
s.arrow([[1384, 510], [1450, 510]])
s.label([1330, 446, 240, 22], "根拠不足／矛盾／版不明", 13.5, align="r")

# output type
s.arrow([[1330, 554], [1330, 590]])
s.label([1338, 558, 90, 22], "問題なし", 14)
s.node([1250, 590, 160, 44], "出力種別の判定", None, tsize=16)
s.arrow([[1250, 612], [1055, 612], [1055, 680]])
s.label([1062, 586, 186, 22], "構造化結果（データそのまま）", 13, align="r")
s.arrow([[1410, 612], [1535, 612], [1535, 680]])
s.label([1418, 586, 110, 22], "説明／比較", 13.5)
s.node([930, 680, 250, 64], "取得データを直接表示", "（テーブル・一覧）", kind="green")
s.node([1440, 680, 184, 64], "LLMに根拠を渡して生成", "（参照ID必須）", kind="blue", tsize=15)
s.node([420, 790, 1180, 76], "候補一覧／根拠／版・適用ラベル／原本リンク の表示", "＋ ログ記録（F-07）", kind="final", tsize=19, ssize=17)
s.E[-1]["paras"][1][0].update(bold=True, color=HEAD)
for x in (1055, 1535):
    s.arrow([[x, 744], [x, 790]])
s.arrow([[1330, 634], [1330, 790]])
s.arrow([[1622, 511], [1636, 511], [1636, 828], [1600, 828]])

s.dump()
