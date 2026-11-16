@echo off
REM 一键构建 GTAOL 载具收藏（Windows）
REM 用法：build_all.bat
REM 前置：JDK 17/21、Android SDK（compileSdk 34）、Python 3

setlocal enabledelayedexpansion
set ROOT=%~dp0
set TOOLS=%ROOT%tools
set APP=%ROOT%app

echo ==^> [1/4] 抓取载具列表与详情（约 900 辆，需联网）
cd /d "%TOOLS%"
python fetch_vehicles.py || goto :err
python fetch_details.py || goto :err

echo ==^> [2/4] 下载车辆缩略图
python fetch_images.py || goto :err

echo ==^> [3/4] 整合数据 + 生成页面
python build_data.py || goto :err
python render_app.py || goto :err

echo ==^> 移动图片到 app assets
if not exist "%APP%\src\main\assets\img" mkdir "%APP%\src\main\assets\img"
copy /Y "%TOOLS%\assets\img\*.webp" "%APP%\src\main\assets\img\" >nul 2>&1

echo ==^> [4/4] 编译 APK
cd /d "%ROOT%"
call gradlew.bat assembleRelease || goto :err

echo.
echo 完成！APK 位于：app\build\outputs\apk\release\app-release.apk
goto :eof

:err
echo 构建失败，请检查上方错误信息。
exit /b 1
