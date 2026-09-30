import sys
sys.path.insert(0, "..")
from common import *

s = Slide()
header(s, "図6-2", "更新反映フロー（共有サーバー／CSV更新 → 画面反映）")

W, GAP, X0, Y0, H = 250, 28, 18, 92, 344
steps = [
    ("共有サーバー／", "CSV更新", ["共有サーバーのファイル\vまたはCSVが更新される"]),
    ("差分検知", "（ハッシュ・更新日）", ["ファイルハッシュの比較", "更新日・件数等の差分を\v検知"]),
    ("新版を取込・", "索引追加", ["更新されたファイル／\vCSVを取込み", "検索用の索引に追加"]),
    ("版テーブル更新", "（新版 latest、旧版 old）", None),
    ("索引切替・", "最終取込日時を記録", ["検索索引を最新版に切替", "最終取込日時を記録\v（ログに保存）"]),
    ("画面に最終取込日時", "を常に表示", ["検索画面や詳細画面に\v最終取込日時を常に表示\v（ユーザーが確認可能）"]),
]
xs = [X0 + i * (W + GAP) for i in range(6)]
for i, (t1, t2, bullets) in enumerate(steps):
    x = xs[i]
    s.rect([x, Y0, W, H], fill="#FFFFFF", line={"color": "#C8D9EC", "width_px": 1.5}, r=8)
    s.rect([x + 10, Y0 + 10, W - 20, 72], fill="#DDEEFB", r=6)
    s.rich([x + 34, Y0 + 12, W - 44, 68], [[{"text": t1, "size_px": 18.5, "bold": True}], [{"text": t2, "size_px": 15.5 if len(t2) > 12 else (17 if len(t2) > 9 else 18.5), "bold": True}]],
           color=HEAD, align="c", line_pitch_px=28)
    num(s, x + 22, Y0 + 20, i + 1, fill="#12398A", d=44, size=24)
    if bullets:
        s.add(type="text", box=[x + 16, Y0 + 236, W - 24, 104], text="\n".join(bullets), size_px=16, color=INK, valign="t",
              bullet=True, bullet_indent_px=16, line_pitch_px=25)
    if i < 5:
        s.add(type="rightArrow", box=[x + W + 2, Y0 + 150, 24, 28], fill="#1F6FD1", line=None)

# step icons (Azure)
s.icon("azure:storage-sync-services", [xs[0] + 60, Y0 + 100, 128, 124])
s.icon("azure:search", [xs[1] + 70, Y0 + 104, 112, 112])
s.icon("azure:files", [xs[2] + 66, Y0 + 100, 120, 120])
s.icon("azure:update-management-center", [xs[4] + 72, Y0 + 100, 108, 108])
# step 4: native version table (editable)
x = xs[3]
s.add(type="can", box=[x + 26, Y0 + 96, W - 52, 76], fill="#1F63C8", line=None, text="版テーブル", size_px=19, bold=True, color="#FFFFFF",
      adj=[0.35], inset_px=[0, 18, 0, 0])
s.add(type="table", box=[x + 26, Y0 + 176, W - 52, 96], col_widths_px=[74, 50, 74], row_heights_px=[32, 32, 32],
      cells=[[{"text": t, "bold": True, "fill": "#E6EEF8", "color": HEAD} for t in ("文書番号", "REV", "状態")],
             ["JP-001", "A", {"text": "old", "color": "#7A838F"}],
             ["JP-001", "B", {"text": "latest", "bold": True, "color": "#1F5FD0", "fill": "#DCEBFA"}]],
      size_px=14, align="c", color=INK, border={"color": "#C9D6E6", "width_px": 1}, cell_pad_px=3)
# step 6: native monitor showing last import time
x = xs[5]
s.rect([x + 30, Y0 + 100, W - 60, 118], fill="#FFFFFF", line={"color": "#0E2E63", "width_px": 6}, r=6)
s.rect([x + W / 2 - 12, Y0 + 218, 24, 16], fill="#0E2E63")
s.rect([x + W / 2 - 50, Y0 + 232, 100, 8], fill="#0E2E63", r=3)
s.icon("azure:file", [x + 44, Y0 + 124, 50, 60])
s.rich([x + 100, Y0 + 116, 116, 86], [[{"text": "最終取込日時", "size_px": 13, "bold": True}], [{"text": "2026/07/02", "size_px": 14, "bold": True}],
                                      [{"text": "18:22", "size_px": 14, "bold": True}]], color="#0E2E63", line_pitch_px=24)
s.E[-10:]  # keep order
# move monitor bullets below stand
s.E = [e for e in s.E]

# step 7: keep old versions
s.add(type="downArrow", box=[xs[3] + W / 2 - 16, Y0 + H + 4, 32, 28], fill="#1F6FD1", line=None)
BX = xs[3] - 10
s.rect([BX, 466, 1656 - BX, 170], fill="#F6F8FB", line={"color": "#D3DCE6", "width_px": 1.5}, r=8)
s.rect([BX, 466, 1656 - BX, 50], fill="#E6EAF0", r=8)
num(s, BX + 34, 491, 7, fill="#4A5563", d=44, size=24)
s.text([BX + 68, 466, 700, 50], "旧版は削除しない → 旧版保持", 22, bold=True, color=HEAD)
s.icon("azure:versions", [BX + 92, 534, 84, 84])
s.rect([BX + 184, 538, 90, 78], fill="#0E2E63", r=6, text="旧版\n(old)", size_px=19, bold=True, color="#FFFFFF", line_pitch_px=28)
s.add(type="text", box=[BX + 334, 530, 1656 - BX - 350, 100], text="過去の版（旧版）は削除せずに保持\n参照・比較・トレーサビリティのために維持\n必要に応じて画面上で旧版も参照可能",
      size_px=18, color=INK, valign="t", bullet=True, bullet_indent_px=18, line_pitch_px=30)

# "latest" concept band
s.rect([16, 656, 1640, 160], fill="#F2F7FD", line={"color": "#C8D9EC", "width_px": 1.5}, r=8)
s.rect([16, 656, 204, 160], fill="#0E3F82", r=8, text="最新の考え方\n（注意）", size_px=23, bold=True, color="#FFFFFF", line_pitch_px=36)
s.rect([246, 668, 216, 62], fill="#2A8FE8", r=6, paras=[[{"text": "取込済み最新", "size_px": 19, "bold": True}], [{"text": "（本システムの最新）", "size_px": 13.5, "bold": True}]],
       color="#FFFFFF", line_pitch_px=24)
s.icon("azure:sql-database", [318, 738, 70, 70])
s.rect([478, 668, 368, 138], fill="#FFFFFF", r=6)
s.rich([492, 674, 350, 30], [[{"text": "（本システムの最新）", "size_px": 18, "bold": True}]], color=HEAD)
s.add(type="text", box=[494, 708, 350, 94], text="本システムに取込み済みの中での最新版\n検索・参照の対象となる\n画面に表示する最終取込日時時点の最新", size_px=15.5, color=INK,
      valign="t", bullet=True, bullet_indent_px=14, line_pitch_px=26)
s.text([856, 700, 80, 80], "≠", 56, bold=True, color=HEAD, align="c")
s.rect([946, 668, 232, 62], fill="#6B7684", r=6, paras=[[{"text": "元システム最新", "size_px": 19, "bold": True}], [{"text": "（共有サーバー上の最新）", "size_px": 13.5, "bold": True}]],
       color="#FFFFFF", line_pitch_px=24)
s.icon("azure:storage-sync-services", [1026, 738, 72, 70])
s.rect([1194, 668, 450, 138], fill="#FFFFFF", r=6)
s.rich([1208, 674, 430, 30], [[{"text": "（共有サーバー上の最新）", "size_px": 18, "bold": True}]], color=HEAD)
s.add(type="text", box=[1210, 708, 430, 94], text="共有サーバー上に存在する最新版\n本システムにまだ取込みされていない可能性がある\n両者は一致しない場合がある（更新直後など）", size_px=15.5,
      color=INK, valign="t", bullet=True, bullet_indent_px=14, line_pitch_px=26)

warn(s, [16, 832, 1640, 94], ["取込済みの最新（本システムの最新）と、元システムの最新（共有サーバー上の最新）は異なる場合があります。",
                              "検索・参照の際は、画面に表示される「最終取込日時」を必ず確認してください。"], sizes=(21, 21))
dump(s)
