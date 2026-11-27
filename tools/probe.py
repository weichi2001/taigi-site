import json,re,sys,urllib.request
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u,data=None,h=None,t=40):
    r=urllib.request.Request(u,data,dict({'user-agent':UA,'accept-language':'zh-TW'},**(h or {})))
    try: return urllib.request.urlopen(r,timeout=t).read().decode('utf8','replace')
    except urllib.error.HTTPError as e: return 'HTTP %s %s'%(e.code,e.read().decode('utf8','replace')[:600])
def sec(x): print('\n=====',x,flush=True)
def q(s): return get('https://www.ptsplus.tv/graphql',json.dumps({'query':s}).encode(),{'content-type':'application/json'})
sec('PTS')
for s in ['{ __typename }','{ videoMarketingLabels{ id name } }','{ videoMarketingLabel(id:"695802cc-c1fe-4071-aea4-5bb21f0cee5a"){ id name } }','{ search(keyword:"台語"){ __typename } }','{ programs{ id } }','{ searchPrograms(keyword:"台語"){ id } }','{ program(id:"419e0c83-bc3c-44ec-8f1a-9e871b1310ca"){ id name seasons{ id name } labels{ id name } } }','{ __type(name:"Program"){ fields{ name } } }']:
    print(s,'->',q(s)[:600])
h=get('https://www.ptsplus.tv/')
print(len(h),re.findall(r'/_next/static/[^"]+\.js|/static/js/[^"]+',h)[:5], sorted(set(re.findall(r'href="(/[^"]*)"',h)))[:40])
sec('EBS bundle')
b=get('https://www.ebookservice.tw/js/main.bundle.js',t=60)
print(len(b))
for m in sorted(set(re.findall(r'["\'`](/(?:api|tc|ajax|Home|Book|library)[A-Za-z0-9_/\-\.?=&{}$]*)["\'`]',b)))[:150]: print(m)
for k in ['getBookList','booklist','searchBook','/api/','LibraryId','libraryId','category']:
    i=b.find(k)
    if i>=0: print('##',k,b[max(0,i-200):i+300].replace('\n',' '))
