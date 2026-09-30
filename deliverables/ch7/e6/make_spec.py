import sys
sys.path.insert(0, "../../ch6")
from common import *

s = Slide()
s.text([24, 4, 1640, 60], "図7-3　キャッシュ設計と無効化条件", 38, bold=True, color=HEAD)
s.text([24, 66, 1640, 66], "検索の高速化と負荷抑制のために、レイヤーごとにキャッシュを設ける。データ更新時は適切に無効化し、キャッシュ利用時でも\n版・適用は必ず再判定することで、誤った最新版・適用結果の提示を防ぐ。",
       21, bold=True, color=HEAD, line_pitch_px=32)

# ---- flow band
steps = [("① 質問解釈", "（IN）", "質問の意図・条件・\n検索対象を構造化"), ("② 検索", "（SQ / FT / VS）", "構造化・全文・ベクトル\n検索で候補を取得"),
         ("③ 版・適用判定", "（VA）", "REV・発効日・適用範囲\nに基づき判定"), ("④ 埋め込み生成", "（EMB）", "文書・質問の\nベクトル化"),
         ("⑤ 意味解析", "（任意）", "類似質問・意図クラスタ\nによる高速化"), ("⑥ 結果生成", "（EV）", "根拠付きの\n回答を生成")]
X0, SW = 150, 230
SX = [X0 + i * SW for i in range(6)]
for i, (t1, t2, d) in enumerate(steps):
    x = SX[i]
    s.add(type="homePlate" if i == 0 else "chevron", box=[x, 152, SW + 16, 58], point_px=18, fill="#0E3F82", line={"color": "#FFFFFF", "width_px": 3},
          paras=[[{"text": t1, "size_px": 17, "bold": True}], [{"text": t2, "size_px": 16, "bold": True}]], color="#FFFFFF", line_pitch_px=23, inset_px=[14, 0, 8, 0])
    s.rect([x + 10, 216, SW - 20, 58], fill="#EEF3F9", r=4, text=d, size_px=15.5, bold=True, color=INK, line_pitch_px=24)

# user / answer
s.rect([16, 202, 118, 178], fill="#E6F1FB", r=8)
s.icon("azure:users", [48, 226, 54, 58])
s.text([16, 292, 118, 60], "ユーザー\n質問", 18, bold=True, color=HEAD, align="c", line_pitch_px=28)
s.rect([1552, 202, 108, 178], fill="#E6F1FB", r=8)
s.icon("azure:file", [1580, 226, 52, 58])
s.text([1552, 292, 108, 60], "回答\n（根拠付き）", 17, bold=True, color=HEAD, align="c", line_pitch_px=28)

# cache boxes (under steps 1, 2, 4, 5)
CY, CH = 288, 138
caches = [(0, "質問解釈キャッシュ", None, ["質問文の正規化結果", "ルーティング結果", "検索条件（構造化）"]),
          (1, "検索結果キャッシュ", None, ["検索クエリ（構造化）", "各検索方式の上位候補", "リランキング結果"]),
          (3, "Embedding\vキャッシュ", None, ["テキストの埋め込みベクトル", "文書チャンクのベクトル"]),
          (4, "意味キャッシュ", "（オプション）", ["質問の意味クラスタ", "類似質問のマッピング"])]
CB = {}
for i, t, sub, items in caches:
    x, w = SX[i] + 4, SW - 8
    s.rect([x, CY, w, CH], fill="#DDEBF8", line={"color": "#9DBBE0", "width_px": 1.2}, r=6)
    s.icon("azure:cache-redis", [x + 10, CY + 10, 38, 38])
    if sub:
        s.rich([x + 52, CY + 6, w - 56, 48], [[{"text": t, "size_px": 17, "bold": True}], [{"text": sub, "size_px": 14, "bold": True}]], color="#1356B0", line_pitch_px=22)
    else:
        s.text([x + 52, CY + 6, w - 56, 48], t, 17 if len(t) < 12 else 16, line_pitch_px=22, bold=True, color="#1356B0")
    s.add(type="text", box=[x + 14, CY + 58, w - 20, CH - 64], text="\n".join(items), size_px=14.5, color=INK, valign="t", bullet=True, bullet_indent_px=14, line_pitch_px=23)
    CB[i] = (x, w)
# arrows
MY = CY + 34
s.arrow([[134, MY], [CB[0][0], MY]], w=2.5)
s.arrow([[CB[0][0] + CB[0][1], MY], [CB[1][0], MY]], w=2.5)
s.arrow([[CB[1][0] + CB[1][1], MY], [SX[2] + SW / 2, MY], [SX[2] + SW / 2, 276]], w=2.5)
s.arrow([[SX[2] + SW / 2 + 40, 276], [SX[2] + SW / 2 + 40, MY], [CB[3][0], MY]], w=2.5)
s.arrow([[CB[3][0] + CB[3][1], MY], [CB[4][0], MY]], w=2.5)
s.line([[CB[4][0] + CB[4][1], MY], [SX[5] + SW / 2, MY]], w=2.5)
s.arrow([[SX[5] + SW / 2, MY], [SX[5] + SW / 2, 276]], w=2.5)
s.arrow([[SX[5] + SW / 2, MY], [1552, MY]], w=2.5)

# ---- table
cols = [338, 330, 316, 332, 328]
rh = [40, 76, 82, 82, 76]
T0 = 440
H = lambda t: {"text": t, "fill": "#0E3F82", "color": "#FFFFFF", "bold": True, "size_px": 19, "align": "c"}
BUL = {"bullet": True, "bullet_indent_px": 16, "size_px": 15.5, "color": INK, "align": "l", "valign": "m", "line_pitch_px": 24, "inset_px": [20, 2, 4, 2]}
PL = {"size_px": 15.5, "color": INK, "align": "l", "valign": "m", "line_pitch_px": 24, "inset_px": [16, 2, 4, 2]}
rows = [("azure:language", "質問解釈キャッシュ", None, ["質問の正規化結果", "検索対象・意図・検索条件", "ルーティング結果"], "正規化質問文字列\n＋設定版（プロンプト）",
         ["設定版の変更", "用語辞書版の変更"], "同一質問の再利用で\nLLM呼び出しを削減"),
        ("azure:search", "検索結果キャッシュ", None, ["各検索方式の上位候補", "リランキング後の候補"], "構造化クエリ／検索語\n＋検索方式\n＋データ版（data_version）",
         ["データ版の更新", "検索設定版の変更", "インデックス再構築時"], "キャッシュヒット時も\n版・適用は必ず再判定する"),
        ("azure:cognitive-services", "Embeddingキャッシュ", None, ["テキストの埋め込みベクトル", "文書チャンクのベクトル"], "テキストのハッシュ\n＋モデル版（Embeddingモデル）",
         ["モデル版の変更", "埋め込みモデルの差し替え時は\vインデックスの再生成が必要"], "同一テキストの再埋め込みを削減"),
        ("azure:language-understanding", "意味キャッシュ", "（オプション）", ["質問の意味クラスタ", "類似質問のマッピング"], "質問の埋め込みベクトル\n＋モデル版（Embeddingモデル）",
         ["モデル版の変更", "辞書版の変更"], "頻出質問の定型化・類似質問提示\nなどで利用")]
cells = [[H("キャッシュ種別"), H("キャッシュ対象"), H("主なキー（例）"), H("無効化条件"), H("備考")]]
for i, (ic, t, sub, tgt, key, inv, note) in enumerate(rows):
    f = "#F3F7FB" if i % 2 == 0 else "#FFFFFF"
    cells.append([{"paras": [[{"text": t, "size_px": 18.5, "bold": True}]] + ([[{"text": sub, "size_px": 15}]] if sub else []), "color": HEAD, "fill": "#E6F1FB",
                   "align": "l", "line_pitch_px": 26, "inset_px": [86, 2, 4, 2]},
                  {**BUL, "text": "\n".join(tgt), "fill": f}, {**PL, "text": key, "fill": f}, {**BUL, "text": "\n".join(inv), "fill": f}, {**PL, "text": note, "fill": f}])
s.add(type="table", box=[16, T0, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells, border={"color": "#FFFFFF", "width_px": 3}, name="cache-table")
y = T0 + rh[0]
for i, r in enumerate(rows):
    s.icon(r[0], [34, y + (rh[i + 1] - 46) / 2, 46, 46])
    y += rh[i + 1]

# common rules
s.rect([16, 810, 338, 120], fill="#E6F1FB", r=6)
s.icon("azure:app-configuration", [38, 844, 54, 54])
s.text([108, 810, 240, 120], "共通ルール・補足", 20, bold=True, color=HEAD)
s.rect([360, 810, 1300, 120], fill="#F3F7FB", r=6)
s.add(type="text", box=[380, 816, 1270, 108], size_px=15.5, color=INK, valign="m", bullet=True, bullet_indent_px=16, line_pitch_px=25,
      text="キャッシュの有効期限（TTL）を設定し、一定期間で自動的に再取得する。\ndata_version（データ版）、設定版、モデル版、辞書版のいずれかが更新された場合は、該当キャッシュを無効化する。\nキャッシュを利用して取得した候補であっても、版・適用判定（VA）は必ず再実行する（古い結果を最新版・適用ありと誤って提示しないため）。\n生成文そのものは原則キャッシュしない（最新データ・設定を常に反映するため）。")
dump(s)
