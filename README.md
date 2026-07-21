# AI 全球短视频情报中心 V10

固定网址：

`https://qiucheng777.github.io/global-short-video-report/`

## 已实现

- 国内外短视频趋势榜
- YouTube 官方 API 支持
- 公开视频指标和缩略图
- 自动去重、失败重试和数据降级
- AI 脚本、标题、标签与创作任务
- 竞品账号监控配置
- 日报、周报、月报、季报、年报
- 历史情报归档
- 每天土耳其时间 16:00 自动更新

## 覆盖升级

将本压缩包解压后，把全部内容上传到原仓库根目录并覆盖。

工作流文件必须位于：

`.github/workflows/daily.yml`

上传后运行：

`Actions → Update AI global short-video intelligence V10 → Run workflow`

## YouTube 官方数据

在仓库：

`Settings → Secrets and variables → Actions → New repository secret`

添加：

`YOUTUBE_API_KEY`

## 竞品监控

编辑：

`config/competitors.json`

自动发布到 YouTube、TikTok、Instagram、抖音等平台，需要各平台官方开发者权限和账号授权。当前版本不会在未授权情况下自动发布。
