"""下載教育部臺灣台語常用詞辭典資料（kautian.ods）→ dict.json（詞目＋義項）、ex.json（例句，點開才載入）。
詞目音檔網址：https://sutian.moe.edu.tw/media/senn/mp3/imtong/subak/{id//1000}/{id}.mp3"""
import json,sys,urllib.request,pathlib
import pandas as pd
HERE=pathlib.Path(__file__).resolve().parent
U='https://sutian.moe.edu.tw/media/senn/ods/kautian.ods'
tmp=HERE/'kautian.ods'
r=urllib.request.Request(U,headers={'user-agent':'Mozilla/5.0'})
tmp.write_bytes(urllib.request.urlopen(r,timeout=180).read())
X=pd.read_excel(tmp,engine='odf',sheet_name=None,dtype=str)
tmp.unlink()
s=lambda v:'' if pd.isna(v) else str(v).strip()
W=X['詞目'];S=X['義項'];E=X['例句'];V=X.get('又唸作')
sen={};ex={};var={}
for _,r in S.iterrows(): sen.setdefault(int(r['詞目id']),[]).append([s(r['詞性']),s(r['解說'])])
for _,r in E.iterrows(): ex.setdefault(int(r['詞目id']),[]).append([s(r['漢字']),s(r['羅馬字']),s(r['華語'])])
if V is not None:
    for _,r in V.iterrows(): var.setdefault(int(r['詞目id']),[]).append([s(r['漢字']),s(r['羅馬字'])])
out=[]
for _,r in W.iterrows():
    i=int(r['詞目id'])
    out.append([i,s(r['漢字']),s(r['羅馬字']),s(r['分類']),1 if s(r['羅馬字音檔檔名']) else 0,sen.get(i,[]),var.get(i,[])])
if len(out)<10000: print('too few',len(out)); sys.exit(1)
(HERE.parent/'dict.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(HERE.parent/'ex.json').write_text(json.dumps(ex,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(len(out),'詞目',sum(len(v) for v in ex.values()),'例句')
