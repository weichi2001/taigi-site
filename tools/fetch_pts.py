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
progs={}
for v in q('{ videoMarketingLabel(id:"%s"){ videos{ program{ id } } } }'%LABEL)['videoMarketingLabel']['videos']:
    progs[v['program']['id']]=1
items=[]
for pid in progs:
    if pid in EXCLUDE: continue
    p=q('{ program(id:"%s"){ id name latestCover seasons{ id name cover } } }'%pid)['program']
    ss=p['seasons'] or []
    tw=[s for s in ss if '台語' in s['name']]
    it={'pid':pid,'t':p['name'],'img':p.get('latestCover') or ''}
    if tw: s=tw[0]
    elif '台語' in p['name'] and ss: s=ss[-1]
    else:
        s=None
        if len(ss)==1: s=ss[0]
        it['u']=1
    if s:
        it['sid']=s['id']; it['img']=s.get('cover') or it['img']
    items.append(it); time.sleep(.3)
if len(items)<10: print('too few items',len(items)); sys.exit(1)
OUT.write_text(json.dumps({'updated':datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),'items':items},ensure_ascii=False,indent=1),encoding='utf-8')
print('ok',len(items))
