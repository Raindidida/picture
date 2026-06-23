---
name: threads-downloader
description: 下载 Threads（threads.com）视频和图片，支持帖子 URL 或 shortcode。通过 Instagram API + Chrome Cookie 认证实现。当用户提到"下载Threads视频"、"threads下载"、"threads.com"、"下载帖子视频"时触发。
---

# Threads 视频下载

## 依赖安装

```bash
pip3 install browser-cookie3 requests
```

> 需要 Chrome 浏览器已登录 Instagram 账号（Threads 共享 Instagram 登录）

## 快速使用

```bash
# 下载视频（传 URL 或 shortcode）
python3 .cursor/skills/threads-downloader/scripts/download_threads.py \
  "https://www.threads.com/@username/post/SHORTCODE"

# 指定输出目录
python3 .cursor/skills/threads-downloader/scripts/download_threads.py \
  "https://www.threads.com/@username/post/SHORTCODE" ~/Movies
```

## 技术原理

Threads 使用 Instagram 的媒体 API，流程：
1. 从 Chrome 读取 `.instagram.com` 的 `sessionid` Cookie
2. 将 URL shortcode 转换为数字 media_id（Base64 解码）
3. 调用 `https://www.instagram.com/api/v1/media/{id}/info/`
4. 提取最高画质 `video_versions[0].url` 并下载

## 手动调用（agent 执行）

当用户粘贴 Threads URL 时，直接运行：

```bash
export PATH="$PATH:/Users/rain/Library/Python/3.9/bin"
python3 /Users/rain/Documents/cusor/picture/.cursor/skills/threads-downloader/scripts/download_threads.py "用户提供的URL"
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `KeyError` in ALPHABET | shortcode 含非标准字符 | 检查 URL 是否完整 |
| `401 / 403` | Cookie 过期 | 重新登录 Instagram 后重试 |
| `items 为空` | 私密账号 / 纯图片帖 | 确认已关注该账号 |
| `browser_cookie3` 报错 | Chrome 未关闭 | 关闭 Chrome 再运行，或用 `--cookies` 文件 |
