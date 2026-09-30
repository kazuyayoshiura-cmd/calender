import sys
sys.path.insert(0, "..")
from lib import *

s = Slide()
s.title("4.4  表4-1  例外分岐一覧（候補なし・根拠不足・矛盾・版不明・対象外・低信頼）")
s.rect([24, 66, 1624, 56], fill="#F2F8FE", line={"color": "#9CC2E8", "width_px": 1.2}, r=4)
s.text([24, 67, 1624, 54], "検索・回答の過程で例外的な状況が発生した場合の検知方法、出力メッセージ、次に確認すべきこと、提示レベルを整理する。\nいずれの場合も、ユーザーに誤った情報を提示せず、適切な保留・確認を行う。",
       16.5, align="c", line_pitch_px=24, color=HEAD)

cols = [40, 104, 176, 124, 170, 300, 400, 206, 104]
xs = [24]
for w in cols:
    xs.append(xs[-1] + w)
T0 = 130
rh = [100, 124, 118, 120, 100, 96, 100]
ys = [T0 + 44]
for h in rh:
    ys.append(ys[-1] + h)

RED = "#D42A3A"; BLUE = "#1F4E9C"; ORANGE = "#E07A1F"
rows = [
    dict(kind="該当なし\n（確定キー）", pink=True,
         cond="部品番号・工程番号・\v文書番号などの確定キー\vで検索したが、\v該当レコードが存在しない。", det="構造化検索\v（SQL）\v0件",
         q="「部品番号 A12345\vのTOSを確認したい」",
         flow=[("構造化検索", "（完全一致・フィルタ）", "box"), ("0件", None, "box"), ("該当なし", "（類似で埋めない）", "pink")],
         msg=("error", RED, "該当レコードはありません。", ["・指定された部品番号：A12345", "・対象：TOS", "入力内容をご確認ください。"], None),
         nxt=["入力キーの再確認", "部品番号の桁数・表記", "別の部品番号で再検索"], lvl="結果表示\nなし\n（保留）"),
    dict(kind="曖昧\n（複数該当）",
         cond="確定キーで検索したが、\v複数の候補が該当し、\v閾値を超える件数がある。", det="構造化検索\v（SQL）\vn件 > 閾値\v（例：> 50件）",
         q="「工程番号 100 の\vTOSを確認したい」",
         flow=[("構造化検索", None, "box"), ("n件", "（多数）", "box"), ("候補一覧提示", "＋追加条件の依頼", "yellow")],
         msg=("info", BLUE, "複数の候補が見つかりました。", ["該当候補を絞り込むため、追加の条件を指定してください。"],
              ([44, 80, 160, 66], [["No.", "工程番号", "作業内容", "件数"], ["1", "100", "穴あけ加工", "120"], ["2", "100", "リーマ加工", "85"], ["3", "100", "面取り", "62"]])),
         nxt=["作業内容の指定", "版の指定", "適用範囲の指定", "より詳細なキーワード"], lvl="候補一覧\n（保留）"),
    dict(kind="根拠不足",
         cond="検索結果はあるが、\v上位候補のスコアが閾値\v未満、または回答に必要\vな根拠情報が不足している。", det="検索スコア\v閾値未満\v／必要項目の\v欠落",
         q="「この加工工程に近い\v過去のTOSを探したい」",
         flow=[("全文＋ベクトル検索", "（ハイブリッド）", "box"), ("低スコア", "／根拠欠落", "box"), ("保留", "（部分情報を参考提示）", "yellow")],
         msg=("warn", RED, "十分な根拠が得られないため、確定した回答はできません。", ["以下は参考となる候補です。"],
              ([40, 96, 64, 150], [["No.", "TOS番号", "類似度", "作業内容（要約）"], ["1", "TOS-12345", "0.42", "穴あけ加工 …"], ["2", "TOS-67890", "0.38", "リーマ加工 …"]])),
         nxt=["より具体的な作業内容", "部品番号の指定", "工程の特定", "関連するキーワード追加"], lvl="参考提示\n（保留）"),
    dict(kind="矛盾",
         cond="同一文書IDで版の内容が\v不整合、または複数候補\vで主要項目（作業内容・\v適用範囲等）が相違する。", det="版情報の不整合\v複数候補の\v主要項目差異",
         q="「JP-123の\v作業内容を教えて」", flow="conflict",
         msg=("warn", RED, "複数の候補で内容に相違があります。", ["ご確認のうえ、適切な版を選択してください。"],
              ([90, 130, 130], [["項目", "Rev.2", "Rev.3"], ["作業内容", "穴あけ加工", "リーマ加工"], ["適用範囲", "A機種のみ", "A/B機種"], ["更新日", "2023/01/10", "2024/05/20"]])),
         nxt=["どちらの版を参照すべきか", "適用する機種・期間の確認", "担当者への確認"], lvl="候補比較\n（保留）"),
    dict(kind="版・適用不明",
         cond="検索結果において、\v版列がNULL、または\v適用情報が登録されて\vいない。", det="版列NULL\v適用情報なし",
         q="「JP-456の\v最新版を教えて」",
         flow=[("検索結果取得", None, "box"), ("版・適用情報", "なし", "box"), ("適用未確認", "（最新版と断定しない）", "yellow")],
         msg=("info", BLUE, "版・適用情報が不明です。", ["以下の候補は適用情報が登録されていません。"],
              ([40, 80, 110, 50, 70], [["No.", "文書番号", "作業内容", "版", "適用範囲"], ["1", "JP-456", "溶接作業", "－", "－"]])),
         nxt=["最新版の確認", "適用範囲の確認", "担当者への確認"], lvl="参考提示\n（保留）"),
    dict(kind="対象外",
         cond="画像・図面・NECST 等\v本PoCの対象外データ\vに関する質問。", det="キーワード検知\v（図面、画像、\vNECST 等）",
         q="「この図面と類似形状\vのWPSを探したい」",
         flow=[("対象外判定", None, "box"), ("PoC対象外", "（案内メッセージ）", "yellow")],
         msg=("info", BLUE, "ご質問の内容は、本PoCの対象外です。", ["・対象外：図面画像の類似形状検索", "・確認先：設計部門／関連システム", "※ 将来的な拡張で対応を検討します。"], None),
         nxt=["対象システムの利用", "設計部門への確認", "将来の対応可否の確認"], lvl="回答なし\n（案内）"),
    dict(kind="低信頼",
         cond="検索スコアが閾値未満\vかつ一致条件が少なく、\v回答の信頼性が低い\vと判断される。", det="総合スコア < 閾値\v一致条件が少ない",
         q="「Aと似た工程の\vTOSを探して」",
         flow=[("検索結果", None, "box"), ("低信頼", "（スコア < 閾値）", "box"), ("低信頼のため保留", "（追加条件の提示）", "yellow")],
         msg=("warn", RED, "回答の信頼性が低いため、確定した回答はできません。\v追加の条件を指定してください。", ["（参考）類似候補：2件（スコア：0.31, 0.28）"], None),
         nxt=["より具体的なキーワード", "部品番号／工程の指定", "作業内容の詳細化"], lvl="参考提示\n（保留）"),
]

HDR = lambda t1, t2=None, s2=11: {"fill": "#123E82", "color": "#FFFFFF", "align": "c", "line_pitch_px": 19,
                           "paras": [[{"text": t1, "size_px": 15, "bold": True}]] + ([[{"text": t2, "size_px": s2, "bold": True}]] if t2 else [])}
cells = [[HDR("No."), HDR("例外の種類"), HDR("条件", "（どのようなときに発生するか）", 10), HDR("検知方法（例）"), HDR("ユーザーの質問例"),
          HDR("システムの動作・分岐イメージ"), HDR("出力メッセージ例", "（画面イメージ）"), HDR("次に確認すべきこと"), HDR("提示レベル")]]
TXT = {"size_px": 12.5, "color": INK, "align": "l", "line_pitch_px": 19, "inset_px": [10, 2, 4, 2]}
for i, r in enumerate(rows):
    kind_fill = "#FBE3E8" if r.get("pink") else "#FFF4D6"
    cells.append([
        {"text": str(i + 1), "size_px": 16, "bold": True, "color": HEAD, "align": "c"},
        {"text": r["kind"], "size_px": 16 if len(r["kind"]) < 6 else 14.5, "bold": True, "color": RED if r.get("pink") else INK, "align": "c", "fill": kind_fill, "line_pitch_px": 22},
        {"text": r["cond"], **TXT},
        {"text": r["det"], **TXT},
        {"text": ""}, {"text": ""}, {"text": ""},
        {"text": "\n".join(r["nxt"]), **TXT, "bullet": True, "bullet_indent_px": 14},
        {"text": r["lvl"], "size_px": 13, "color": INK, "align": "c", "line_pitch_px": 19},
    ])
s.add(type="table", box=[24, T0, sum(cols), ys[-1] - T0], col_widths_px=cols, row_heights_px=[44] + rh, cells=cells,
      border={"color": "#D3DEEB", "width_px": 1}, name="exception-table")

FLOWK = {"box": ("#E4F0FC", "#6E9BD6"), "yellow": ("#FFF1CC", "#E2B650"), "pink": ("#FBDDE2", "#D9707F")}


def fbox(box, t1, t2, kind, s1=12.5, s2=10):
    fill, line = FLOWK[kind]
    paras = [[{"text": t1, "size_px": s1, "bold": True, "color": HEAD}]] + ([[{"text": t2, "size_px": s2, "color": SUB}]] if t2 else [])
    s.add(type="roundRect", box=box, radius_px=4, fill=fill, line={"color": line, "width_px": 1.2}, paras=paras, align="c", line_pitch_px=16, inset_px=[3, 1, 3, 1])


ICON = {"error": ("material:error-fill", RED), "info": ("material:info-fill", "#2F6FD0"), "warn": ("material:warning-fill", ORANGE)}
for i, r in enumerate(rows):
    top, bot = ys[i], ys[i + 1]
    cy = (top + bot) / 2
    # question
    qx = xs[4]
    s.icon("material:person-fill", [qx + 4, cy - 14, 26, 28], "#1F3F7A")
    s.add(type="roundRect", box=[qx + 32, cy - 26, 132, 52], radius_px=8, fill="#FFFFFF", line={"color": "#8FB4E0", "width_px": 1.2},
          text=r["q"], size_px=11.5, color=INK, align="c", line_pitch_px=17)
    # flow
    fx = xs[5]
    if r["flow"] == "conflict":
        fbox([fx + 6, cy - 42, 78, 38], "候補A", "（Rev.2）", "box")
        fbox([fx + 6, cy + 4, 78, 38], "候補B", "（Rev.3）", "box")
        fbox([fx + 104, cy - 22, 82, 44], "内容比較で", "相違を検知", "box", s1=11.5, s2=11.5)
        s.E[-1]["paras"][1][0].update(bold=True, color=HEAD)
        fbox([fx + 204, cy - 24, 90, 48], "両方を提示", "＋矛盾箇所の明示", "yellow", s2=10.5)
        s.line([[fx + 84, cy - 23], [fx + 94, cy - 23], [fx + 94, cy + 23], [fx + 84, cy + 23]], w=1.4)
        s.arrow([[fx + 94, cy], [fx + 104, cy]], w=1.4)
        s.arrow([[fx + 186, cy], [fx + 204, cy]], w=1.4)
    else:
        n = len(r["flow"])
        widths = [100, 76, 108] if n == 3 else [120, 140]
        gap = (300 - 12 - sum(widths)) / (n - 1)
        x = fx + 6
        for j, ((t1, t2, kind), w) in enumerate(zip(r["flow"], widths)):
            fbox([x, cy - 24, w, 48], t1, t2, kind, s1=12 if len(t1) < 8 else 11)
            if j < n - 1:
                s.arrow([[x + w + 2, cy], [x + w + gap - 2, cy]], w=1.4)
            x += w + gap
    # message box
    mx = xs[6]
    kind, color, title, lines, table = r["msg"]
    warnish = kind in ("error", "warn")
    s.rect([mx + 6, top + 6, 388, bot - top - 12], fill="#FFF3F4" if warnish else "#F2F7FD",
           line={"color": "#E58A95" if warnish else "#8FB4E0", "width_px": 1.2}, r=4)
    ic, icol = ICON[kind]
    s.icon(ic, [mx + 12, top + 10, 20, 20], icol)
    tl = title.count("\v") + 1 if len(title) < 30 else 2
    s.text([mx + 36, top + 8, 352, 18 * tl + 4], title.replace("\v", "\v") if len(title) < 30 or "\v" in title else title[:26] + "\v" + title[26:],
           12.5, bold=True, color=color, valign="t", line_pitch_px=18)
    ty = top + 12 + 18 * tl
    s.text([mx + 36, ty, 352, 17 * len(lines)], "\n".join(lines), 11.5, color=INK, valign="t", line_pitch_px=17)
    if table:
        widths, data = table
        ty2 = ty + 17 * len(lines) + 3
        h = min(17, (bot - 10 - ty2) / len(data))
        s.add(type="table", box=[mx + 36, ty2, sum(widths), h * len(data)], col_widths_px=widths, row_heights_px=[h] * len(data),
              cells=[[{"text": c, "bold": k == 0, "fill": "#E6EEF8" if k == 0 else "#FFFFFF"} for c in row] for k, row in enumerate(data)],
              size_px=10.5, align="c", color=INK, border={"color": "#C9D6E6", "width_px": 0.8}, cell_pad_px=3)

s.dump()
