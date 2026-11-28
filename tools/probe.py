import json,urllib.request,time
API='https://www.ptsplus.tv/graphql'
def q(s):
    r=urllib.request.Request(API,json.dumps({'query':s}).encode(),{'content-type':'application/json','user-agent':'Mozilla/5.0'})
    try: return json.load(urllib.request.urlopen(r,timeout=30))['data']
    except Exception as e: return {'err':str(e)}
P=json.load(open('pts.json'))['items']
for i in P:
    d=q('{ program(id:"%s"){ name categories tags } }'%i['pid'])
    print('PG',i['t'],'|',json.dumps(d,ensure_ascii=False)[:300])
off=0
while off<200:
    d=q('{ homepageMarketingLabels(limit:20,offset:%d){ records{ marketingLabel{ id name } } } }'%off)
    recs=(d.get('homepageMarketingLabels') or {}).get('records') or []
    if not recs: break
    for r in recs:
        m=r['marketingLabel'];n=len(((q('{ videoMarketingLabel(id:"%s"){ videos{ program{ id } } } }'%m['id']) or {}).get('videoMarketingLabel') or {}).get('videos',[]))
        print('LB',m['name'],n)
    off+=20
