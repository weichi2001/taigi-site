import json,re,sys,time
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36'
log=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(user_agent=UA)
    def on(r):
        if r.request.resource_type in('xhr','fetch') and 'ebookservice' in r.url:
            try: t=r.text()[:700]
            except Exception: t=''
            log.append((r.status,r.url,t))
    pg.on('response',on)
    pg.goto('https://www.ebookservice.tw/tc/',wait_until='networkidle',timeout=60000)
    for s,u,t in log:
        if 'library-home' in u or 'chateaux' in u or 'categories' in u: print('##',u,t[:700].replace('\n',' '));print()
    n=len(log)
    pg.goto('https://www.ebookservice.tw/tc/search?q=%E5%8F%B0%E8%AA%9E',wait_until='networkidle',timeout=60000);time.sleep(2)
    print('URL',pg.url,pg.title())
    for s,u,t in log[n:]: print('##',s,u,t[:900].replace('\n',' '));print()
    print(pg.inner_text('body')[:1500])
    b.close()
