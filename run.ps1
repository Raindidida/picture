# 抖音视频下载 + 镜头切分 - 一键脚本
# 使用方法：
#   1. 在 PowerShell 中运行: Set-ExecutionPolicy -Scope Process Bypass
#   2. 运行: E:\漫剧\run.ps1

param(
    [string]$VideoUrl = "https://www.douyin.com/video/7232222530164018492",
    [string]$OutputDir = "E:\漫剧\莉莉周视频",
    [string]$CookiesFile = "E:\漫剧\douyin_cookies.txt",
    [double]$SceneThreshold = 0.3  # 场景切换阈值(0-1)
)

$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
$env:PYTHONIOENCODING = "utf-8"

function Show-Banner {
    Write-Host ""
    Write-Host "=================================================" -ForegroundColor Cyan
    Write-Host "   抖音视频下载 + 镜头切分工具" -ForegroundColor Cyan  
    Write-Host "=================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Check-Tools {
    $ok = $true
    if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
        Write-Host "[错误] ffmpeg 未找到" -ForegroundColor Red
        $ok = $false
    }
    if (-not (Get-Command yt-dlp -ErrorAction SilentlyContinue)) {
        Write-Host "[错误] yt-dlp 未找到" -ForegroundColor Red
        $ok = $false
    }
    return $ok
}

function Get-Cookies {
    if (Test-Path $CookiesFile) {
        $lines = (Get-Content $CookiesFile | Where-Object { $_ -notmatch '^#' -and $_ -ne '' }).Count
        if ($lines -gt 0) {
            Write-Host "[OK] 找到cookies文件 ($lines 条记录)" -ForegroundColor Green
            return $true
        }
    }
    
    Write-Host ""
    Write-Host "需要抖音登录凭据(cookies)来下载视频" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "方法一 [推荐]: Chrome扩展自动导出" -ForegroundColor Cyan
    Write-Host "  1. 打开Chrome，安装扩展:"
    Write-Host "     https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc"
    Write-Host "  2. 访问 https://www.douyin.com 并登录账号"
    Write-Host "  3. 点击扩展图标 -> 点击 'Export' 按钮"
    Write-Host "  4. 另存为: $CookiesFile"
    Write-Host ""
    Write-Host "方法二: 关闭Chrome后自动提取" -ForegroundColor Cyan
    Write-Host "  1. 关闭所有Chrome窗口"
    Write-Host "  2. 重新运行此脚本，将自动读取Chrome中的抖音cookies"
    Write-Host ""
    
    $choice = Read-Host "是否尝试自动从Chrome提取cookies? (需关闭Chrome) [y/N]"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Write-Host "请关闭所有Chrome窗口后按回车继续..."
        Read-Host
        
        $result = python "E:\漫剧\extract_cookies.py" 2>&1
        $result | ForEach-Object { Write-Host $_ }
        
        if (Test-Path $CookiesFile) {
            $lines = (Get-Content $CookiesFile | Where-Object { $_ -notmatch '^#' -and $_ -ne '' }).Count
            if ($lines -gt 0) {
                Write-Host "[OK] Cookies提取成功 ($lines 条)" -ForegroundColor Green
                return $true
            }
        }
    }
    
    Write-Host ""
    Write-Host "请手动导出cookies后重新运行此脚本" -ForegroundColor Red
    return $false
}

function Download-Video {
    param([string]$url, [string]$outputDir, [string]$cookies)
    
    Write-Host ""
    Write-Host "[步骤 1/3] 下载视频..." -ForegroundColor Green
    
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    
    $args = @(
        "--no-playlist",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", "$outputDir\original_video.%(ext)s",
        "--merge-output-format", "mp4"
    )
    
    if (Test-Path $cookies) {
        $args += @("--cookies", $cookies)
    }
    
    $args += $url
    
    & yt-dlp @args 2>&1 | ForEach-Object { Write-Host "  $_" }
    
    $videoFile = Get-ChildItem $outputDir -Filter "original_video.*" | Select-Object -First 1
    if (-not $videoFile) {
        Write-Host "[错误] 下载失败" -ForegroundColor Red
        return $null
    }
    
    Write-Host "[OK] 下载完成: $($videoFile.Name)" -ForegroundColor Green
    return $videoFile.FullName
}

function Split-Scenes {
    param([string]$videoPath, [string]$outputDir, [double]$threshold)
    
    Write-Host ""
    Write-Host "[步骤 2/3] 检测场景切换点..." -ForegroundColor Green
    
    # 获取视频时长
    $duration = [double](ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$videoPath" 2>&1 | Where-Object { $_ -match '^\d' } | Select-Object -First 1)
    Write-Host "  视频时长: $([Math]::Round($duration, 2)) 秒"
    
    # 检测场景
    $sceneOutput = ffmpeg -i "$videoPath" -vf "select='gt(scene,$threshold)',showinfo" -vsync vfr -f null - 2>&1
    
    $timestamps = @(0.0)
    $timePattern = 'pts_time:(\d+(?:\.\d+)?)'
    foreach ($line in $sceneOutput) {
        if ($line -match $timePattern) {
            $t = [double]$matches[1]
            if ($t -gt 0.5) {
                $timestamps += $t
            }
        }
    }
    $timestamps = ($timestamps | Sort-Object -Unique)
    $timestamps += $duration
    
    $shotCount = $timestamps.Count - 1
    Write-Host "  检测到 $shotCount 个镜头" -ForegroundColor Yellow
    
    # 切分镜头
    Write-Host ""
    Write-Host "[步骤 3/3] 切分镜头..." -ForegroundColor Green
    
    $shotsDir = "$outputDir\shots"
    New-Item -ItemType Directory -Path $shotsDir -Force | Out-Null
    
    for ($i = 0; $i -lt ($timestamps.Count - 1); $i++) {
        $startTime = $timestamps[$i]
        $endTime = $timestamps[$i + 1]
        $dur = $endTime - $startTime
        $shotNum = ($i + 1).ToString("D3")
        $outputFile = "$shotsDir\shot_${shotNum}.mp4"
        
        $pct = [Math]::Round(($i + 1) / $shotCount * 100)
        Write-Host "  [$pct%] 镜头 $shotNum: $([Math]::Round($startTime,2))s - $([Math]::Round($endTime,2))s ($([Math]::Round($dur,2))s)"
        
        ffmpeg -y -ss $startTime -i "$videoPath" -t $dur `
            -c:v libx264 -preset fast -crf 18 -c:a aac `
            -avoid_negative_ts make_zero "$outputFile" 2>$null
    }
    
    return $shotCount
}

# ===== 主流程 =====
Show-Banner

if (-not (Check-Tools)) {
    Write-Host "请先安装缺失的工具后重试" -ForegroundColor Red
    exit 1
}

if (-not (Get-Cookies)) {
    exit 1
}

$videoFile = Download-Video -url $VideoUrl -outputDir $OutputDir -cookies $CookiesFile
if (-not $videoFile) { exit 1 }

$shotCount = Split-Scenes -videoPath $videoFile -outputDir $OutputDir -threshold $SceneThreshold

Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
Write-Host "   完成！" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "  原始视频: $videoFile" -ForegroundColor White
Write-Host "  镜头目录: $OutputDir\shots\" -ForegroundColor White
Write-Host "  镜头数量: $shotCount 个" -ForegroundColor Yellow
Write-Host ""
Start-Process "explorer.exe" "$OutputDir\shots"
