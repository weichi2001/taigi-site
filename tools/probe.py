import json,urllib.request
API='https://www.ptsplus.tv/graphql'
def q(s):
    r=urllib.request.Request(API,json.dumps({'query':s}).encode(),{'content-type':'application/json','user-agent':'Mozilla/5.0'})
    try:
        return json.load(urllib.request.urlopen(r,timeout=30))
    except Exception as e:
        return {'http':str(e),'body':getattr(e,'read',lambda:b'')().decode()[:600]}
pid='419e0c83-bc3c-44ec-8f1a-9e871b1310ca'
for f in ['genre','genres','category','categories','tags','type','contentType','format','labels','marketingLabels','programType','kind','classification','subject','subjects','channel','channels','introduction','description','displayType']:
    d=q('{ program(id:"%s"){ id %s } }'%(pid,f))
    print(f,'=>',json.dumps(d,ensure_ascii=False)[:500])
