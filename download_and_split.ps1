# 抖音视频下载 + 镜头切分脚本
# 用法：先按照下面说明获取cookies.txt，然后运行此脚本

$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

# ===== 配置 =====
$VIDEO_URL = "https://www.douyin.com/video/7232222530164018492"
$OUTPUT_DIR = "E:\漫剧\莉莉周视频"
$COOKIES_FILE = "E:\漫剧\douyin_cookies.txt"
$SCENE_THRESHOLD = 30  # 场景切换敏感度(0-100，越小越敏感)

# ===== 检查cookies文件 =====
if (-not (Test-Path $COOKIES_FILE)) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  需要先获取抖音cookies！" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "请按以下步骤操作：" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "方法一：使用Chrome扩展（推荐）" -ForegroundColor Cyan
    Write-Host "  1. 在Chrome中安装扩展: 'Get cookies.txt LOCALLY'" -ForegroundColor White
    Write-Host "     地址: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
    Write-Host "  2. 在Chrome中打开并登录抖音: https://www.douyin.com"
    Write-Host "  3. 点击扩展图标，选择 'Export' 导出cookies"
    Write-Host "  4. 保存文件为: $COOKIES_FILE"
    Write-Host ""
    Write-Host "方法二：使用Edge扩展" -ForegroundColor Cyan
    Write-Host "  1. 在Edge中安装: 'EditThisCookie' 或 'Cookie Editor'"
    Write-Host "  2. 登录抖音后导出Netscape格式cookies"
    Write-Host "  3. 保存到: $COOKIES_FILE"
    Write-Host ""
    Write-Host "获取cookies后，重新运行此脚本即可。" -ForegroundColor Green
    exit 1
}

# ===== 创建输出目录 =====
New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null

# ===== 步骤1：下载视频 =====
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  步骤 1/3: 下载视频" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$downloadOutput = yt-dlp --cookies $COOKIES_FILE `
    --no-playlist `
    -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" `
    -o "$OUTPUT_DIR\original_video.%(ext)s" `
    $VIDEO_URL 2>&1

$downloadOutput | ForEach-Object { Write-Host $_ }

# 查找下载的视频文件
$videoFile = Get-ChildItem $OUTPUT_DIR -Filter "original_video.*" | Select-Object -First 1
if (-not $videoFile) {
    Write-Host "下载失败，请检查cookies是否有效" -ForegroundColor Red
    exit 1
}
$videoPath = $videoFile.FullName
Write-Host "视频下载完成: $videoPath" -ForegroundColor Green

# ===== 步骤2：检测场景切换点 =====
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  步骤 2/3: 检测镜头切换点" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# 用ffmpeg的场景检测过滤器
$scenesFile = "$OUTPUT_DIR\scenes.txt"
$ffmpegFilter = "select='gt(scene,$($SCENE_THRESHOLD/100))',showinfo"

Write-Host "正在分析视频场景..."
$ffmpegOutput = ffmpeg -i $videoPath -vf "select='gt(scene,$($SCENE_THRESHOLD/100))',showinfo" -vsync vfr -f null - 2>&1
$ffmpegOutput | Out-File -FilePath $scenesFile -Encoding UTF8

# 解析时间戳
$timestamps = @(0.0)  # 从0开始
$timePattern = 'pts_time:(\d+\.?\d*)'
$matches = [regex]::Matches($ffmpegOutput -join "`n", $timePattern)
foreach ($m in $matches) {
    $t = [double]$m.Groups[1].Value
    $timestamps += $t
}
$timestamps = $timestamps | Sort-Object -Unique

# 获取视频总时长
$durationOutput = ffprobe -v quiet -show_entries format=duration -of csv=p=0 $videoPath 2>&1
$totalDuration = [double]($durationOutput -match '^\d' | Select-Object -First 1)
if ($totalDuration -gt 0) { $timestamps += $totalDuration }

Write-Host "检测到 $($timestamps.Count - 1) 个镜头" -ForegroundColor Yellow

# ===== 步骤3：切分视频 =====
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  步骤 3/3: 切分镜头" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

$shotsDir = "$OUTPUT_DIR\shots"
New-Item -ItemType Directory -Path $shotsDir -Force | Out-Null

for ($i = 0; $i -lt $timestamps.Count - 1; $i++) {
    $startTime = $timestamps[$i]
    $endTime = $timestamps[$i + 1]
    $duration = $endTime - $startTime
    $shotNum = ($i + 1).ToString("D3")
    $outputFile = "$shotsDir\shot_${shotNum}.mp4"
    
    Write-Host "切分镜头 $shotNum/$($timestamps.Count - 1): $([Math]::Round($startTime,2))s - $([Math]::Round($endTime,2))s"
    
    ffmpeg -y -ss $startTime -i $videoPath -t $duration `
        -c:v libx264 -c:a aac -avoid_negative_ts make_zero `
        $outputFile 2>$null
}

# ===== 完成 =====
$shotCount = (Get-ChildItem $shotsDir -Filter "*.mp4").Count
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "原始视频: $videoPath" -ForegroundColor White
Write-Host "镜头片段: $shotsDir" -ForegroundColor White
Write-Host "共切分出 $shotCount 个镜头" -ForegroundColor Yellow
