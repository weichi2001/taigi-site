import json,re,sys,time,urllib.request,urllib.parse
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u):
    r=urllib.request.Request(u,headers={'user-agent':UA,'accept':'application/json','referer':'https://www.ebookservice.tw/tc/'})
    return json.load(urllib.request.urlopen(r,timeout=40))
inc={x[1]:x for x in json.load(open('ebs.json'))}
cand={}
for qq in ['台語','臺語','台羅','閩南語','河洛','台文','母語','Tâi','Taiwanese','台灣話','客語','原住民']:
    got=0
    for pg in range(1,8):
        try: d=get('https://www.ebookservice.tw/api/1.00/search/web/tc/2/60/%d?q=%s'%(pg,urllib.parse.quote(qq)))
        except Exception as e: print(qq,pg,'ERR',e);break
        h=d['payload']['hits']
        if pg==1: print(qq,'found',h['found'], list(h['hit'][0]['fields'].keys()))
        for x in h['hit']: cand.setdefault(x['id'],x['fields']);got+=1
        if len(h['hit'])<60: break
        time.sleep(.3)
print('cand',len(cand),'inc',len(inc),'recall',len([i for i in inc if i in cand]))
miss=[i for i in inc if i not in cand];print('missed inc',[(inc[i][2]) for i in miss])
f=next(iter(cand.values()));print(json.dumps(f,ensure_ascii=False)[:1500])
print('--- IN')
for i in list(inc)[:0]: pass
n=0
for i,f in cand.items():
    if i in inc and n<12: n+=1;print('IN ',f.get('title'),'|',f.get('creators'),'|',{k:v for k,v in f.items() if k not in('id','title','creators','description','publisher')})
n=0
print('--- OUT')
for i,f in cand.items():
    if i not in inc and n<45: n+=1;print('OUT',f.get('title'),'|',f.get('creators'),'|',(f.get('description') or '')[:50].replace('\n',' '))
