#!/usr/bin/env python3
"""
Threads 视频下载脚本
用法: python3 download_threads.py <threads_url_or_shortcode> [输出目录]

示例:
  python3 download_threads.py https://www.threads.com/@zayn_film/post/DXJvpHpE_Al
  python3 download_threads.py DXJvpHpE_Al ~/Movies
"""

import sys
import os
import re
import browser_cookie3
import requests

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def shortcode_to_id(code: str) -> int:
    return sum(ALPHABET.index(c) * (64 ** i) for i, c in enumerate(reversed(code)))


def extract_shortcode(url_or_code: str) -> str:
    m = re.search(r"/post/([A-Za-z0-9_-]+)", url_or_code)
    return m.group(1) if m else url_or_code.strip("/").split("/")[-1]


def build_session() -> tuple[requests.Session, dict]:
    cj = browser_cookie3.chrome(domain_name=".instagram.com")
    cookies = {c.name: c.value for c in cj}
    session = requests.Session()
    for name, value in cookies.items():
        session.cookies.set(name, value, domain=".instagram.com")
    return session, cookies


def fetch_video_info(session: requests.Session, cookies: dict, media_id: int) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "X-IG-App-ID": "238260118697367",
        "X-CSRFToken": cookies.get("csrftoken", ""),
        "Referer": "https://www.instagram.com/",
    }
    r = session.get(
        f"https://www.instagram.com/api/v1/media/{media_id}/info/",
        headers=headers,
    )
    r.raise_for_status()
    data = r.json()
    items = data.get("items", [])
    if not items:
        raise ValueError("API 返回空 items，帖子可能是私密账号或不含视频")
    return items[0], headers


def download_video(session, headers, url, output_path):
    r = session.get(url, headers=headers, stream=True)
    r.raise_for_status()
    total = int(r.headers.get("content-length", 0))
    downloaded = 0
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
            downloaded += len(chunk)
            if total:
                pct = downloaded / total * 100
                print(f"\r  {pct:.1f}% ({downloaded//1024//1024}MB/{total//1024//1024}MB)", end="", flush=True)
    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_arg = sys.argv[1]
    output_dir = os.path.expanduser(sys.argv[2]) if len(sys.argv) > 2 else os.path.expanduser("~/Downloads")
    os.makedirs(output_dir, exist_ok=True)

    shortcode = extract_shortcode(input_arg)
    media_id = shortcode_to_id(shortcode)
    print(f"Shortcode: {shortcode}  →  Media ID: {media_id}")

    print("读取 Chrome Cookie...")
    session, cookies = build_session()

    print("请求视频信息...")
    item, headers = fetch_video_info(session, cookies, media_id)

    user = item.get("user", {}).get("username", "unknown")
    video_versions = item.get("video_versions", [])

    if not video_versions:
        print("❌ 该帖子不含视频（可能是纯图片帖）")
        # 尝试下载图片
        images = item.get("image_versions2", {}).get("candidates", [])
        if images:
            best_img = max(images, key=lambda x: x.get("width", 0) * x.get("height", 0))
            out = os.path.join(output_dir, f"threads_{shortcode}.jpg")
            print(f"下载图片 {best_img['width']}x{best_img['height']}...")
            download_video(session, headers, best_img["url"], out)
            print(f"✅ 图片保存: {out}")
        sys.exit(0)

    # 选最高分辨率（三个版本分辨率相同时取第一个）
    best = max(video_versions, key=lambda v: v.get("width", 0) * v.get("height", 0))
    w, h = best.get("width", 0), best.get("height", 0)
    video_url = best["url"]

    out_path = os.path.join(output_dir, f"threads_{user}_{shortcode}.mp4")
    print(f"用户: @{user}")
    print(f"画质: {w}x{h}")
    print(f"下载到: {out_path}")

    download_video(session, headers, video_url, out_path)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"✅ 完成！文件大小: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
