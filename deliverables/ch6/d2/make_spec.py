import sys
sys.path.insert(0, "..")
from common import *

s = Slide()
header(s, "表6-1", "版・適用の情報源と優先順位")

cols = [236, 366, 298, 168, 576]
rh = [58, 92, 88, 90, 90, 96, 94]
T0 = 82
H = lambda t, **k: {"text": t, "fill": "#0E3F82", "color": "#FFFFFF", "bold": True, "size_px": 23, "align": "c", **k}
BUL = {"bullet": True, "bullet_indent_px": 18, "color": INK, "align": "l", "valign": "m", "fill": "#FFFFFF"}
PRI = {1: ("最優先", NAVY), 2: ("高", "#2AA0EE"), 3: ("補助", "#7A838F")}
rows = [
    ("REV", "（リビジョン）", ["図面マスター（UsingDWG.REV）", "文書管理（JP/WPS/SPEC 等）"], "最新判定の主要キー", "（同一文書番号内での新旧比較）", 1,
     [[("同一文書番号で、", False), ("発効日 ≦ 基準日 かつ有効の中で REV 最大を最新版", True), ("とする", False)], [("英数字の比較規則（例：A < B < … < Z < AA …）は Gate 0 で確認", False)]]),
    ("ED", "（改訂・設変番号）", ["図面マスター（UsingDWG.EO）", "文書管理（設変履歴 等）"], "版の派生関係・改訂の追跡", "（参考情報）", 2,
     [[("同一 REV 内の改訂識別に使用", False)], [("最新版判定の補助。運用は文書種別により異なるため Gate 0 で確認", False)]]),
    ("発効日", "（有効開始日）", ["文書管理（発効日）", "図面マスター（承認日・発効日 等）"], "最新判定の条件", "（基準日時点で有効かの判定）", 1,
     [[("発効日 ≦ 基準日 のものを対象とする", False)], [("未発効の文書は最新版としない", False)]]),
    ("FROM - THRU", "（適用号機範囲）", ["図面マスター（UsingDWG.\vSerialFrom / SerialThru）"], "対象への適用判定", "（号機・製番の範囲確認）", 1,
     [[("対象の号機・製番が FROM ～ THRU の範囲内に含まれるかで判定", False)], [("NULL（空欄）の扱い（全号機適用等）は Gate 0 で確認", False)]]),
    ("MBOM部品バージョン", "有効開始/終了日", ["MBOM（部品マスター／構成履歴）"], "部品の適用判定", "（構成の有効期間確認）", 2,
     [[("対象日時点で ", False), ("有効開始日 ≦ 基準日 ≦ 有効終了日", True), (" を満たすものを適用", False)], [("終了日が NULL の扱い（無期限等）は Gate 0 で確認", False)]]),
    ("履歴番号", "（改訂履歴・変更履歴）", ["文書管理（改訂履歴）", "システム履歴（承認履歴 等）"], "変更経緯の確認", "（参考情報）", 3,
     [[("最新版判定・適用判定の補助情報として利用", False)], [("履歴番号のみでは最新版・適用を判定しない", False)]]),
]
cells = [[H("情報"), H("主な情報源"), H("用途"), H("優先度・留意点", span=[1, 2]), None]]
for name, sub, src, use1, use2, pri, notes in rows:
    label, _ = PRI[pri]
    long_name = len(name) > 8
    cells.append([
        {"paras": [[{"text": name, "size_px": 18.5 if long_name else 25, "bold": True}], [{"text": sub, "size_px": 18 if not long_name else 18.5, "bold": True}]],
         "color": HEAD, "fill": "#E6F1FB", "align": "l", "line_pitch_px": 30, "inset_px": [20, 2, 4, 2]},
        {**BUL, "text": "\n".join(src), "size_px": 17.5, "line_pitch_px": 28, "inset_px": [20, 2, 6, 2]},
        {"paras": [[{"text": use1, "size_px": 18, "bold": True}], [{"text": use2, "size_px": 17.5}]], "color": INK, "fill": "#FFFFFF", "align": "l",
         "line_pitch_px": 29, "inset_px": [16, 2, 4, 2]},
        {"text": label, "size_px": 22, "bold": True, "color": HEAD if pri != 3 else "#4A5563", "align": "l", "fill": "#F5F9FD", "inset_px": [76, 2, 4, 2]},
        {**BUL, "fill": "#F5F9FD", "line_pitch_px": 27, "inset_px": [16, 2, 4, 2], "size_px": 14.5,
         "paras": [[{"text": t, "bold": b} for t, b in para] for para in notes]},
    ])
s.add(type="table", box=[16, T0, sum(cols), sum(rh)], col_widths_px=cols, row_heights_px=rh, cells=cells,
      border={"color": "#D6E1EE", "width_px": 1.5}, name="source-table")
y = T0 + rh[0]
x_badge = 16 + sum(cols[:3]) + 42
for i, r in enumerate(rows):
    num(s, x_badge, y + rh[i + 1] / 2, r[5], fill=PRI[r[5]][1], d=46, size=24)
    y += rh[i + 1]

# bottom panels
PY = 706


def panel(x, w, title, fill):
    s.rect([x, PY, w, 218], fill="#F7FAFD", line={"color": "#C4D6EA", "width_px": 1.2}, r=6)
    s.rect([x, PY, w, 44], fill=fill, r=6)
    s.rect([x, PY + 24, w, 20], fill=fill)
    s.text([x + 18, PY, w - 24, 44], title, 22, bold=True, color="#FFFFFF")


panel(16, 546, "最新版の判定ルール（基本）", "#0E4A9A")
for i, t in enumerate(["同一文書番号の候補を抽出", "発効日 ≦ 基準日 かつ 有効（終了日未到達）のものに絞り込み", "REV（必要に応じて ED を含む）の比較規則に従い、\v最大のものを最新版とする"]):
    cy = PY + 76 + i * 50
    num(s, 52, cy, i + 1, fill=NAVY, d=36, size=19)
    s.text([82, cy - 24, 474, 48 if i < 2 else 56], t, 16.5, color=INK, line_pitch_px=24)

panel(576, 564, "適用の判定ルール（基本）", "#1D64C4")
for i, t in enumerate(["対象の号機・製番が FROM ～ THRU の範囲内に含まれるかを確認\v（図面・文書）", "部品については 有効開始日 ≦ 基準日 ≦ 有効終了日 を確認\v（MBOM）", "上記を満たすもののみを適用と判定する"]):
    cy = PY + 78 + i * 56
    num(s, 612, cy, i + 1, fill="#2A8FE8", d=36, size=19)
    s.text([642, cy - 26, 494, 52], t, 16, color=INK, line_pitch_px=24)

panel(1154, 502, "共通の留意事項", "#5B6573")
s.add(type="text", box=[1170, PY + 52, 480, 162], valign="t", color=INK, bullet=True, bullet_indent_px=16, line_pitch_px=22.5, size_px=15,
      text="未発効の文書は、たとえ REV が最大でも最新版としない。\nNULL（空欄・未設定）の扱い（全号機適用、無期限 等）は\v文書種別ごとに異なるため、Gate 0 で確認する。\nREV・ED の比較規則（英数字・桁数・先頭ゼロの扱い等）は\vGate 0 で確認し、実装時に固定する。\n情報が欠損している場合でも、最新版であると断定しない。\v不明の場合は「適用未確認」として扱う。")
dump(s)
