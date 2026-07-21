#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, time, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
TZ=timezone(timedelta(hours=3))
UA={"User-Agent":"Mozilla/5.0 TrendReportBot/5.0"}
YT_KEY=os.getenv("YOUTUBE_API_KEY","").strip()

GLOBAL_QUERIES=[
("YouTube Shorts","AI工具","AI tools shorts"),
("YouTube Shorts","知识科普","science explained shorts"),
("YouTube Shorts","旅行","travel shorts"),
("TikTok","生活反差","site:tiktok.com viral life story"),
("TikTok","挑战","site:tiktok.com challenge viral"),
("Instagram Reels","美食","site:instagram.com/reel food"),
]
CHINA_QUERIES=[
("抖音","AI效率","site:douyin.com AI 工具"),
("抖音","情绪共鸣","site:douyin.com 情绪 短视频"),
("快手","真实生活","site:kuaishou.com 生活"),
("快手","乡村美食","site:kuaishou.com 美食"),
("B站","知识科普","site:bilibili.com/video 科普"),
("视频号","家庭教育","视频号 家庭教育 热门"),
]

def http_json(url,retries=3):
    last=None
    for i in range(retries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last=e; time.sleep(1.5*(i+1))
    raise last

def http_bytes(url,retries=3):
    last=None
    for i in range(retries):
        try:
            req=urllib.request.Request(url,headers=UA)
            with urllib.request.urlopen(req,timeout=25) as r:return r.read()
        except Exception as e:
            last=e;time.sleep(1.5*(i+1))
    raise last

def yt_search(query,max_results=8):
    if not YT_KEY:return []
    q=urllib.parse.quote(query)
    url=f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={max_results}&q={q}&key={YT_KEY}"
    data=http_json(url)
    ids=[x["id"]["videoId"] for x in data.get("items",[]) if x.get("id",{}).get("videoId")]
    if not ids:return []
    u="https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id="+",".join(ids)+"&key="+YT_KEY
    vd=http_json(u)
    out=[]
    for x in vd.get("items",[]):
        sn=x.get("snippet",{}); st=x.get("statistics",{})
        out.append({
          "title":sn.get("title",""),"url":"https://www.youtube.com/watch?v="+x["id"],
          "source":sn.get("channelTitle","YouTube"),"published":sn.get("publishedAt",""),
          "thumbnail":((sn.get("thumbnails",{}).get("medium") or sn.get("thumbnails",{}).get("default") or {}).get("url","")),
          "signal":f"播放 {st.get('viewCount','?')} · 赞 {st.get('likeCount','?')} · 评论 {st.get('commentCount','?')}"
        })
    return out

def news_rss(query):
    url="https://news.google.com/rss/search?q="+urllib.parse.quote(query)+"&hl=zh-CN&gl=US&ceid=US:zh-Hans"
    try:
        root=ET.fromstring(http_bytes(url))
        out=[]
        for it in root.findall(".//item")[:8]:
            out.append({"title":(it.findtext("title") or "").strip(),"url":(it.findtext("link") or "").strip(),
            "source":(it.findtext("source") or "Google News RSS").strip(),"published":(it.findtext("pubDate") or "").strip(),
            "thumbnail":"","signal":"近期公开网页/RSS提及"})
        return out
    except Exception:return []

def why(cat):
    m={"AI工具":"结果先行 + 效率对比 + 可复制流程","知识科普":"反常识 + 高信息密度","旅行":"地点向往 + 收藏价值",
    "生活反差":"真实感 + 文化差异","挑战":"连续剧结构 + 悬念","美食":"视觉满足 + 无语言门槛","AI效率":"痛点明确 + 工作流演示",
    "情绪共鸣":"强代入 + 留白","真实生活":"人物关系 + 真实记录","乡村美食":"烟火气 + 完整过程","家庭教育":"讨论性 + 熟人传播"}
    return m.get(cat,"清晰钩子 + 快节奏 + 可讨论")

def build(queries,limit=10):
    pool=[]
    for platform,cat,q in queries:
        items=yt_search(q) if platform=="YouTube Shorts" else news_rss(q)
        for x in items:
            pool.append({"platform":platform,"category":cat,"title":x["title"][:140],"source":x["source"],
            "signal":x["signal"],"why":why(cat),"hook":"先展示结果，再解释过程","url":x["url"],"thumbnail":x.get("thumbnail",""),
            "published":x.get("published","")})
        time.sleep(.3)
    # Deduplicate by normalized title and URL.
    seen=set();out=[]
    for x in pool:
        key=re.sub(r"\W+","",x["title"]).lower()[:100] or x["url"]
        if key in seen:continue
        seen.add(key);out.append(x)
        if len(out)>=limit:break
    while len(out)<limit:
        i=len(out)+1
        out.append({"platform":"公开数据不足","category":"待核验","title":f"第 {i} 位暂无足够公开证据","source":"—",
        "signal":"公开数据不可完整验证","why":"不编造排名","hook":"—","url":"","thumbnail":""})
    return out

def load_archives():
    items=[]
    for p in sorted((ROOT/"archive").glob("*/*/*.json"),reverse=True):
        try:items.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:pass
    return items

def period_summary(current):
    hist=load_archives()[:365]
    cats=Counter()
    for d in hist+[current]:
        for x in d.get("global_top10",[])+d.get("china_top10",[]):
            if x.get("category")!="待核验":cats[x.get("category","其他")]+=1
    top="、".join([x for x,_ in cats.most_common(3)]) or "公开数据不足"
    return {
      "本周":f"近7日高频方向：{top}。重点观察持续出现且公开指标可验证的内容。",
      "本月":f"近30日主要趋势集中在：{top}。优先制作可跨平台改编的选题。",
      "本季度":f"季度方向以 {top} 为主。连续剧、前后对比和高信息密度内容更具复用价值。",
      "本年度":f"年度趋势显示，{top} 持续获得关注；真实体验与可信结果比单纯工具展示更重要。"
    }

def ideas():
    return [
      {"title":"同一选题的中外双版本实验","hook":"同一个故事，为什么中国版和海外版要用两种开头？","script":"海外版先给结果和视觉冲击，中国版加入人物关系与情绪铺垫。最后总结：海外内容进入中国，加关系与情绪；中国内容走向海外，删铺垫、提前结果。"},
      {"title":"30秒判断短视频是否值得拍","hook":"别先看点赞，先看三个结构信号。","script":"第一，前三秒是否提出冲突；第二，每五秒是否出现新信息；第三，结尾是否自然引导评论、收藏或转发。"},
      {"title":"四台设备组成24小时AI工作站","hook":"Mac、Windows、iPad和手机，怎样不再各自闲置？","script":"Mac负责创作，Windows负责自动化，iPad负责监控，手机负责采集、通知与审批。四台设备组成一套持续运行的AI系统。"}
    ]

def main():
    g=build(GLOBAL_QUERIES);c=build(CHINA_QUERIES)
    valid=[x for x in g+c if x["category"]!="待核验"]
    cats=Counter(x["category"] for x in valid);plats=Counter(x["platform"] for x in valid)
    topcat=cats.most_common(1)[0][0] if cats else "公开数据不足"
    focus=plats.most_common(1)[0][0] if plats else "公开数据不足"
    now=datetime.now(TZ)
    data={"updated_at":now.strftime("%Y-%m-%d %H:%M"),"kpis":{"top_category":topcat,
    "top_category_note":"按当日公开趋势信号出现频次","focus_platform":focus,
    "data_status":"YouTube官方API + 公开RSS" if YT_KEY else "公开RSS（未配置YouTube API）"},
    "summary":[
      "V5 已启用自动去重、失败重试、缩略图、公开指标字段以及周期汇总。",
      "配置 YOUTUBE_API_KEY 后，YouTube 条目将使用官方 Data API 获取公开视频标题、频道、发布时间、播放量、点赞量、评论量与缩略图。",
      "其他平台仍使用公开网页和 RSS 趋势信号；无法核验时明确标注，不冒充平台官方全量排行榜。"
    ],"global_top10":g,"china_top10":c,"ideas":ideas(),"archive":[]}
    data["period_reports"]=period_summary(data)
    day=now.strftime("%Y-%m-%d");adir=ROOT/"archive"/now.strftime("%Y")/now.strftime("%m");adir.mkdir(parents=True,exist_ok=True)
    (adir/f"{day}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    ars=[]
    for p in sorted((ROOT/"archive").glob("*/*/*.json"),reverse=True)[:180]:
        ars.append({"label":p.stem+" 日报","url":str(p.relative_to(ROOT)).replace("\\","/")})
    data["archive"]=ars
    (ROOT/"data"/"latest.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print("V5 generated",day,len(valid),"valid items","YT API",bool(YT_KEY))
if __name__=="__main__":main()
