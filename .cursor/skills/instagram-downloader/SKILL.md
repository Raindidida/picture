---
name: instagram-downloader
description: 专门下载 Instagram 内容，包括帖子视频、Reels、Stories、合集、用户主页所有视频。支持批量下载和私人账号内容（需 Cookie 认证）。当用户提到"下载ins视频"、"Instagram下载"、"下载Reels"、"ins帖子"、"Instagram Stories"时触发。
---

# Instagram 视频下载专项

## 基础命令

```bash
export PATH="$PATH:/Users/rain/Library/Python/3.9/bin"

# 所有 Instagram 内容都需要登录态，始终加 --cookies-from-browser
yt-dlp --cookies-from-browser chrome "INSTAGRAM_URL"
```

## 各类型内容下载

### 帖子（Post）/ Reels

```bash
# 单个帖子
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/p/POST_ID/"

# Reels
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/reel/REEL_ID/"
```

### Stories

```bash
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/stories/USERNAME/STORY_ID/"
```

### 用户主页批量下载

```bash
# 下载某用户所有视频
yt-dlp --cookies-from-browser chrome \
  -o "%(uploader)s/%(upload_date)s_%(title)s.%(ext)s" \
  "https://www.instagram.com/USERNAME/"

# 只下载最新 20 个
yt-dlp --cookies-from-browser chrome \
  --playlist-end 20 \
  "https://www.instagram.com/USERNAME/"
```

### 合集 / Highlights

```bash
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/stories/highlights/HIGHLIGHT_ID/"
```

---

## 输出格式建议

```bash
# 按用户名和日期整理文件夹
yt-dlp --cookies-from-browser chrome \
  -o "~/Downloads/Instagram/%(uploader)s/%(upload_date)s_%(id)s.%(ext)s" \
  "URL"
```

---

## 如果 Chrome Cookie 无效

```bash
# 尝试 Safari
yt-dlp --cookies-from-browser safari "URL"

# 或手动导出：
# 1. 安装 Chrome 扩展 "Get cookies.txt LOCALLY"
# 2. 在 instagram.com 页面导出 cookies.txt
# 3. 使用文件
yt-dlp --cookies ~/cookies.txt "URL"
```

---

## 常见错误

| 错误 | 解决方案 |
|------|---------|
| `Requested format is not available` | 帖子可能是图片，不含视频 |
| `Login required` | 补充 `--cookies-from-browser chrome` |
| `HTTP Error 401` | Cookie 已过期，重新登录 Instagram 后再试 |
| `Private profile` | 必须是该账号的关注者且 Cookie 有效 |
