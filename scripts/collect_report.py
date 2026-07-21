#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, time, hashlib, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
TZ=timezone(timedelta(hours=3))
UA={"User-Agent":"Mozilla/5.0 TrendReportBot/1.0"}

GLOBAL_QUERIES=[
("YouTube Shorts","AI工具","site:youtube.com/shorts AI tools shorts"),
("YouTube Shorts","知识科普","site:youtube.com/shorts science explained"),
("TikTok","生活反差","site:tiktok.com viral life story"),
("TikTok","挑战","site:tiktok.com challenge viral"),
("Instagram Reels","旅行","site:instagram.com/reel travel"),
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

def fetch(url:str)->bytes:
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=25) as r:return r.read()

def google_news(query:str):
    url="https://news.google.com/rss/search?q="+urllib.parse.quote(query)+"&hl=zh-CN&gl=US&ceid=US:zh-Hans"
    try:
        root=ET.fromstring(fetch(url))
        out=[]
        for it in root.findall(".//item")[:8]:
            title=(it.findtext("title") or "").strip()
            link=(it.findtext("link") or "").strip()
            source=(it.findtext("source") or "Google News RSS").strip()
            pub=(it.findtext("pubDate") or "").strip()
            out.append({"title":title,"url":link,"source":source,"published":pub})
        return out
    except Exception as e:
        return []

def classify_reason(cat,title):
    rules={
      "AI工具":"结果先行 + 效率对比 + 可复制流程",
      "知识科普":"反常识 + 单点结论 + 高信息密度",
      "生活反差":"真实感 + 文化差异 + 评论驱动",
      "挑战":"连续剧结构 + 悬念 + 结果验证",
      "旅行":"地点向往 + 镜头密度 + 收藏价值",
      "美食":"视觉满足 + 过程压缩 + 无语言门槛",
      "AI效率":"痛点明确 + 工作流演示 + 强实用性",
      "情绪共鸣":"强代入 + 留白 + 转发属性",
      "真实生活":"人物关系 + 真实记录 + 情绪价值",
      "乡村美食":"烟火气 + 完整过程 + 场景稀缺",
      "家庭教育":"家长共鸣 + 讨论性 + 熟人传播",
    }
    return rules.get(cat,"清晰钩子 + 快节奏 + 可讨论")

def build(queries,limit=10):
    pool=[]
    for platform,cat,q in queries:
        for x in google_news(q):
            key=hashlib.md5((x["title"]+x["url"]).encode()).hexdigest()
            pool.append({
              "id":key,"platform":platform,"category":cat,"title":x["title"][:120],
              "source":x["source"],"signal":"近期公开网页/RSS提及",
              "why":classify_reason(cat,x["title"]),
              "hook":"先展示结果，再解释过程","url":x["url"],"published":x["published"]
            })
        time.sleep(.4)
    seen=set();out=[]
    for x in pool:
        t=re.sub(r"\s+"," ",x["title"]).lower()
        if t in seen:continue
        seen.add(t);out.append(x)
        if len(out)>=limit:break
    while len(out)<limit:
        i=len(out)+1
        out.append({"platform":"公开数据不足","category":"待核验","title":f"第 {i} 位暂无足够公开证据",
        "source":"—","signal":"公开数据不可完整验证","why":"不编造排名","hook":"—","url":""})
    return out

def ideas(topcats):
    return [
      {"title":"同一选题的中外双版本实验","hook":"同一个故事，为什么中国版和海外版要用两种开头？","script":"先展示海外版：结果先行、字幕更少、视觉更强。再展示中国版：人物关系、情绪铺垫、结尾反转。最后给出改编公式：海外内容进入中国，加关系与情绪；中国内容走向海外，删铺垫、提前结果。"},
      {"title":"30秒判断短视频是否值得拍","hook":"别先看点赞，先看三个结构信号。","script":"第一，前三秒是否提出冲突；第二，每五秒是否有新信息；第三，结尾是否自然引导评论、收藏或转发。三项各十分，低于二十分先重写脚本。"},
      {"title":"四台设备组成24小时AI工作站","hook":"Mac、Windows、iPad和手机，怎样不再各自闲置？","script":"Mac负责创作，Windows负责自动化与兼容软件，iPad负责监控和远程控制，手机负责采集、通知和审批。四台设备不是四个工具，而是一套持续运行的AI系统。"}
    ]

def main():
    g=build(GLOBAL_QUERIES);c=build(CHINA_QUERIES)
    cats={}
    for x in g+c:
        if x["category"]!="待核验":cats[x["category"]]=cats.get(x["category"],0)+1
    top=max(cats,key=cats.get) if cats else "公开数据不足"
    now=datetime.now(TZ)
    data={
      "updated_at":now.strftime("%Y-%m-%d %H:%M"),
      "kpis":{"top_category":top,"top_category_note":"基于当日公开趋势信号出现频次",
      "cross_platform":"AI效率 / 真实生活 / 文化差异","data_status":"自动公开信号榜"},
      "summary":[
        "本报告通过公开网页、Google News RSS及可访问元数据生成趋势信号榜，不声称是各平台官方全量排行榜。",
        "TikTok、Instagram、抖音、快手和视频号缺少统一且稳定的开放排行榜接口；抓取失败或证据不足时，系统明确标注“公开数据不可完整验证”。",
        "网站每天土耳其时间16:00自动运行并保存历史归档；固定链接不改变。"
      ],
      "global_top10":g,"china_top10":c,"ideas":ideas(cats),
      "archive":[]
    }
    day=now.strftime("%Y-%m-%d")
    adir=ROOT/"archive"/now.strftime("%Y")/now.strftime("%m")
    adir.mkdir(parents=True,exist_ok=True)
    apath=adir/f"{day}.json"
    apath.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    # all archive json links
    ars=[]
    for p in sorted((ROOT/"archive").glob("*/*/*.json"), reverse=True)[:120]:
        ars.append({"label":p.stem+" 日报","url":str(p.relative_to(ROOT)).replace("\\","/")})
    data["archive"]=ars
    (ROOT/"data"/"latest.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print("generated",day,len(g),len(c))
if __name__=="__main__":main()
