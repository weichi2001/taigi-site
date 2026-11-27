import json,re,sys,urllib.request,urllib.parse
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u,data=None,h=None,t=40):
    r=urllib.request.Request(u,data,dict({'user-agent':UA,'accept-language':'zh-TW'},**(h or {})))
    return urllib.request.urlopen(r,timeout=t).read().decode('utf8','replace')
def sec(x): print('\n=====',x,flush=True)
sec('PTS introspection')
try:
    def q(s):
        return json.loads(get('https://www.ptsplus.tv/graphql',json.dumps({'query':s}).encode(),{'content-type':'application/json'}))
    d=q('{ __schema{ queryType{ fields{ name args{name type{name kind ofType{name}}} } } } }')
    for f in d['data']['__schema']['queryType']['fields']: print(f['name'],[a['name'] for a in f['args']])
    for tn in ['Program','Season','VideoMarketingLabel']:
        d=q('{ __type(name:"%s"){ fields{ name } } }'%tn);print(tn,[f['name'] for f in (d['data']['__type'] or {'fields':[]})['fields']])
except Exception as e: print('ERR',e)
sec('BONG feed')
try:
    t=get('https://tsbp.tgb.org.tw/feeds/posts/default?alt=json&max-results=3')
    j=json.loads(t);print(j['feed']['openSearch$totalResults'],[ (e['title']['$t'],e['published']['$t']) for e in j['feed']['entry']])
except Exception as e: print('ERR',e)
sec('EBS')
for u in ['https://www.ebookservice.tw/tc/','https://www.ebookservice.tw/tc/book/33825999-1bdd-4619-81cc-9dc44b058cff']:
    try:
        t=get(u);print(u,len(t));print(re.sub(r'\s+',' ',t)[:1500])
        print(sorted(set(re.findall(r'(?:href|src|action)="([^"]+)"',t)))[:60])
    except Exception as e: print(u,'ERR',e)
