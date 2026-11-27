import json,urllib.request
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def post(s):
    r=urllib.request.Request('https://www.ptsplus.tv/graphql',json.dumps({'query':s}).encode(),{'content-type':'application/json','user-agent':UA})
    try: return json.load(urllib.request.urlopen(r,timeout=40))
    except urllib.error.HTTPError as e: return e.read().decode()[:700]
for s in ['{ homepageMarketingLabels{ __typename } }','{ homepageMarketingLabels{ labels{ id name } } }','{ homepageMarketingLabels{ items{ id name } } }','{ homepageMarketingLabels{ list{ id name } } }','{ homepageMarketingLabels{ marketingLabels{ id name } } }','{ programs{ __typename } }','{ programs{ items{ id name } } }','{ programs{ programs{ id name } } }','{ programs{ list{ id name } } }','{ programs{ edges{ node{ id name } } } }','{ programs{ programs{ id } total } }','{ videoSubMarketingLabel{ __typename } }','{ videoSubMarketingLabel(id:"695802cc-c1fe-4071-aea4-5bb21f0cee5a"){ id name } }','{ program(id:"419e0c83-bc3c-44ec-8f1a-9e871b1310ca"){ __typename id name } }']:
    print(s,'->',json.dumps(post(s),ensure_ascii=False)[:700]);print()
