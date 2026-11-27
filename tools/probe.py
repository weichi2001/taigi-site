import json,time,urllib.request
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def post(s):
    r=urllib.request.Request('https://www.ptsplus.tv/graphql',json.dumps({'query':s}).encode(),{'content-type':'application/json','user-agent':UA})
    try: return json.load(urllib.request.urlopen(r,timeout=40))
    except urllib.error.HTTPError as e: return {'err':e.read().decode()[:500]}
labs={}
off=0
while True:
    d=post('{ homepageMarketingLabels(limit:20,offset:%d){ records{ marketingLabel{ id name } } } }'%off)
    if 'err' in d or not d.get('data'): print(json.dumps(d,ensure_ascii=False)[:600]);break
    rec=d['data']['homepageMarketingLabels']['records']
    print('off',off,len(rec),[r['marketingLabel']['name'] for r in rec][:20])
    if not rec:break
    for r in rec: labs[r['marketingLabel']['id']]=r['marketingLabel']['name']
    off+=20
    if off>400:break
print('labels',len(labs))
known={i['pid'] for i in json.load(open('pts.json'))['items']}
seen={}
for lid,n in labs.items():
    r=post('{ videoMarketingLabel(id:"%s"){ videos{ program{ id name } } } }'%lid)
    v=((r.get('data') or {}).get('videoMarketingLabel') or {}).get('videos') or []
    print(n,len(v))
    for x in v: seen[x['program']['id']]=x['program']['name']
print('programs',len(seen))
for pid,n in seen.items():
    r=post('{ program(id:"%s"){ name seasons{ id name } } }'%pid);p=(r.get('data') or {}).get('program') or {}
    ss=[s['name'] for s in p.get('seasons') or []]
    if any('台語' in s for s in ss) or '台語' in n: print('TW','KNOWN' if pid in known else 'NEW',n,ss)
    time.sleep(.15)
