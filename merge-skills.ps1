# ============================================================
# Cursor Skills 合并脚本
# 用途：把家里电脑（GitHub 仓库）的 skills 合并到本机，去重不覆盖
# 使用前提：已将 personal-skill 仓库 Clone 到本地
# ============================================================

$repoPath   = "C:\Users\Mayn\Documents\GitHub\personal-skill"  # Clone 的仓库路径
$localSkills = "C:\Users\Mayn\.cursor\skills"                   # 本机 skills 目录

# 检查路径是否存在
if (-not (Test-Path $repoPath)) {
    Write-Host ""
    Write-Host "❌ 找不到仓库目录：$repoPath" -ForegroundColor Red
    Write-Host "   请先在 GitHub Desktop 中 Clone 你的 personal-skill 仓库" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

if (-not (Test-Path $localSkills)) {
    Write-Host ""
    Write-Host "❌ 找不到本机 skills 目录：$localSkills" -ForegroundColor Red
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Cursor Skills 合并工具" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "来源（家里仓库）：$repoPath"
Write-Host "目标（本机）    ：$localSkills"
Write-Host ""

$added   = 0
$skipped = 0
$addedList = @()

# ---- 第一步：把仓库里的 skills 合并到本机（不覆盖已有） ----
Write-Host "【第一步】将仓库 skills 合并到本机..." -ForegroundColor White
Write-Host ""

Get-ChildItem $repoPath -Directory | ForEach-Object {
    $skillName = $_.Name
    $destPath  = Join-Path $localSkills $skillName

    if (Test-Path $destPath) {
        Write-Host "  跳过（本机已有）: $skillName" -ForegroundColor DarkGray
        $skipped++
    } else {
        Copy-Item $_.FullName -Destination $destPath -Recurse
        Write-Host "  ✅ 新增: $skillName" -ForegroundColor Green
        $added++
        $addedList += $skillName
    }
}

Write-Host ""
Write-Host "第一步完成：新增 $added 个，跳过 $skipped 个（已存在）" -ForegroundColor Cyan
Write-Host ""

# ---- 第二步：把本机独有的 skills 同步回仓库 ----
Write-Host "【第二步】将本机独有 skills 同步到仓库..." -ForegroundColor White
Write-Host ""

$syncBack  = 0
$syncList  = @()

Get-ChildItem $localSkills -Directory | ForEach-Object {
    $skillName = $_.Name
    $destPath  = Join-Path $repoPath $skillName

    if (-not (Test-Path $destPath)) {
        Copy-Item $_.FullName -Destination $destPath -Recurse
        Write-Host "  ✅ 同步到仓库: $skillName" -ForegroundColor Blue
        $syncBack++
        $syncList += $skillName
    }
}

Write-Host ""
Write-Host "第二步完成：同步到仓库 $syncBack 个新 skill" -ForegroundColor Cyan
Write-Host ""

# ---- 汇总报告 ----
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  合并完成！汇总报告" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  从仓库新增到本机：$added 个" -ForegroundColor Green
Write-Host "  从本机同步到仓库：$syncBack 个" -ForegroundColor Blue
Write-Host "  跳过重复项      ：$skipped 个" -ForegroundColor DarkGray
Write-Host ""

if ($syncBack -gt 0) {
    Write-Host "⚠️  下一步操作：" -ForegroundColor Yellow
    Write-Host "   打开 GitHub Desktop → 选择 personal-skill 仓库" -ForegroundColor Yellow
    Write-Host "   可以看到新增的文件 → 填写 Commit 消息 → Commit → Push" -ForegroundColor Yellow
    Write-Host "   这样家里的电脑 Pull 后也能同步这些 skills" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "按任意键退出..." -ForegroundColor DarkGray
pause
