import json,re,urllib.request
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u):
    r=urllib.request.Request(u,headers={'user-agent':UA})
    try: return urllib.request.urlopen(r,timeout=40).read().decode('utf8','replace')
    except Exception as e: return 'ERR %s'%e
h=get('https://www.ptsplus.tv/')
srcs=sorted(set(re.findall(r'(/_next/static/[^"\']+\.js)',h)))
print(len(srcs))
seen=set()
for s in srcs:
    js=get('https://www.ptsplus.tv'+s)
    for kw in ['homepageMarketingLabels','programs(','searchProgram','search(','keyword','videoMarketingLabel']:
        for m in re.finditer(re.escape(kw),js):
            seg=js[max(0,m.start()-150):m.start()+450].replace('\n',' ')
            key=seg[:80]
            if key in seen: continue
            seen.add(key); print('##',s[-40:],kw,'::',seg);print()
            break
