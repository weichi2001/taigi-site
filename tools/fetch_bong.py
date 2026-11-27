#!/usr/bin/env python3
"""抓《台文通訊BONG報》最新期數與各期封面／年月 → bong.json（只存期數、封面網址、年月；文章內容不複製）。
結果異常（抓不到、期數倒退）時不覆蓋舊檔。"""
import json,re,sys,time,urllib.request,urllib.parse,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import updlog
OUT=pathlib.Path(__file__).resolve().parent.parent/'bong.json'
F='https://tsbp.tgb.org.tw/feeds/posts/default'
N='台文通訊BONG報'
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'user-agent':UA}),timeout=40))
def entries(u):
    return get(u+('&' if '?' in u else '?')+'alt=json').get('feed',{}).get('entry',[]) 
def meta(n):
    es=entries(F+'/-/'+urllib.parse.quote(N+str(n)+'期')+'?max-results=4')
    for e in es:
        t=e['title']['$t']
        if t.startswith(N) and ' - ' not in t:
            h=(e.get('content') or e.get('summary') or {}).get('$t','')
            m=re.search(r'<img[^>]+src="([^"]+)"',h)
            cover=re.sub(r'/(s\d+|w\d+-h\d+)(-c)?/','/s600/',m.group(1).replace('http:','https:')) if m else ''
            txt=re.sub(r'<[^>]+>',' ',h)
            w=re.search(r'(\d{4})\s*年\s*(\d{1,2})\s*月',txt) or re.search(r'(\d{4})年(\d{1,2})月',t)
            return {'cover':cover,'when':'%s 年 %d 月'%(w.group(1),int(w.group(2))) if w else ''}
    return {'cover':'','when':''}
old={'latest':0,'issues':{}}
if OUT.exists():
    try: old=json.loads(OUT.read_text(encoding='utf-8'))
    except Exception: pass
es=entries(F+'?max-results=10')
nums=sorted({int(m.group(1)) for e in es for m in [re.search(r'(\d{3})期',e['title']['$t'])] if m},reverse=True)
if not nums: print('no issue found'); sys.exit(1)
latest=nums[0]
if latest<old.get('latest',0): print('latest went backwards',latest,old['latest']); sys.exit(1)
iss=dict(old.get('issues',{}))
for n in range(latest,max(latest-6,0),-1):
    if str(n) in iss and iss[str(n)].get('cover'): continue
    try: iss[str(n)]=meta(n)
    except Exception as e: print('meta fail',n,e)
    time.sleep(.5)
if latest>old.get('latest',0) and old.get('latest'):
    updlog.add('book','%s 第 %d 期'%(N,latest),src='BONG報')
import datetime
OUT.write_text(json.dumps({'updated':datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),'latest':latest,'issues':iss},ensure_ascii=False,indent=1),encoding='utf-8')
print('ok latest',latest,iss.get(str(latest)))
