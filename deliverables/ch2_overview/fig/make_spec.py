import json
NAVY="#1B3F72"; INK="#1B2E55"; BLUE="#1F6FD1"; SUB="#33507A"; LB="#5B9BE0"
E=[]
def add(**k): E.append(k); return k
def T(box,text,size,bold=True,color=INK,align="l",valign="m",**k): return add(type="text",box=box,text=text,size_px=size,bold=bold,color=color,align=align,valign=valign,**k)
def R(box,fill="#FFFFFF",line=None,r=None,kind=None,**k):
    d=dict(type=kind or ("roundRect" if r is not None else "rect"),box=box,fill=fill,line=line,**k)
    if r is not None: d["radius_px"]=r
    return add(**d)
def A(pts,color=BLUE,w=4,**k): return add(type="arrow",points=pts,color=color,width_px=w,**k)
def I(icon,box,color=None,**k):
    d=dict(type="icon",icon=icon,box=box,**k)
    if color: d["color"]=color
    return add(**d)
def L(color,w=1.5,dash=None): return {"color":color,"width_px":w,**({"dash":dash} if dash else {})}

# chapter header + title
R([0,0,1672,37],fill={"gradient":[["#D3E5F6",0],["#EEF5FB",100]],"angle":0},name="chapter-band")
R([0,0,24,37],fill="#2E5E8E")
T([38,3,640,32],"第2章 ｜ 全体/ユースケースごとのアーキテクチャ",21,bold=False,color="#1D3A64")
T([36,44,440,58],"図2-1 全体構成図",48,color="#0B1F4F",name="title")

# top flow band
R([29,113,189,74],fill="#F4F9FD",line=L("#6A87AE",2),r=10)
I("material:person-fill",[36,128,42,44],"#2A4A7A")
T([78,120,136,60],"生産技術部員\n（ブラウザ）",19,align="c")
A([[222,150],[252,150]],w=5)
steps=[(232,"Dify UI\nワークフロー"),(372,"質問解釈\n（LLM抽出＋検証）"),(525,"辞書・正規化"),(660,"ルーティング"),
       (790,"構造化検索SQL\n全文検索BM25\nベクトル検索"),(955,"RRF＋必須条件\nフィルタ（統合）"),(1105,"版・適用判定\nルール"),(1240,"根拠アセンブリ\nsource_ref")]
ends=[s for s,_ in steps[1:]]+[1395]
for i,((s,txt),e) in enumerate(zip(steps,ends)):
    n=txt.count("\n")+1
    paras=[]
    for j,line in enumerate(txt.split("\n")):
        paras.append([{"text":line,"size_px":15 if ("（LLM" in line) else (16 if n==3 else 17)}])
    add(type="homePlate" if i==0 else "chevron",box=[s,110,e-s+25,80],point_px=25,
        fill={"gradient":[["#D2E6F8",0],["#E8F2FC",100]],"angle":0},line=L("#FFFFFF",3),
        paras=paras,bold=True,color=INK,inset_px=[22,0,10,0],line_spacing=0.95,name=f"flow-{i+1}")
R([1420,110,228,80],fill="#EDF5FC")
A([[1435,150],[1468,150]],w=5)
T([1478,132,160,36],"Difyで結果表示",18,align="c")

# main frame
add(type="line",points=[[42,207],[1442,207],[1442,300],[1454,311],[1633,311],[1645,323],[1645,791],[1633,803],[42,803],[30,791],[30,219],[42,207]],color=NAVY,width_px=3,name="frame")
R([36,211,929,52],fill={"gradient":[["#0E2858",0],["#2C5289",100]],"angle":0},name="dgx-band")
I("lucide:server",[66,215,48,44],"#FFFFFF",stroke_width=1.8)
T([128,214,560,46],"DGX Spark 1台（オンプレミス）",32,color="#FFFFFF")
I("lucide:ban",[990,218,46,46],"#E01A1A",stroke_width=3)
T([1048,217,390,46],"外部通信なし ｜ 外部通信遮断",28,color="#E01A1A")
A([[1450,240],[1480,240]],color="#E02020",w=3,head="both")
I("lucide:globe",[1486,222,40,40],"#8A94A6")
I("lucide:ban",[1510,250,22,22],"#E01A1A",stroke_width=3)
T([1534,218,136,48],"インターネット\n（外部システム）",16,bold=False,color="#8A94A6")

# layer labels
layers=[(272,54,"1","利用者層"),(350,69,"2","部員が触る層"),(458,146,"3","開発者が守る層"),(618,76,"4","モデル層"),(712,79,"5","データ・検索基盤")]
for y,h,n,lab in layers:
    add(type="group",name=f"layer{n}-label",children=[
        dict(type="roundRect",box=[44,y,233,h],radius_px=4,fill=NAVY,line=None),
        dict(type="roundRect",box=[58,y+(h-38)/2,38,38],radius_px=4,fill="#3A7BBF",line=None,text=n,size_px=30,bold=True,color="#FFFFFF"),
        dict(type="text",box=[110,y,165,h],text=lab,size_px=22 if len(lab)<7 else 19,bold=True,color="#FFFFFF")])

# layer 1
R([288,272,1134,50],fill="#F7FAFD",line=L("#BFD3EA",1.5),r=6)
I("lucide:laptop",[652,274,56,46],NAVY,stroke_width=1.8)
T([726,280,240,32],"生産技術部員のブラウザ",22)
R([968,284,110,26],fill="#DCEAF8",r=4,text="PC／Browser",size_px=14,color="#5A7BA8")
A([[715,322],[715,355]],w=5); T([740,328,120,24],"質問・検索",17)
A([[948,355],[948,322]],w=5); T([973,328,120,24],"回答表示",17)

# layer 2
R([292,356,1138,58],fill="#E3F0FB",line=L(LB,2),r=8)
I("simple:docker",[316,368,48,32],"#2496ED")
T([376,366,244,38],"Dify CE（Docker）",25)
box=L("#7A93B8",1.5)
R([620,364,208,44],line=box,r=4,text="チャットUI",size_px=18,bold=True,color=INK)
R([860,364,255,44],line=box,r=4,paras=[[{"text":"ワークフローDSL","size_px":18}],[{"text":"（分岐・文言・表示項目）","size_px":13}]],bold=True,color=INK,line_spacing=0.9)
R([1146,364,256,44],line=box,r=4,paras=[[{"text":"検索API呼び出し","size_px":18}],[{"text":"（OpenAPI）","size_px":13}]],bold=True,color=INK,line_spacing=0.9)
A([[832,386],[857,386]],color="#2A86DB"); A([[1118,386],[1143,386]],color="#2A86DB")
A([[730,418],[730,463]],w=5); T([752,420,160,44],"検索リクエスト\n（質問・条件）",17,line_spacing=0.95)
A([[1010,463],[1010,416]],w=5); T([1042,420,170,44],"検索結果\n（根拠付き回答）",17,line_spacing=0.95)

# layer 3
R([292,465,1142,139],fill="#EAF3FC",line=L(LB,2),r=8)
I("simple:docker",[316,472,48,32],"#2496ED")
T([386,468,330,32],"検索API FastAPI（Docker）",22)
sb=L("#7A93B8",1.5)
def sub(x,w,txt,size=17): R([x,507,w,84],line=sb,r=4,text=txt,size_px=size,bold=True,color=INK,line_spacing=0.95)
sub(305,115,"質問解釈\nLLM抽出＋\nコード検証",15); sub(446,114,"用語辞書・\n正規化"); sub(586,114,"ルーティング")
R([727,488,224,114],fill=None,line=L("#7A93B8",1.2,"dot"),r=4)
for yy,ic,txt in [(495,"material:database-fill","構造化検索SQL"),(531,"lucide:search","全文検索BM25"),(566,"lucide:atom","ベクトル検索")]:
    R([740,yy,196,29],line=L("#7A93B8",1.2),r=4)
    I(ic,[762,yy+4,22,22],NAVY,**({"stroke_width":2.5} if ic.startswith("lucide") else {}))
    T([798,yy,130,29],txt,16)
sub(974,146,"RRF＋必須条件\nフィルタ\n（統合）"); sub(1147,109,"版・適用判定\nルール"); sub(1282,142,"根拠アセンブリ\nsource_ref")
for x1,x2 in [(421,444),(561,584),(701,725),(952,972),(1121,1145),(1257,1280)]:
    A([[x1,549],[x2,549]],color="#2A86DB")

# layer 4
m=L("#6F95C8",1.5)
R([293,620,434,72],fill="#F7FAFD",line=m,r=4)
I("lucide:brain",[322,626,50,50],NAVY,stroke_width=1.8)
add(type="text",box=[388,622,330,34],paras=[[{"text":"LLM ","size_px":26,"bold":True},{"text":"(vLLM / llama.cpp)","size_px":20}]],color=INK,bold=True)
R([390,657,264,28],fill="#DDEBF8",r=4,text="質問解釈／根拠付き説明生成のみ",size_px=16,color=SUB)
R([738,620,344,72],fill="#F7FAFD",line=m,r=4)
I("lucide:cpu",[764,625,46,46],NAVY,stroke_width=2)
T([824,624,200,34],"Embedding",24)
R([826,657,125,28],fill="#DDEBF8",r=4,text="ベクトル検索用",size_px=16,color=SUB)
R([1094,620,338,72],fill="#F7FAFD",line=L("#6F95C8",1.5,"dash"),r=4)
I("lucide:cpu",[1124,625,46,46],NAVY,stroke_width=2)
T([1182,624,112,34],"Reranker",22)
R([1296,629,88,24],fill="#DDEBF8",r=4,text="任意接続",size_px=15,color=SUB)
R([1186,657,96,28],fill="#DDEBF8",r=4,text="任意接続",size_px=16,color=SUB)
add(type="line",points=[[636,704],[1266,704]],color=BLUE,width_px=3)
for x,y1,y2 in [(636,704,720),(1266,704,722),(785,704,693),(880,704,693)]:
    A([[x,y1],[x,y2]],w=3)

# layer 5
R([294,710,1140,83],fill="#EAF3FC",line=L(LB,2),r=8)
R([310,722,596,66],fill="#F7FAFD",line=L("#7A9CC8",1.5),r=4)
I("material:database-fill",[336,726,56,58],"#2A5CA8")
T([410,728,320,32],"PostgreSQL 中間DB",23)
T([410,759,420,26],"TOS検索単位／文書メタ／版適用／辞書／ログ",17,bold=False,color=SUB)
R([918,722,502,66],fill="#F7FAFD",line=L("#7A9CC8",1.5),r=4)
I("material:stacks-fill",[1004,724,60,60],"#2A5CA8")
T([1083,728,200,32],"OpenSearch",23)
T([1083,759,200,26],"全文＋ベクトル",17,bold=False,color=SUB)

# right column
T([1450,332,194,26],"横串の共通機能",21,align="c")
T([1450,357,194,24],"（全層に適用）",17,align="c")
cards=[(400,82,"material:verified_user-fill","認証・権限",NAVY,19),(496,84,"material:description-fill","監査ログ",NAVY,19),(600,84,"lucide:ban","外部通信遮断","#E01A1A",15),(700,84,"lucide:network","バージョン\n管理",NAVY,19)]
for y,h,ic,txt,col,sz in cards:
    R([1463,y,168,h],fill="#FAFCFE",line=L("#C3D3E6",1.5),r=6)
    I(ic,[1476,y+(h-42)/2,42,42],col,**({"stroke_width":3 if "ban" in ic else 2.2} if ic.startswith("lucide") else {}))
    T([1528,y,100,h],txt,sz,line_spacing=0.95)

# ingest batch
R([33,813,1614,110],fill=None,line=L("#7A93B8",1.5,"dash"),r=8)
I("material:settings-fill",[50,850,44,44],NAVY)
T([106,852,150,40],"取込バッチ",28)
R([262,853,602,56],fill="#F4F8FD",line=L("#9FB6D3",1.5),r=6)
I("material:description-fill",[280,864,30,36],"#7E8FA8")
I("lucide:sheet",[314,866,32,32],"#2E9E4F",stroke_width=2.2)
T([354,866,166,30],"N-PLUS CSV 12表",16)
A([[522,881],[549,881]],color="#2A86DB",w=5)
R([556,861,290,40],line=L("#7A93B8",1.5),r=4,text="JOIN・コード変換・文脈化",size_px=16,bold=True,color=INK)
R([929,853,676,56],fill="#F4F8FD",line=L("#9FB6D3",1.5),r=6)
I("lucide:file-text",[944,862,34,38],NAVY,stroke_width=1.8)
I("lucide:file-spreadsheet",[980,862,34,38],NAVY,stroke_width=1.8)
I("material:picture_as_pdf-fill",[1016,862,36,38],"#2563B8")
T([1064,866,190,30],"Word／Excel／PDF",16)
A([[1258,881],[1285,881]],color="#2A86DB",w=5)
R([1292,861,302,40],line=L("#7A93B8",1.5),r=4,text="本文・表抽出・分割・メタ付与",size_px=16,bold=True,color=INK)
for x,c in [(527,BLUE),(727,"#4A9BE8"),(1126,BLUE),(1323,"#4A9BE8")]:
    A([[x,852],[x,796]],color=c,w=4)
for x,txt in [(546,"PostgreSQLへ投入\n（メタ・辞書 等）"),(747,"OpenSearchへ投入\n（本文・ベクトル化データ）"),(1146,"PostgreSQLへ投入\n（文書メタ 等）"),(1343,"OpenSearchへ投入\n（本文・ベクトル化データ）")]:
    T([x,808,180,42],txt,15,bold=False,color="#1F5FB8",line_spacing=0.95)

json.dump({"source_size":[1672,941],"font":"Meiryo","background":"#FFFFFF","elements":E},open("spec.json","w"),ensure_ascii=False,indent=1)
print(len(E),"elements")
