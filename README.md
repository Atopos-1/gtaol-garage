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

## 数据来源与版权声明

本项目**开源代码**（MIT License），并随仓库附带载具数据（`vehicles_compact.json`）与车辆图片（`app/src/main/assets/img/`，通过 **Git LFS** 存储）。

- 载具名称、参数、介绍等数据，来源于公开的 GTA 中文数据库（antwen.cn 等）与 GTA 中文维基
- **图片版权归原站点 / 原作者所有**，本项目仅作学习交流用途收集整理
- 若原作者认为侵权，请提 Issue 或邮件联系，我会立即删除相关图片
- 本项目与 Rockstar Games、Take-Two Interactive 无任何关联，GTA、Grand Theft Auto 等均为其商标

**请勿将本项目附带的数据/图片用于商业用途。** 仅建议个人学习使用。

> ⚠️ 使用 Git LFS：克隆前请先安装 [Git LFS](https://git-lfs.com/)，然后 `git lfs install` 再 `git clone`。否则图片将只是指针文件。

## 许可证

代码部分：MIT License（见 [LICENSE](LICENSE)）。
数据与图片：版权归各自原作者所有，不适用本仓库的 MIT 许可。

## 免责声明

本项目仅供学习交流，使用第三方数据与图片请自行确认合规性。由此产生的任何责任由使用者自行承担。
