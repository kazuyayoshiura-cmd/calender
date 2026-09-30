import sys
sys.path.insert(0, "../../ch6")
from common import *

EB = "#1F7FE0"  # evidence badge
s = Slide()
s.text([24, 4, 1640, 64], "図7-2　説明生成と根拠IDの対応", 40, bold=True, color=HEAD)

# column layout (all inside 16..1656)
C = [(16, 346), (384, 352), (756, 292), (1066, 252), (1356, 300)]
heads = [("① 検索結果", "（候補の evidence[]）"), ("② 説明生成（LLM）", "（evidence 以外を根拠にしない）"), ("③ 生成結果", "（参照ID付きの説明文）"),
         ("④ コード検証", "（参照IDのチェック）"), ("⑤ Dify での表示", "（回答・根拠・参照リンク）")]
for (x, w), (t1, t2) in zip(C, heads):
    s.rect([x, 72, w, 74], fill="#0E3F82", paras=[[{"text": t1, "size_px": 22, "bold": True}], [{"text": t2, "size_px": 17 if len(t2) < 16 else 15.5}]],
           color="#FFFFFF", line_pitch_px=30)

BODY_Y, BODY_H = 156, 508
# ---- ① search results
x, w = C[0]
s.rect([x, BODY_Y, w, 578], fill="#EAF3FC", r=6)
s.text([x, BODY_Y + 6, w, 34], "検索API /search の結果", 19, bold=True, color=HEAD, align="c")
ev = [("E1", "REF-0001", "作業標準 JP-123", "Rev.3（2024-05-01）", "「治工具の取り付け後、\vトルク 15N・m で締め付ける。」", "p.12 3.2項", "作業標準（PDF）"),
      ("E2", "REF-0456", "TOS-2024-001", "A", "「本工程では治工具Aを使用し、\v締付トルクは15N・mとする。」", "工程 10", "N-PLUS（TOS）")]
for i, (tag, ref, fn, rev, quote, loc, kind) in enumerate(ev):
    y = BODY_Y + 48 + i * 238
    s.rect([x + 12, y, w - 24, 228], fill="#FFFFFF", r=6)
    s.rect([x + 22, y + 12, 50, 44], fill=EB, r=4, text=tag, size_px=21, bold=True, color="#FFFFFF")
    s.text([x + 82, y + 8, w - 100, 26], "source_ref_id：" + ref, 16, bold=True, color="#0E2E63")
    s.text([x + 82, y + 34, w - 100, 24], "ファイル名：" + fn, 14.5, color=INK)
    s.text([x + 82, y + 56, w - 100, 24], "版：" + rev, 14.5, color=INK)
    s.text([x + 82, y + 80, 120, 22], "本文抜粋：", 14.5, color=INK)
    s.rect([x + 82, y + 104, w - 110, 60], fill="#EEF2F7", r=4)
    s.text([x + 90, y + 108, w - 124, 52], quote, 14, color=INK, line_pitch_px=24)
    s.text([x + 82, y + 170, w - 100, 24], "場所：" + loc, 14.5, color=INK)
    s.text([x + 82, y + 194, w - 100, 24], "種別：" + kind, 14.5, color=INK)
s.text([x, BODY_Y + 530, w, 44], "・・・\n（上位 N 件を evidence[] として提示）", 14.5, color=SUB, align="c", line_pitch_px=20)

# ①→②
s.arrow([[x + w + 2, 420], [384 + 14, 420]], w=2.5)
s.text([x + w - 6, 346, 60, 70], "", 12)  # spacer (unused)

# ---- ② LLM
x, w = C[1]
s.rect([x + 14, BODY_Y, w - 28, BODY_H], fill="#EAF3FC", r=6)
s.rect([x + 30, BODY_Y + 12, w - 60, 172], fill="#FFFFFF", r=6)
s.icon("azure:azure-openai", [x + w / 2 - 36, BODY_Y + 26, 72, 72])
s.text([x + 30, BODY_Y + 106, w - 60, 66], "LLM\n（生成）", 20, bold=True, color=HEAD, align="c", line_pitch_px=30)
s.rich([x + 30, BODY_Y + 196, w - 60, 32], [[{"text": "evidence[]", "size_px": 15.5, "bold": True}, {"text": "（本文・場所・source_ref）", "size_px": 12.5}]], color=HEAD)
s.text([x + 30, BODY_Y + 232, w - 60, 30], "プロンプト（抜粋）", 19, bold=True, color=HEAD)
s.add(type="text", box=[x + 30, BODY_Y + 266, w - 56, 236], valign="t", color=INK, bullet=True, bullet_indent_px=16, line_pitch_px=24, para_space_px=6, size_px=15,
      text="以下の evidence[] だけを根拠にして\v回答してください。\nevidence にない情報は\v生成しないでください。\n文章中に必ず参照IDを\v[E1][E2] の形式で付与してください。\n不明な点は「根拠が不足しています」\vとしてください。")

s.arrow([[x + w - 12, 420], [756 + 6, 420]], w=2.5)

# ---- ③ output
x, w = C[2]
s.rect([x + 6, BODY_Y, w - 12, BODY_H], fill="#EAF3FC", r=6)
s.rect([x + 16, BODY_Y + 10, w - 32, BODY_H - 20], fill="#FFFFFF", r=6)
s.text([x + 16, BODY_Y + 14, w - 32, 34], "LLM の出力例", 19, bold=True, color=HEAD, align="c")
s.line([[x + 30, BODY_Y + 52], [x + w - 30, BODY_Y + 52]], w=1, color="#C4D6EA")
EID = {"text": "", "bold": True, "color": "#FFFFFF"}


def ref_paras(chunks, size):
    runs = []
    for c in chunks:
        if c.startswith("["):
            runs.append({"text": c, "size_px": size, "bold": True, "color": EB})
        else:
            runs.append({"text": c, "size_px": size})
    return runs


out_paras = [ref_paras(["TOS-2024-001 では、本工程で\v治工具Aを使用し、締付トルクは\v15N・m と規定されています ", "[E2]", "。"], 16),
             ref_paras(["また、作業標準 JP-123 では、\v治工具の取り付け後、トルク\v15N・m で締め付ける手順が\v記載されています ", "[E1]", "。"], 16),
             ref_paras(["したがって、本工程の治工具A\vの締付トルクは 15N・m です\v", "[E1][E2]", "。"], 16)]
s.add(type="text", box=[x + 28, BODY_Y + 62, w - 50, BODY_H - 80], paras=out_paras, color=INK, valign="t", line_pitch_px=28, para_space_px=14)

s.arrow([[x + w - 4, 420], [1066 + 8, 420]], w=2.5)

# ---- ④ code check
x, w = C[3]
s.rect([x + 6, BODY_Y, w - 12, BODY_H - 70], fill="#EAF3FC", r=6)
s.icon("azure:form-recognizers", [x + 20, BODY_Y + 14, 58, 62])
s.rich([x + 86, BODY_Y + 18, w - 96, 56], [[{"text": "コード検証", "size_px": 19, "bold": True}], [{"text": "（ルールチェック）", "size_px": 15}]], color=HEAD, line_pitch_px=26)
for y, head, items in [(BODY_Y + 92, "参照IDの付与確認", ["すべての主張に参照ID\vが付いているか", "存在しない参照IDが\v含まれていないか"]),
                       (BODY_Y + 266, "根拠の整合性確認", ["evidence の内容と\v矛盾していないか", "根拠不足の主張がないか"])]:
    s.rect([x + 18, y, w - 36, 164], fill="#FFFFFF", r=6)
    s.rect([x + 18, y, w - 36, 38], fill="#D6E6F7", r=6, text=head, size_px=17, bold=True, color=HEAD)
    s.add(type="text", box=[x + 28, y + 46, w - 52, 114], text="\n".join(items), size_px=15, color=INK, valign="t", bullet=True, bullet_indent_px=14, line_pitch_px=24, para_space_px=6)
# OK -> ⑤
s.text([x + w - 4, 364, 44, 50], "検証\nOK", 15, bold=True, color=HEAD, align="c", line_pitch_px=21)
s.arrow([[x + w - 6, 420], [1356 + 2, 420]], w=2.5)
# NG -> hold
s.arrow([[x + w / 2, BODY_Y + BODY_H - 68], [x + w / 2, 680]], w=2.5, color="#D43A3A")
s.rich([x + w / 2 - 214, BODY_Y + BODY_H - 62, 204, 50], [[{"text": "NG", "size_px": 17, "bold": True}], [{"text": "（根拠不足・矛盾・参照IDなし）", "size_px": 12.5}]], color="#C0303A", line_pitch_px=22, align="r")

# ---- ⑤ Dify display
x, w = C[4]
s.rect([x, BODY_Y, w, BODY_H], fill="#EAF3FC", r=6)
s.text([x, BODY_Y + 6, w, 32], "Dify チャット画面（表示例）", 18, bold=True, color=HEAD, align="c")
s.icon("azure:users", [x + 12, BODY_Y + 46, 34, 36])
s.rect([x + 56, BODY_Y + 46, w - 68, 36], fill="#FFFFFF", r=6, text="この工程の治具の締付トルクは？", size_px=14, color=INK)
s.icon("azure:bot-services", [x + 12, BODY_Y + 102, 34, 34])
s.rect([x + 56, BODY_Y + 96, w - 68, 262], fill="#FFFFFF", r=6)
dify_paras = [ref_paras(["TOS-2024-001 では、本工程\vでは治工具Aを使用し、締付\vトルクは 15N・m と規定され\vています ", "[E2]", "。"], 13),
              ref_paras(["また、作業標準 JP-123 では、\v治工具の取り付け後、トルク\v15N・m で締め付ける手順が\v記載されています ", "[E1]", "。"], 13),
              ref_paras(["したがって、本工程の治工具A\vの締付トルクは 15N・m です\v", "[E1][E2]", "。"], 13)]
s.add(type="text", box=[x + 66, BODY_Y + 104, w - 84, 250], paras=dify_paras, color=INK, valign="t", line_pitch_px=20, para_space_px=6)
s.text([x + 12, BODY_Y + 370, 200, 26], "参照資料", 15.5, bold=True, color=HEAD)
for i, (tag, t) in enumerate([("E1", "作業標準 JP-123（Rev.3）p.12"), ("E2", "TOS-2024-001（A）工程10")]):
    y = BODY_Y + 402 + i * 46
    s.rect([x + 12, y, w - 24, 40], fill="#FFFFFF", r=4)
    s.rect([x + 18, y + 4, 36, 32], fill=EB, r=3, text=tag, size_px=15, bold=True, color="#FFFFFF")
    s.text([x + 60, y, w - 104, 40], t, 12, color=INK)
    s.icon("lucide:external-link", [x + w - 42, y + 9, 22, 22], EB, stroke_width=2.2)

# ---- hold band
s.rect([446, 680, 1210, 124], fill="#FDEDED", line={"color": "#F0B4B4", "width_px": 1.5}, r=6)
s.icon("material:error-fill", [462, 692, 42, 42], "#E02020")
s.rich([512, 690, 600, 34], [[{"text": "保留", "size_px": 22, "bold": True}, {"text": "（根拠不足・矛盾時）", "size_px": 17, "bold": True}]], color="#D42A2A")
s.add(type="text", box=[512, 726, 740, 76], size_px=15, color=INK, valign="t", bullet=True, bullet_indent_px=14, line_pitch_px=24,
      text="evidence に該当情報がない、または矛盾がある場合は回答を保留\n「根拠が不足しています／情報が矛盾しています」として返す（参照IDなしの文は削除）\n必要に応じて追加検索や対象の見直しを促す")
s.rect([1262, 694, 380, 98], fill="#FFFFFF", r=8)
s.icon("azure:bot-services", [1276, 718, 46, 46])
s.text([1334, 700, 300, 86], "該当する情報が見つかりませんでした。\n根拠が不足しています。\n別の条件で再検索してください。", 14.5, color=INK, line_pitch_px=24)

# ---- faithfulness band
s.rect([16, 818, 1640, 114], fill="#E6EFF8", r=8)
s.rect([30, 830, 326, 88], fill="#0E3F82", r=6, text="二重の Faithfulness 担保\n（ハルシネーション抑制）", size_px=21, bold=True, color="#FFFFFF", line_pitch_px=34)
for bx, n, head, items in [(380, 1, "生成時の制約", ["LLMに「evidence 以外を根拠にしない」指示", "必ず参照IDを付与するようプロンプトで制約"]),
                           (874, 2, "事後のコード検証", ["参照ID未付与文の検出・削除または保留", "evidence と矛盾する記述の検出"])]:
    s.rect([bx, 830, 420, 88], fill="#FFFFFF", line={"color": "#9DBBE0", "width_px": 1.2}, r=6)
    num(s, bx + 38, 874, n, fill="#1F6FD1", d=48, size=26)
    s.text([bx + 74, 834, 330, 30], head, 20, bold=True, color=HEAD)
    s.add(type="text", box=[bx + 74, 866, 342, 50], text="\n".join(items), size_px=14, color=INK, valign="t", bullet=True, bullet_indent_px=13, line_pitch_px=22)
s.text([806, 846, 64, 56], "+", 44, bold=True, color="#1F6FD1", align="c")
s.add(type="rightArrow", box=[1318, 850, 52, 46], fill="#1F6FD1", line=None)
s.rect([1384, 836, 262, 76], fill="#FFFFFF", line={"color": "#1F6FD1", "width_px": 2.5}, r=4, text="根拠に基づく\n信頼性の高い回答を表示", size_px=18, bold=True, color=HEAD, line_pitch_px=28)
dump(s)
