import re,urllib.request,pandas as pd,pathlib
H={'user-agent':'Mozilla/5.0'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=60).read()
p=pathlib.Path('k.ods');p.write_bytes(get('https://sutian.moe.edu.tw/media/senn/ods/kautian.ods'))
X=pd.read_excel(p,engine='odf',sheet_name=None,dtype=str)
for k,v in X.items(): print('SHEET',k,list(v.columns),len(v))
E=X['例句'];print(E.head(5).to_string())
for i in (1,2,3):
    h=get('https://sutian.moe.edu.tw/zh-hant/su/%d/'%i).decode('utf-8','ignore')
    print('PAGE',i,sorted(set(re.findall(r'[^"\'\s=]*\.mp3',h)))[:20])
    print(re.findall(r'<audio[^>]*>|data-[a-z-]*="[^"]*mp3[^"]*"',h)[:8])
