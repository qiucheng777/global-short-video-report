# 全球短视频趋势中心

固定网站地址（开启 GitHub Pages 后）：

`https://qiucheng777.github.io/global-short-video-report/`

## 上传后开启网站

1. 仓库顶部进入 **Settings**
2. 左侧进入 **Pages**
3. Build and deployment 的 Source 选择 **Deploy from a branch**
4. Branch 选择 **main**，文件夹选择 **/(root)**
5. 点击 **Save**
6. 等待约 1–3 分钟后打开固定网址

## 自动更新时间

`.github/workflows/daily.yml` 已设置为每天土耳其时间 16:00 运行。

当前自动程序只更新时间标记，不会伪造 TikTok、Instagram、抖音等平台排名。正式榜单需要接入合法 API、公开榜单或人工审核后的数据，写入 `data/latest.json`。

## 修改日报

直接编辑：

`data/latest.json`

网页会自动读取最新内容，固定链接不变。
