import re,urllib.request
H={'user-agent':'Mozilla/5.0'}
h=urllib.request.urlopen(urllib.request.Request('https://sutian.moe.edu.tw/zh-hant/su/1/',headers=H),timeout=60).read().decode('utf-8')
for m in re.finditer(r'leku/\d+/\d+\.mp3',h):
    s=h[max(0,m.start()-250):m.end()+700]
    print('=====',m.group(0));print(re.sub(r'\s+',' ',s))
