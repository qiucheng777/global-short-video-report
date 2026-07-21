# 全球短视频趋势中心 V5

固定地址：

`https://qiucheng777.github.io/global-short-video-report/`

## V5 新增

- YouTube Data API 官方公开视频指标
- 视频缩略图
- 自动去重
- 网络失败自动重试
- 周/月/季/年趋势汇总
- 历史归档
- 数据不足明确标注
- 每天土耳其时间 16:00 自动运行

## 覆盖安装

将本压缩包解压后，把所有文件上传到原仓库根目录并覆盖同名文件。

## 创建工作流

文件路径必须是：

`.github/workflows/daily.yml`

如果 Windows 看不到 `.github`，请使用 GitHub 网页：

`Add file → Create new file`

然后输入上述完整路径，再粘贴 `WORKFLOW_SETUP/daily.yml` 的内容。

## 可选：接入 YouTube 官方 API

仓库进入：

`Settings → Secrets and variables → Actions → New repository secret`

名称：

`YOUTUBE_API_KEY`

值：

你在 Google Cloud Console 创建的 YouTube Data API v3 密钥。

不配置密钥时，系统仍会使用公开 RSS 趋势信号运行，但 YouTube 不会显示官方播放量、点赞量和评论量。

## 首次运行

`Actions → Update global short-video report V5 → Run workflow`
