import re
BAD=re.compile(r'台語片|臺語片|電影|流行歌|憲章|解放|文訊|雜誌|越南語|韓語|英文|單字|日語|英語')
EXPL=re.compile(r'[台臺]文(?:詩|小說|散文|書寫|創作|作家|版|通訊|文學|雙語)|漢羅|台羅|臺羅|[台臺]華雙語|華[台臺]雙語|[台臺]法對照|[台臺]語(?:朗讀|有聲|詩集|小說|散文|漫畫|好讀版|文學叢書|版|囡仔歌|童謠|故事)|Tâi-lô|POJ')
def accept(f):
    if f.get('type') not in ('10','30','40'): return False
    t=f.get('title') or ''; d=f.get('description') or ''; s=f.get('series') or ''
    if re.search(r'台語|臺語|台文|臺文',s): return True
    if BAD.search(t): return False
    if re.search(r'台語|臺語|台羅|臺羅|[台臺]文(?![所館系學史藝戰化])|閩南語|河洛話|Tâi',t): return True
    return bool(EXPL.search(d))
