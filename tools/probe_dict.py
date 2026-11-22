import urllib.request,zipfile,io
class R(io.RawIOBase):
    def __init__(s,u):
        s.u=u;s.pos=0
        r=urllib.request.Request(u,method='HEAD',headers={'user-agent':'Mozilla/5.0'});s.n=int(urllib.request.urlopen(r).headers['Content-Length'])
    def seekable(s):return True
    def readable(s):return True
    def tell(s):return s.pos
    def seek(s,o,w=0):
        s.pos=o if w==0 else s.pos+o if w==1 else s.n+o;return s.pos
    def read(s,k=-1):
        if k<0:k=s.n-s.pos
        if s.pos>=s.n:return b''
        e=min(s.n-1,s.pos+k-1)
        r=urllib.request.Request(s.u,headers={'Range':f'bytes={s.pos}-{e}','user-agent':'Mozilla/5.0'});d=urllib.request.urlopen(r).read();s.pos+=len(d);return d
    def readinto(s,b):
        d=s.read(len(b));b[:len(d)]=d;return len(d)
for n in ('leku-mp3','sutiau-mp3'):
    r=R(f'https://sutian.moe.edu.tw/media/senn/{n}.zip');print(n,r.n)
    z=zipfile.ZipFile(io.BufferedReader(r));L=z.namelist();print(len(L),L[:6],L[-3:])
