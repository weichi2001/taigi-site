import urllib.request,sys,io,zipfile
u='https://sutian.moe.edu.tw/zh-hant/siongkuantsuguan/'
r=urllib.request.Request(u,headers={'user-agent':'Mozilla/5.0'})
h=urllib.request.urlopen(r,timeout=60).read().decode('utf8')
import re
print([x for x in re.findall(r'href="([^"]+)"',h) if re.search(r'\.(ods|zip)',x)])
