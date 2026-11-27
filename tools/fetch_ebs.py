#!/usr/bin/env python3
"""台灣雲端書庫（臺中市）台語書單：用網站公開的搜尋介面找候選書，
- 新書若明確有台語文書寫（保守規則）→ 自動加進 ebs.json
- 其他新書 → 記在 ebs_review.json 給老師過目，不上架
- 已經看過的書都記在 ebs_seen.json，只處理「新出現」的。
第一次執行：把目前所有候選當成已看過，只把符合規則但尚未收錄的放進待確認。結果異常不覆蓋。"""
import json,re,sys,time,urllib.request,urllib.parse,pathlib,datetime
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from ebs_rule import accept
import updlog
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
QS=['台語','臺語','台羅','臺羅','台文','臺文','閩南語','河洛','Tâi','台灣話','台語文學']
def get(u):
    r=urllib.request.Request(u,headers={'user-agent':UA,'accept':'application/json','referer':'https://www.ebookservice.tw/tc/'})
    return json.load(urllib.request.urlopen(r,timeout=40))
cand={}
for qq in QS:
    for pg in range(1,12):
        try: h=get('https://www.ebookservice.tw/api/1.00/search/web/tc/2/60/%d?q=%s'%(pg,urllib.parse.quote(qq)))['payload']['hits']
        except Exception as e: print('fail',qq,pg,e); break
        for x in h['hit']: cand.setdefault(x['id'],x['fields'])
        if len(h['hit'])<60: break
        time.sleep(.3)
print('candidates',len(cand))
if len(cand)<300: print('too few, abort'); sys.exit(1)
L=lambda n,d:json.loads((ROOT/n).read_text(encoding='utf-8')) if (ROOT/n).exists() else d
cur=L('ebs.json',[]);have={x[1] for x in cur}
seen=set(L('ebs_seen.json',[]));first=not seen
review=L('ebs_review.json',[])
TYPE={'10':'B','30':'C','40':'P'}
def author(f):
    cr=[re.sub(r'(主編|編著|編|著|譯|繪)$','',c.split(',')[0].split('／')[0].strip()) for c in (f.get('creators') or [])]
    return ' '.join(cr[:2])[:24]
today=datetime.date.today().isoformat();added=[]
for i,f in cand.items():
    if i in seen or i in have: continue
    ok=f.get('type') in TYPE and accept(f)
    if first:
        if ok: review.append({'id':i,'t':f['title'],'a':author(f),'d':today,'why':'首次盤點：符合規則但尚未收錄'})
    elif ok:
        cur.append([TYPE[f['type']],i,f['title'],author(f),today]);added.append(f['title'])
    elif f.get('type') in TYPE:
        review.append({'id':i,'t':f['title'],'a':author(f),'d':today,'why':'新書但不確定是否有台語文書寫'})
    seen.add(i)
seen|=set(cand)
if added:
    cur.sort(key=lambda x:'PCB'.index(x[0]))
    (ROOT/'ebs.json').write_text(json.dumps(cur,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    for t in added: updlog.add('book',t,src='台灣雲端書庫')
(ROOT/'ebs_seen.json').write_text(json.dumps(sorted(seen)),encoding='utf-8')
(ROOT/'ebs_review.json').write_text(json.dumps(review[-300:],ensure_ascii=False,indent=1),encoding='utf-8')
print('added',added);print('review',len(review))
