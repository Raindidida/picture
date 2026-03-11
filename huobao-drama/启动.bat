@echo off
chcp 65001 >nul
echo ========================================
echo   火宝短剧 - 启动脚本
echo ========================================
echo.

set "FFMPEG_PATH=C:\Users\1212\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
set "GO_PATH=C:\Program Files\Go\bin"
set "NODE_PATH=C:\Program Files\nodejs"

echo [1/2] 启动后端服务 (端口 5678)...
start "火宝短剧-后端" cmd /k "set PATH=%GO_PATH%;%FFMPEG_PATH%;%NODE_PATH%;%PATH% && cd /d E:\漫剧\huobao-drama && go run main.go"

echo 等待后端启动 (8秒)...
timeout /t 8 /nobreak >nul

echo [2/2] 启动前端服务 (端口 3012)...
start "火宝短剧-前端" cmd /k "cd /d E:\漫剧\huobao-drama\web && \"%NODE_PATH%\npm.cmd\" run dev"

echo.
echo ========================================
echo  启动完成！请在浏览器中访问：
echo  http://localhost:3012
echo ========================================
echo.
start http://localhost:3012
pause
