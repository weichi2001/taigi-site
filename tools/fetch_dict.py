"""下載教育部臺灣台語常用詞辭典資料（kautian.ods）→ dict.json（詞目＋義項）、ex.json（例句，點開才載入）。
詞目音檔網址：https://sutian.moe.edu.tw/media/senn/mp3/imtong/subak/{id//1000}/{id}.mp3"""
import json,sys,re,urllib.request,urllib.error,pathlib
from concurrent.futures import ThreadPoolExecutor
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
# ---- 詞目音檔路徑檢查 ----
# 多數詞目音檔在 imtong/subak/{id//1000}/{id}.mp3；但約 13% 的詞目（id 約 16000–22000、26000 以後）
# 教育部用隨機兩層資料夾 imtong/{xx}/{yy}/{id}1.mp3，只能到詞目頁面讀。這裡逐一檢查並記下。
SU='https://sutian.moe.edu.tw'
CACHE=HERE/'audio_cache.json'
prev=json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {'done':[],'ap':{},'none':[]}
done=set(prev['done']);ap=dict(prev['ap']);none=set(prev['none'])
def get(u,m='GET'):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,method=m,headers={'user-agent':'Mozilla/5.0'}),timeout=30)
        except urllib.error.HTTPError as e:
            if e.code==404:return None
        except Exception:pass
    return False
def check(i):
    r=get(f'{SU}/media/senn/mp3/imtong/subak/{i//1000}/{i}.mp3','HEAD')
    if r is False:return i,'?'
    if r is not None:return i,'ok'
    h=get(f'{SU}/zh-hant/su/{i}/')
    if not h:return i,'?'
    m=re.search(r'data-src="/media/senn/mp3/imtong/([^"?/]+/[^"?/]+)/%d1\.mp3'%i,h.read().decode('utf8','ignore'))
    return (i,m.group(1)) if m else (i,'none')
todo=[e[0] for e in out if e[4] and e[0] not in done]
print('待檢查音檔',len(todo))
with ThreadPoolExecutor(20) as pool:
    for i,v in pool.map(check,todo):
        if v=='?':continue
        done.add(i)
        if v=='none':none.add(i)
        elif v!='ok':ap[str(i)]=v
CACHE.write_text(json.dumps({'done':sorted(done),'ap':ap,'none':sorted(none)},separators=(',',':')),encoding='utf-8')
for e in out:
    if e[0] in none:e[4]=0
    elif str(e[0]) in ap:e[4]=2;e.append(ap[str(e[0])])
if len(out)<10000: print('too few',len(out)); sys.exit(1)
(HERE.parent/'dict.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(HERE.parent/'ex.json').write_text(json.dumps(ex,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(len(out),'詞目',sum(len(v) for v in ex.values()),'例句')
