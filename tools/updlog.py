"""把「新增了什麼」記到 updates.json（之後做公告／推送用）。只留最近 200 筆。"""
import json,pathlib,datetime
P=pathlib.Path(__file__).resolve().parent.parent/'updates.json'
def add(kind,title,**kw):
    try: d=json.loads(P.read_text(encoding='utf-8'))
    except Exception: d=[]
    d.insert(0,dict(kind=kind,title=title,date=datetime.date.today().isoformat(),**kw))
    P.write_text(json.dumps(d[:200],ensure_ascii=False,indent=1),encoding='utf-8')
