---
name: video-downloader
description: 使用 yt-dlp 下载全网视频，支持 YouTube、Vimeo、Instagram、Twitter/X、TikTok、B站、抖音等 1000+ 平台。当用户提到"下载视频"、"download video"、"yt-dlp"、"YouTube下载"、"Vimeo下载"、"视频下载"、"批量下载"、"下载音频"时触发。
---

# 全网视频下载工具 (yt-dlp)

## 环境准备

```bash
# PATH 配置（每次使用前确认）
export PATH="$PATH:/Users/rain/Library/Python/3.9/bin"

# 验证安装
yt-dlp --version

# 更新到最新版
pip3 install -U yt-dlp
```

## 常用平台下载命令

### YouTube

```bash
# 下载最高画质（默认）
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# 指定格式：1080p MP4
yt-dlp -f "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]" "URL"

# 仅下载音频（MP3）
yt-dlp -x --audio-format mp3 "URL"

# 下载整个播放列表
yt-dlp --yes-playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# 下载字幕
yt-dlp --write-subs --sub-langs zh-Hans,en "URL"
```

### Vimeo

```bash
# 下载最高质量
yt-dlp "https://vimeo.com/VIDEO_ID"

# 指定分辨率
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "https://vimeo.com/VIDEO_ID"

# 私有视频（需提供密码）
yt-dlp --video-password "PASSWORD" "https://vimeo.com/VIDEO_ID"
```

### Instagram

```bash
# 帖子视频（需登录 Cookie）
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/p/POST_ID/"

# Reels
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/reel/REEL_ID/"

# 用户所有视频
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/USERNAME/videos/"
```

### TikTok / 抖音

```bash
# TikTok（无水印）
yt-dlp "https://www.tiktok.com/@user/video/VIDEO_ID"

# 抖音
yt-dlp "https://www.douyin.com/video/VIDEO_ID"
```

### Twitter / X

```bash
yt-dlp "https://twitter.com/user/status/TWEET_ID"
yt-dlp "https://x.com/user/status/TWEET_ID"
```

### B站

```bash
yt-dlp "https://www.bilibili.com/video/BV_CODE"
# 高清需 Cookie
yt-dlp --cookies-from-browser chrome "https://www.bilibili.com/video/BV_CODE"
```

---

## 通用参数速查

| 参数 | 说明 |
|------|------|
| `-o "%(title)s.%(ext)s"` | 自定义输出文件名 |
| `-P ~/Downloads` | 指定下载目录 |
| `-f bestvideo+bestaudio` | 最高画质 |
| `-f "best[height<=720]"` | 限制分辨率 |
| `--no-playlist` | 只下载当前视频，不下载整个列表 |
| `--write-thumbnail` | 同时下载封面图 |
| `--embed-subs` | 字幕嵌入视频 |
| `--proxy socks5://127.0.0.1:7890` | 使用代理 |
| `-N 4` | 多线程加速（4线程） |

---

## 查看可用格式

```bash
# 列出所有可下载格式（先用这个看清楚再下载）
yt-dlp -F "URL"
```

输出示例：
```
ID      EXT   RESOLUTION  NOTE
251     webm  audio only  128k
137     mp4   1920x1080   1080p
248     webm  1920x1080   1080p
```

然后用 `-f 137+251` 组合下载。

---

## 批量下载

```bash
# 从文件中读取 URL 列表
yt-dlp -a urls.txt

# urls.txt 格式（每行一个）:
# https://www.youtube.com/watch?v=xxx
# https://vimeo.com/xxx
```

---

## Cookie 认证（Instagram/B站/付费内容）

```bash
# 从浏览器自动读取（推荐）
yt-dlp --cookies-from-browser chrome "URL"
yt-dlp --cookies-from-browser firefox "URL"
yt-dlp --cookies-from-browser safari "URL"

# 手动导出 Cookie 文件（使用 cookies.txt 扩展）
yt-dlp --cookies cookies.txt "URL"
```

---

## 代理配置

```bash
# Clash/V2Ray 默认端口
yt-dlp --proxy socks5://127.0.0.1:7890 "URL"
yt-dlp --proxy http://127.0.0.1:7890 "URL"
```

---

## 常见问题

**下载失败/格式不支持**：先运行 `pip3 install -U yt-dlp` 更新

**Instagram 私密内容**：必须用 `--cookies-from-browser` 传入登录状态

**YouTube 高清**：需要 ffmpeg 合并音视频流 → `brew install ffmpeg` 或 `pip3 install ffmpeg-python`

**地区限制**：加 `--proxy` 参数指定代理
