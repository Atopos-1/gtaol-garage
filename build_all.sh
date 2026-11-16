#!/usr/bin/env bash
# 一键构建 GTAOL 载具收藏
# 用法：./build_all.sh
# 前置：JDK 17/21、Android SDK（compileSdk 34）、Python 3
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$ROOT/tools"
APP="$ROOT/app"

echo "==> [1/4] 抓取载具列表与详情（约 900 辆，需联网）"
cd "$TOOLS"
python fetch_vehicles.py
python fetch_details.py

echo "==> [2/4] 下载车辆缩略图"
python fetch_images.py

echo "==> [3/4] 整合数据 + 生成页面"
python build_data.py
python render_app.py

echo "==> 移动图片到 app assets"
mkdir -p "$APP/src/main/assets/img"
cp "$TOOLS/assets/img/"*.webp "$APP/src/main/assets/img/" 2>/dev/null || true

echo "==> [4/4] 编译 APK"
cd "$ROOT"
./gradlew assembleRelease

echo ""
echo "完成！APK 位于：app/build/outputs/apk/release/app-release.apk"
