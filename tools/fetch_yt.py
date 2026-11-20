#!/usr/bin/env python3
"""抓 YouTube 播放清單的逐集清單（影片編號、標題、片長）→ yt.json。
用 YouTube 網頁自己用的 innertube browse 介面（不需要帳號）。結果異常時不覆蓋舊檔。"""
import json, re, sys, time, urllib.request, pathlib
HERE=pathlib.Path(__file__).resolve().parent
OUT=HERE.parent/'yt.json'
IDS=[l.strip() for l in (HERE/'yt_playlists.txt').read_text().split('\n') if l.strip()]
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def req(url,data=None):
    r=urllib.request.Request(url,json.dumps(data).encode() if data else None,{'user-agent':UA,'accept-language':'zh-TW,zh;q=0.9','content-type':'application/json'})
    return urllib.request.urlopen(r,timeout=40).read().decode()
html=req('https://www.youtube.com/playlist?list='+IDS[0]+'&hl=zh-TW&persist_hl=1')
key=re.search(r'"INNERTUBE_API_KEY":"([^"]+)"',html).group(1)
ver=re.search(r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"',html).group(1)
CTX={'client':{'clientName':'WEB','clientVersion':ver,'hl':'zh-TW','gl':'TW'}}
def browse(body):
    body=dict(body,context=CTX)
    return json.loads(req('https://www.youtube.com/youtubei/v1/browse?key=%s&prettyPrint=false'%key,body))
def walk(o,vids,toks):
    if isinstance(o,dict):
        lv=o.get('lockupViewModel')
        if lv and lv.get('contentType')=='LOCKUP_CONTENT_TYPE_VIDEO':
            t=lv['metadata']['lockupMetadataViewModel']['title']['content']
            m=re.search(r'"text":\s*"(\d+:\d\d(?::\d\d)?)"',json.dumps(lv,ensure_ascii=False))
            vids.append([lv['contentId'],t,m.group(1) if m else ''])
        sl=o.get('shortsLockupViewModel')
        if sl:
            try:
                vid=sl['onTap']['innertubeCommand']['reelWatchEndpoint']['videoId']
                vids.append([vid,sl['overlayMetadata']['primaryText']['content'],'短'])
            except Exception: pass
        pv=o.get('playlistVideoRenderer')
        if pv:
            vids.append([pv['videoId'],''.join(r['text'] for r in pv['title'].get('runs',[])),(pv.get('lengthText') or {}).get('simpleText','')])
        c=o.get('continuationCommand')
        if c and c.get('token'): toks.append(c['token'])
        for v in o.values(): walk(v,vids,toks)
    elif isinstance(o,list):
        for v in o: walk(v,vids,toks)
res={}
for pid in IDS:
    vids=[];toks=[]
    try:
        walk(browse({'browseId':'VL'+pid}),vids,toks)
        seen=set()
        while toks and len(vids)<600:
            tk=toks.pop(0)
            if tk in seen: continue
            seen.add(tk)
            nv=[];nt=[]
            walk(browse({'continuation':tk}),nv,nt)
            vids+=nv; toks+=nt
    except Exception as e:
        print('fail',pid,e); continue
    uniq={}
    for v in vids: uniq.setdefault(v[0],v)
    res[pid]=list(uniq.values()); print(pid,len(res[pid])); time.sleep(.5)
if len(res)<len(IDS)//2: print('too few'); sys.exit(1)
EX=HERE.parent/'yt_extra.json'
if EX.exists():  # 台灣限定、Actions 抓不到的清單（手動在台灣瀏覽器抓好），一律以此為準
    for k,v in json.loads(EX.read_text(encoding='utf-8')).items():
        if v: res[k]=v
OUT.write_text(json.dumps(res,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
