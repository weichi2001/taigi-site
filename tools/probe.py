import json,re,sys,urllib.request,time
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def post(s):
    r=urllib.request.Request('https://www.ptsplus.tv/graphql',json.dumps({'query':s}).encode(),{'content-type':'application/json','user-agent':UA})
    try: return json.load(urllib.request.urlopen(r,timeout=40))
    except urllib.error.HTTPError as e: return {'err':e.read().decode()[:500]}
print('===== PTS labels')
d=post('{ homepageMarketingLabels{ id name } }');print(json.dumps(d,ensure_ascii=False)[:1500])
labs=(d.get('data') or {}).get('homepageMarketingLabels') or []
known={i['pid'] for i in json.load(open('pts.json'))['items']}
seen={}
for L in labs:
    r=post('{ videoMarketingLabel(id:"%s"){ name videos{ program{ id name } } } }'%L['id'])
    v=((r.get('data') or {}).get('videoMarketingLabel') or {})
    ps=[x['program'] for x in v.get('videos',[])]
    print(L['name'],len(ps))
    for p in ps: seen[p['id']]=p['name']
print('programs seen',len(seen))
for pid,n in list(seen.items()):
    r=post('{ program(id:"%s"){ name seasons{ id name } } }'%pid)
    p=(r.get('data') or {}).get('program') or {}
    ss=[s['name'] for s in p.get('seasons') or []]
    if any('台語' in s for s in ss) or '台語' in n:
        print('TW', 'KNOWN' if pid in known else 'NEW', n, ss)
    time.sleep(.2)
print('===== EBS playwright')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(user_agent=UA)
    reqs=[]
    pg.on('response',lambda r:reqs.append((r.request.resource_type,r.status,r.url)) if r.request.resource_type in('xhr','fetch') else None)
    pg.goto('https://www.ebookservice.tw/tc/',wait_until='networkidle',timeout=60000)
    print(pg.url, pg.title())
    print([ (a.inner_text()[:20],a.get_attribute('href')) for a in pg.query_selector_all('a')][:80])
    print(reqs[:30])
    b.close()
