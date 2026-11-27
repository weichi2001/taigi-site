#!/usr/bin/env python3
"""從公視+ 抓「經典動畫✦台語配音也好好看」專輯，輸出 tw700/pts.json。
- 台語季：季名含「台語」→ 直連該季；片名含「台語」→ 用第一季
- 單季無標示的片：專輯本身是台語配音策展，仍收錄，標 u:1（待確認）
- 抓不到/結果異常時不覆蓋舊檔（exit 1）
"""
import json, sys, time, urllib.request, pathlib, datetime
API='https://www.ptsplus.tv/graphql'
LABEL='695802cc-c1fe-4071-aea4-5bb21f0cee5a'
EXCLUDE={'041f4a9b-0d1a-4f7c-ac51-a5d24004d039'}  # 百姓貴族：公視+ 無台語版（教師確認）
OUT=pathlib.Path(__file__).resolve().parent.parent/'pts.json'
def q(query):
    r=urllib.request.Request(API,json.dumps({'query':query}).encode(),
        {'content-type':'application/json','user-agent':'Mozilla/5.0 (taigi-site refresh)'})
    d=json.load(urllib.request.urlopen(r,timeout=30))
    if d.get('errors'): raise RuntimeError(d['errors'])
    return d['data']
progs={}   # pid -> True（來自精選專輯：沒標台語也先收，標 u）
for v in q('{ videoMarketingLabel(id:"%s"){ videos{ program{ id } } } }'%LABEL)['videoMarketingLabel']['videos']:
    progs[v['program']['id']]=True
# 公視+ 首頁所有頻道／片單：只收「季名或片名有標台語」的作品，這是判斷有沒有新台語片源的關鍵
try:
    off=0
    while off<400:
        recs=q('{ homepageMarketingLabels(limit:20,offset:%d){ records{ marketingLabel{ id name } } } }'%off)['homepageMarketingLabels']['records']
        if not recs: break
        for r in recs:
            lid=r['marketingLabel']['id']
            try:
                for v in q('{ videoMarketingLabel(id:"%s"){ videos{ program{ id } } } }'%lid)['videoMarketingLabel']['videos']:
                    progs.setdefault(v['program']['id'],False)
            except Exception as e: print('label fail',lid,e)
            time.sleep(.2)
        off+=20
except Exception as e: print('homepage labels fail',e)
items=[]
for pid,album in progs.items():
    if pid in EXCLUDE: continue
    try: p=q('{ program(id:"%s"){ id name latestCover seasons{ id name cover } } }'%pid)['program']
    except Exception as e: print('program fail',pid,e); continue
    ss=p['seasons'] or []
    tw=[s for s in ss if '台語' in s['name']]
    if not album and not tw and not ('台語' in p['name'] and ss):
        time.sleep(.15); continue
    it={'pid':pid,'t':p['name'],'img':p.get('latestCover') or ''}
    if tw: s=tw[0]
    elif '台語' in p['name'] and ss: s=ss[-1]
    else:
        s=None
        if len(ss)==1: s=ss[0]
        it['u']=1
    if s:
        it['sid']=s['id']; it['img']=s.get('cover') or it['img']
    # 集數：每個台語季都抓（間諜家家酒有兩季）；沒標台語的片不抓
    if not it.get('u'):
        its=[x for x in (tw or ([s] if s else []))]
        ss=[]
        for x in its:
            try:
                eps=q('{ season(id:"%s"){ episodes{ id name number } } }'%x['id'])['season']['episodes']
            except Exception as e:
                print('eps fail',p['name'],e); eps=[]
            eps=sorted(eps,key=lambda e:(e.get('number') or 0))
            ss.append({'sid':x['id'],'n':x['name'],'eps':[[e['id'],e.get('number'),(e['name'] or '').rsplit(' ep',1)[0]] for e in eps]})
            time.sleep(.3)
        if ss: it['ss']=ss
    items.append(it); time.sleep(.3)
if len(items)<10: print('too few items',len(items)); sys.exit(1)
old=json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {'items':[]}
oldp={i['pid'] for i in old['items']}
newp=[i['t'] for i in items if i['pid'] not in oldp and not i.get('u')]
print('NEW台語片源:',newp)
if oldp:
    sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
    import updlog
    for t in newp: updlog.add('video',t,src='公視+')
OUT.write_text(json.dumps({'updated':datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),'items':items},ensure_ascii=False,indent=1),encoding='utf-8')
print('ok',len(items))
