# GTAOL 载具收藏（gtaol-garage）

一个离线可用的《GTA Online》载具图鉴与「已购 / 未购」登记工具，安卓 App + 网页版。

## 功能

- 收录 900+ 辆 GTA Online 载具，官方简体中文译名
- 每辆车带：厂商、类别、座位、驱动、DLC、价格、批发价、购买地点、性能（极速/加速/刹车/操控）、车辆介绍、现实原型、实拍图
- 手动登记「已购买 / 未购买」，进度统计
- 四套主题切换（Material You / 浅色 / 深色 / 暖色），毛玻璃 + 液态玻璃材质
- 数据存原生 SharedPreferences，升级不丢记录
- WebDAV 云备份（坚果云、Nextcloud 等），备份/恢复一键完成
- 中英搜索、分类筛选、导出/导入 JSON 备份

## 技术栈

- Android：原生 WebView 壳（Java），页面是单文件 HTML + 内嵌数据
- 无第三方运行时依赖，构建只需 Android SDK + JDK 17

## 目录结构

```
gtaol-garage/
├── app/                      # Android 应用模块
│   ├── build.gradle
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/gtaol/garage/   # MainActivity + WebBridge
│       └── res/                     # 图标、样式
├── tools/                    # 数据/图片抓取与构建脚本
├── build_all.(sh|bat)        # 一键构建
├── LICENSE                   # MIT
└── README.md
```

## 构建方法

### 前置条件

- JDK 17（或 21）
- Android SDK（compileSdk 34、build-tools 34.0.0）
- 网络（首次构建拉取 Gradle 依赖；构建数据需访问第三方源）

### 一键构建

```bash
# Linux / macOS
./build_all.sh

# Windows
build_all.bat
```

脚本会依次：① 抓取载具数据 → ② 下载车辆缩略图 → ③ 生成页面 → ④ 编译 APK。

### 手动构建

1. 运行 `tools/` 下的抓取脚本，生成 `vehicles_compact.json` 和 `assets/img/` 图片
2. 运行生成脚本，产出 `app/src/main/assets/index.html`
3. 把图片放进 `app/src/main/assets/img/`
4. 执行 `./gradlew assembleRelease`

### 签名

`assembleRelease` 默认产出**未签名** APK（`app-release-unsigned.apk`），可直接用于学习，但无法直接安装。

要产出可安装包，二选一：

1. **用 debug 签名快速出包**：执行 `./gradlew assembleDebug`，产物 `app-debug.apk` 已用 debug keystore 签名，可直接装到手机。
2. **配自己的 release keystore**：生成 keystore 后，在 `app/build.gradle` 里加 `signingConfigs.release` 并引用；keystore 文件与密码**不要提交**（已加入 `.gitignore`）。

## 数据来源与版权声明

本项目**只开源代码**（MIT License）。代码内嵌的载具数据与车辆图片**不随仓库分发**，需通过 `tools/` 脚本自行抓取。

- 载具名称、参数、介绍等数据，来源于公开的 GTA 中文数据库（antwen.cn 等）与 GTA 中文维基
- 车辆图片版权归原站点 / 原作者所有
- 本项目与 Rockstar Games、Take-Two Interactive 无任何关联，GTA、Grand Theft Auto 等均为其商标

**请勿将抓取到的数据/图片用于商业用途。** 仅建议个人学习使用。

## 许可证

代码部分：MIT License（见 [LICENSE](LICENSE)）。
数据与图片：版权归各自原作者所有，不适用本仓库的 MIT 许可。

## 免责声明

本项目仅供学习交流，使用第三方数据与图片请自行确认合规性。由此产生的任何责任由使用者自行承担。
