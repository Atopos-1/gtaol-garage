import json, re

data = json.load(open("vehicles_compact.json", encoding="utf-8"))

def safe_name(m):
    s = "".join(c for c in (m or "") if c.isalnum() or c in "-_")
    return s or None

for x in data:
    sn = safe_name(x.get("m"))
    x["_img"] = ("img/" + sn + ".webp") if sn else None

data_js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#F6F2FB">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>GTAOL 载具收藏</title>
<style>
  /* ================================================================
     主题变量 —— Material You 风格（默认）+ 浅色 + 深色 + 暖色
     质感：elevation 阴影层级 / 大圆角 / 顺滑过渡
  ================================================================ */
  :root{
    /* Material 原生（Material You 柔紫） */
    --bg:#f6f2fb; --surface:#ffffff; --surface2:#f2ebf9; --surface3:#e9e0f4; --field:#f2ebf9;
    --outline:#e3dbea; --outline-strong:#cac1d6;
    --txt:#1d192b; --dim:#6f6580; --dim2:#a89cb8; --icon:#d3c8e2;
    --primary:#6750a4; --on-primary:#ffffff; --primary-soft:rgba(103,80,164,.12);
    --grad:linear-gradient(135deg,#6750a4,#8f6fd0);
    --on-accent:#ffffff; --check:#b9aed0;
    --shadow-1:0 1px 2px rgba(0,0,0,.05),0 1px 3px rgba(0,0,0,.07);
    --shadow-2:0 2px 6px rgba(0,0,0,.07),0 6px 18px rgba(0,0,0,.06);
    --shadow-3:0 8px 20px rgba(0,0,0,.12),0 16px 40px rgba(0,0,0,.10);
    --header-bg:rgba(246,242,251,.90);
    --toast-bg:#1d192b; --toast-txt:#ffffff;
    --ok:#00b96a; --ok-soft:rgba(0,185,106,.12);
    --warn:#f5b301; --bad:#e5484d; --info:#2f7fd0;
  }
  body[data-theme="light"]{
    --bg:#f4f6f9; --surface:#ffffff; --surface2:#f0f2f6; --surface3:#e7ebf1; --field:#f0f2f6;
    --outline:#e3e7ed; --outline-strong:#c8d0da;
    --txt:#1b2430; --dim:#667386; --dim2:#97a2b0; --icon:#c8d0da;
    --primary:#00b96a; --on-primary:#ffffff; --primary-soft:rgba(0,185,106,.12);
    --grad:linear-gradient(135deg,#00b96a,#2ee6a8);
    --on-accent:#ffffff; --check:#bdc6d2;
    --shadow-1:0 1px 2px rgba(0,0,0,.05),0 1px 3px rgba(0,0,0,.07);
    --shadow-2:0 2px 6px rgba(0,0,0,.07),0 6px 18px rgba(0,0,0,.06);
    --shadow-3:0 8px 20px rgba(0,0,0,.12),0 16px 40px rgba(0,0,0,.10);
    --header-bg:rgba(244,246,249,.90);
    --toast-bg:#1b2430; --toast-txt:#ffffff;
    --ok:#00b96a; --ok-soft:rgba(0,185,106,.12);
    --warn:#f5b301; --bad:#e5484d; --info:#2f7fd0;
  }
  body[data-theme="dark"]{
    --bg:#141821; --surface:#1d222d; --surface2:#242a37; --surface3:#2c3341; --field:#202633;
    --outline:#323a48; --outline-strong:#455061;
    --txt:#eef1f6; --dim:#8b96a6; --dim2:#5f6a78; --icon:#3a4352;
    --primary:#9a82db; --on-primary:#1d192b; --primary-soft:rgba(154,130,219,.18);
    --grad:linear-gradient(135deg,#8f6fd0,#a98ce8);
    --on-accent:#1d192b; --check:#495362;
    --shadow-1:0 1px 2px rgba(0,0,0,.4);
    --shadow-2:0 2px 8px rgba(0,0,0,.45);
    --shadow-3:0 10px 28px rgba(0,0,0,.5);
    --header-bg:rgba(20,24,33,.90);
    --toast-bg:#eef1f6; --toast-txt:#141821;
    --ok:#00c16e; --ok-soft:rgba(0,193,110,.16);
    --warn:#f5b301; --bad:#e5484d; --info:#7ac8ff;
  }
  body[data-theme="warm"]{
    --bg:#f8f2e7; --surface:#fffdf7; --surface2:#f3ebda; --surface3:#ece2cd; --field:#f3ebda;
    --outline:#e7ddc8; --outline-strong:#d4c7ac;
    --txt:#3a3225; --dim:#8b7f6c; --dim2:#b2a68e; --icon:#d8ccb0;
    --primary:#b0662a; --on-primary:#ffffff; --primary-soft:rgba(176,102,42,.12);
    --grad:linear-gradient(135deg,#c07a3a,#d99a5b);
    --on-accent:#ffffff; --check:#cdbfa4;
    --shadow-1:0 1px 2px rgba(0,0,0,.05),0 1px 3px rgba(0,0,0,.07);
    --shadow-2:0 2px 6px rgba(0,0,0,.07),0 6px 18px rgba(0,0,0,.06);
    --shadow-3:0 8px 20px rgba(0,0,0,.12),0 16px 40px rgba(0,0,0,.10);
    --header-bg:rgba(248,242,231,.90);
    --toast-bg:#3a3225; --toast-txt:#fffdf7;
    --ok:#00b96a; --ok-soft:rgba(0,185,106,.12);
    --warn:#d9a406; --bad:#dc4a4f; --info:#2b84b8;
  }

  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;padding:0;background:var(--bg);color:var(--txt);
    font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    overscroll-behavior-y:none;transition:background .3s,color .3s}
  body{padding-bottom:calc(env(safe-area-inset-bottom) + 96px)}

  /* ===== 顶栏 ===== */
  header{position:sticky;top:0;z-index:20;background:var(--header-bg);
    backdrop-filter:blur(24px) saturate(1.8);-webkit-backdrop-filter:blur(24px) saturate(1.8);
    border-bottom:1px solid var(--outline);padding:calc(env(safe-area-inset-top) + 12px) 16px 12px}
  .top{display:flex;align-items:center;justify-content:space-between;gap:10px}
  .brand{display:flex;align-items:center;gap:10px;min-width:0}
  .logo{width:36px;height:36px;border-radius:11px;background:var(--grad);
    display:flex;align-items:center;justify-content:center;font-weight:800;font-size:17px;color:var(--on-accent);
    box-shadow:var(--shadow-2)}
  h1{margin:0;font-size:18px;font-weight:800;letter-spacing:.3px;white-space:nowrap}
  h1 em{font-style:normal;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
  .right{display:flex;align-items:center;gap:11px;flex:0 0 auto}
  .themeBtn{width:38px;height:38px;border-radius:12px;border:1px solid var(--outline);
    background:var(--surface);font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;
    box-shadow:var(--shadow-1);transition:transform .16s cubic-bezier(.2,0,0,1);position:relative;overflow:hidden;
    backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
  .themeBtn::after{content:"";position:absolute;inset:0;border-radius:12px;
    background:linear-gradient(180deg,rgba(255,255,255,.28),transparent 55%);pointer-events:none;opacity:.6}
  .themeBtn:active{transform:scale(.88)}
  .num{font-variant-numeric:tabular-nums;font-size:13px;color:var(--dim);white-space:nowrap}
  .num b{color:var(--txt);font-size:16px;font-weight:800}
  .bar{height:6px;border-radius:4px;background:var(--surface3);margin:12px 0 13px;overflow:hidden}
  .bar i{display:block;height:100%;width:0;background:var(--grad);border-radius:4px;
    transition:width .45s cubic-bezier(.22,1,.36,1)}

  /* ===== 搜索 ===== */
  .search{position:relative}
  .search input{width:100%;padding:12px 40px 12px 15px;border-radius:14px;border:1px solid var(--outline);
    background:var(--surface);color:var(--txt);font-size:15px;outline:none;
    box-shadow:var(--shadow-1);transition:border-color .18s,box-shadow .18s}
  .search input::placeholder{color:var(--dim2)}
  .search input:focus{border-color:var(--primary);box-shadow:0 0 0 3px var(--primary-soft)}
  .search .x{position:absolute;right:8px;top:50%;transform:translateY(-50%);
    width:30px;height:30px;border:0;background:none;color:var(--dim);font-size:20px;line-height:1;display:none;cursor:pointer}
  .search.has .x{display:block}

  /* ===== 分类 chips ===== */
  .chips{display:flex;gap:8px;margin-top:11px;overflow-x:auto;scrollbar-width:none;padding-bottom:3px}
  .chips::-webkit-scrollbar{display:none}
  .chip{flex:0 0 auto;display:flex;align-items:center;gap:5px;padding:7px 13px;border-radius:999px;
    border:1px solid var(--outline);background:var(--surface);color:var(--dim);font-size:13px;cursor:pointer;
    white-space:nowrap;user-select:none;transition:all .18s cubic-bezier(.2,0,0,1);box-shadow:var(--shadow-1)}
  .chip:active{transform:scale(.94)}
  .chip.on{background:var(--primary-soft);border-color:var(--primary);color:var(--primary);font-weight:700}
  .chip .ic{font-size:14px}
  .chip .c{opacity:.6;font-size:11px;margin-left:1px;font-variant-numeric:tabular-nums}

  /* ===== 状态分段 ===== */
  .status{display:flex;gap:6px;margin-top:11px;padding:4px;border-radius:13px;background:var(--surface3)}
  .seg{flex:1;text-align:center;padding:8px 0;border-radius:10px;color:var(--dim);font-size:13px;
    font-weight:600;cursor:pointer;user-select:none;transition:all .2s cubic-bezier(.2,0,0,1);border:0;background:transparent}
  .seg.on{background:var(--surface);color:var(--txt);box-shadow:var(--shadow-1);font-weight:700}

  /* ===== 列表卡片 ===== */
  main{padding:10px 14px 0}
  .grp{margin:18px 4px 10px;font-size:12px;color:var(--dim);letter-spacing:1.6px;font-weight:800;
    display:flex;align-items:center;gap:9px}
  .grp::after{content:"";flex:1;height:1px;background:var(--outline)}
  .row{display:flex;align-items:center;gap:12px;padding:12px;margin-bottom:11px;
    background:var(--surface);border:1px solid var(--outline);border-radius:18px;cursor:pointer;
    box-shadow:var(--shadow-1);position:relative;overflow:hidden;
    transition:transform .18s cubic-bezier(.2,0,0,1),box-shadow .22s,border-color .18s}
  .row::before{content:"";position:absolute;inset:0;border-radius:18px;padding:1px;
    background:linear-gradient(135deg,rgba(255,255,255,.6),rgba(255,255,255,.06) 40%,rgba(255,255,255,.32));
    -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;opacity:.75}
  .row::after{content:"";position:absolute;left:-30%;top:-60%;width:60%;height:220%;
    background:linear-gradient(100deg,transparent,rgba(255,255,255,.22),transparent);
    transform:rotate(18deg);pointer-events:none;opacity:0;transition:left .6s cubic-bezier(.2,0,0,1),opacity .3s}
  .row:hover::after{left:130%;opacity:1}
  .row:hover{box-shadow:var(--shadow-2);transform:translateY(-1px)}
  .row:active{transform:scale(.98);box-shadow:var(--shadow-2)}
  .row.own{border-color:var(--ok);box-shadow:0 0 0 1px var(--ok) inset,0 0 18px var(--ok-soft),var(--shadow-1)}
  .thumb{flex:0 0 auto;width:68px;height:48px;border-radius:12px;overflow:hidden;background:var(--field);
    border:1px solid var(--outline);position:relative;box-shadow:var(--shadow-1)}
  .thumb::after{content:"";position:absolute;inset:0;border-radius:12px;
    background:linear-gradient(180deg,rgba(255,255,255,.18),transparent 45%);pointer-events:none}
  .thumb img{width:100%;height:100%;object-fit:cover;display:block}
  .thumb .ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
    font-size:21px;color:var(--icon)}
  .box{flex:0 0 auto;width:23px;height:23px;border-radius:8px;border:2px solid var(--check);
    display:flex;align-items:center;justify-content:center;transition:all .18s cubic-bezier(.2,0,0,1);background:transparent}
  .row.own .box{background:var(--ok);border-color:var(--ok);box-shadow:0 0 10px var(--ok-soft)}
  .box svg{width:13px;height:13px;opacity:0;stroke:var(--on-accent);stroke-width:3.4;fill:none;
    stroke-linecap:round;stroke-linejoin:round;transition:opacity .15s}
  .row.own .box svg{opacity:1}
  .nm{flex:1;min-width:0;display:block}
  .cn{display:block;font-size:15px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .en{display:block;font-size:11.5px;color:var(--dim);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-top:2px}
  .mini{display:flex;gap:5px;margin-top:6px;flex-wrap:wrap}
  .mb{font-size:10px;padding:2px 7px;border-radius:6px;background:var(--surface2);border:1px solid var(--outline);color:var(--dim);
    font-variant-numeric:tabular-nums;font-weight:600}
  .mb.rm{color:var(--bad);border-color:rgba(229,72,77,.35);background:rgba(229,72,77,.07)}
  .arw{flex:0 0 auto;color:var(--dim2);font-size:19px;padding:0 2px}
  .tag-cus{flex:0 0 auto;font-size:10px;color:var(--info);border:1px solid rgba(47,127,208,.4);
    padding:2px 7px;border-radius:6px;background:rgba(47,127,208,.07)}
  .empty{text-align:center;color:var(--dim);padding:56px 20px;font-size:14px;line-height:1.9}

  /* ===== FAB ===== */
  .fab{position:fixed;right:18px;bottom:calc(env(safe-area-inset-bottom) + 20px);z-index:30;
    width:58px;height:58px;border-radius:19px;border:1px solid rgba(255,255,255,.25);background:var(--grad);
    color:var(--on-accent);font-size:30px;font-weight:600;line-height:1;box-shadow:var(--shadow-3),
    inset 0 1px 0 rgba(255,255,255,.4),inset 0 -2px 4px rgba(0,0,0,.12);
    backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);cursor:pointer;
    transition:transform .18s cubic-bezier(.2,0,0,1);position:fixed;overflow:hidden}
  .fab::after{content:"";position:absolute;inset:0;border-radius:19px;
    background:linear-gradient(135deg,rgba(255,255,255,.45),transparent 42%);pointer-events:none}
  .fab:active{transform:scale(.9)}

  /* ===== 弹层 ===== */
  .sheet{position:fixed;inset:0;z-index:50;display:none;align-items:flex-end;background:rgba(20,18,28,.42);
    backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
  .sheet.on{display:flex}
  .panel{width:100%;max-height:92vh;overflow:auto;background:var(--surface);
    backdrop-filter:blur(30px) saturate(1.6);-webkit-backdrop-filter:blur(30px) saturate(1.6);
    border-radius:24px 24px 0 0;padding:0 0 calc(env(safe-area-inset-bottom) + 18px);
    border-top:1px solid var(--outline);box-shadow:0 -12px 40px rgba(0,0,0,.16);position:relative}
  .panel::before{content:"";position:absolute;inset:0;border-radius:24px 24px 0 0;padding:1px;
    background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(255,255,255,.08) 30%,transparent);
    -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
    -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none}
  .panel .pad{padding:18px 20px}

  .hero{position:relative;height:190px;background:var(--field);overflow:hidden;border-radius:24px 24px 0 0}
  .hero img{width:100%;height:100%;object-fit:cover;display:block}
  .hero .ov{position:absolute;inset:0;background:linear-gradient(180deg,transparent 32%,rgba(16,14,24,.94) 100%)}
  .hero .ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:54px;color:var(--icon)}
  .hero .ttl{position:absolute;left:20px;right:20px;bottom:14px}
  .hero .ttl h2{margin:0;font-size:22px;font-weight:800;color:#fff;text-shadow:0 1px 10px rgba(0,0,0,.65)}
  .hero .ttl .sub{font-size:12px;color:#e2e0ea;text-shadow:0 1px 5px rgba(0,0,0,.6)}

  .kv{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 4px}
  .pill{font-size:12px;padding:5px 12px;border-radius:999px;background:var(--surface2);
    border:1px solid var(--outline);color:var(--dim);font-weight:600}
  .pill b{color:var(--txt);font-weight:800}
  .pill.g{color:var(--ok);border-color:rgba(0,185,106,.4);background:var(--ok-soft)}
  .pill.r{color:var(--bad);border-color:rgba(229,72,77,.4);background:rgba(229,72,77,.08)}

  .stats{margin:18px 0 6px}
  .stat{display:flex;align-items:center;gap:11px;margin-bottom:12px}
  .stat .k{width:40px;font-size:12.5px;color:var(--dim);flex:0 0 auto;font-weight:700}
  .stat .track{flex:1;height:10px;background:var(--surface3);border-radius:6px;overflow:hidden}
  .stat .fill{height:100%;border-radius:6px;transition:width .55s cubic-bezier(.22,1,.36,1)}
  .stat .v{width:46px;text-align:right;font-size:12.5px;font-variant-numeric:tabular-nums;flex:0 0 auto;font-weight:800}
  .f-green{background:linear-gradient(90deg,#00b96a,#2ee6a8)}
  .f-yellow{background:linear-gradient(90deg,#f5b301,#ffd23f)}
  .f-orange{background:linear-gradient(90deg,#ff8c42,#ffb86b)}
  .f-red{background:linear-gradient(90deg,#e5484d,#ff7a7f)}

  .sec{margin-top:22px}
  .sec h3{margin:0 0 9px;font-size:12px;color:var(--dim);letter-spacing:1.6px;font-weight:800;
    display:flex;align-items:center;gap:8px}
  .sec h3::before{content:"";width:3px;height:14px;border-radius:2px;background:var(--grad)}
  .desc{font-size:14px;line-height:1.8;color:var(--txt);white-space:pre-wrap}

  .fld{margin-bottom:14px}
  .fld label{display:block;font-size:12px;color:var(--dim);margin-bottom:6px;font-weight:700}
  .fld input,.fld select{width:100%;padding:13px 15px;border-radius:13px;border:1px solid var(--outline);
    background:var(--surface2);color:var(--txt);font-size:15px;outline:none;transition:border-color .18s,box-shadow .18s}
  .fld input:focus,.fld select:focus{border-color:var(--primary);box-shadow:0 0 0 3px var(--primary-soft)}
  .btns{display:flex;gap:10px;margin-top:8px}
  .btn{flex:1;padding:14px;border-radius:13px;border:1px solid var(--outline);background:var(--surface2);
    color:var(--txt);font-size:15px;font-weight:700;cursor:pointer;text-align:center;transition:all .16s cubic-bezier(.2,0,0,1)}
  .btn:active{transform:scale(.96)}
  .btn.primary{background:var(--grad);border:none;color:var(--on-accent);font-weight:800;box-shadow:var(--shadow-2)}
  .btn.danger{color:var(--bad);border-color:rgba(229,72,77,.45);background:rgba(229,72,77,.07)}
  .hint{font-size:12px;color:var(--dim);line-height:1.75;margin-top:15px}

  .toast{position:fixed;left:50%;bottom:calc(env(safe-area-inset-bottom) + 94px);transform:translate(-50%,14px);
    background:var(--toast-bg);color:var(--toast-txt);padding:11px 20px;border-radius:999px;font-size:13px;font-weight:700;
    opacity:0;pointer-events:none;transition:all .28s cubic-bezier(.2,0,0,1);z-index:60;white-space:nowrap;max-width:88vw;
    overflow:hidden;text-overflow:ellipsis;box-shadow:var(--shadow-3)}
  .toast.on{opacity:1;transform:translate(-50%,0)}
</style>
</head>
<body data-theme="material">

<header>
  <div class="top">
    <div class="brand">
      <div class="logo">G</div>
      <h1>GTA<em>OL</em> 载具收藏</h1>
    </div>
    <div class="right">
      <button class="themeBtn" id="webdavBtn" aria-label="云备份">☁️</button>
      <button class="themeBtn" id="themeBtn" aria-label="切换主题">🎨</button>
      <div class="num"><b id="ownN">0</b> / <span id="allN">0</span> · <span id="pct">0%</span></div>
    </div>
  </div>
  <div class="bar"><i id="barFill"></i></div>

  <div class="search" id="searchWrap">
    <input id="q" type="search" placeholder="搜索载具 · 中文 / 英文 / 厂商" autocomplete="off" autocorrect="off" spellcheck="false">
    <button class="x" id="qx" aria-label="清空">×</button>
  </div>

  <div class="chips" id="cats"></div>

  <div class="status">
    <div class="seg on" data-st="all">全部</div>
    <div class="seg" data-st="no">未购买</div>
    <div class="seg" data-st="yes">已购买</div>
  </div>
</header>

<main id="list"></main>

<button class="fab" id="fab" aria-label="添加载具">+</button>

<div class="sheet" id="detail"><div class="panel" id="detailBody"></div></div>

<div class="sheet" id="sheet">
  <div class="panel"><div class="pad">
    <h2 style="margin:0 0 18px;font-size:18px;font-weight:800">添加载具</h2>
    <div class="fld"><label>中文名（可留空）</label><input id="fCn" placeholder="例：暴君 Mk 2" autocomplete="off"></div>
    <div class="fld"><label>英文名（必填）</label><input id="fEn" placeholder="例：Oppressor Mk II" autocomplete="off"></div>
    <div class="fld"><label>分类</label><select id="fCat"></select></div>
    <div class="btns">
      <button class="btn" id="cancel">取消</button>
      <button class="btn primary" id="save">添加</button>
    </div>
    <div class="hint">数据只存在本机，不上传、不联网。换手机或清缓存前先导出备份。</div>
    <div class="btns" style="margin-top:16px">
      <button class="btn" id="export">导出备份</button>
      <button class="btn" id="importBtn">导入备份</button>
    </div>
    <div class="btns" style="margin-top:10px">
      <button class="btn danger" id="reset">清空全部记录</button>
    </div>
    <input type="file" id="file" accept=".json,application/json" hidden>
  </div></div>
</div>

<!-- WebDAV 面板 -->
<div class="sheet" id="webdav">
  <div class="panel"><div class="pad">
    <h2 style="margin:0 0 6px;font-size:18px;font-weight:800">WebDAV 云备份</h2>
    <div class="hint" style="margin:0 0 16px">支持坚果云、Nextcloud 等 WebDAV 网盘。文件会以 JSON 形式存到你的网盘。</div>
    <div class="fld"><label>服务器地址（完整文件 URL）</label>
      <input id="wUrl" placeholder="https://dav.jianguoyun.com/dav/gtaol/backup.json" autocomplete="off"></div>
    <div class="fld"><label>用户名</label>
      <input id="wUser" placeholder="你的网盘账号 / 邮箱" autocomplete="off"></div>
    <div class="fld"><label>密码 / 应用密码</label>
      <input id="wPass" type="password" placeholder="网盘密码或独立应用密码" autocomplete="off"></div>
    <div class="btns">
      <button class="btn" id="wBackup">↑ 备份到云端</button>
      <button class="btn" id="wRestore">↓ 从云端恢复</button>
    </div>
    <div class="btns" style="margin-top:10px">
      <button class="btn" id="wClose">关闭</button>
    </div>
    <div class="hint">
      提示：坚果云请在「账户信息 → 安全选项」里生成「应用密码」，用那个密码填在这里。
      密码只存在本机，不会上传给除你网盘以外的任何地方。
    </div>
  </div></div>
</div>

<div class="toast" id="toast"></div>

<script>
var VEHICLES = __DATA__;

(function(){
  "use strict";

  /* ===== 主题 ===== */
  var THEMES = [
    {id:"material", icon:"🎨"},
    {id:"light",    icon:"☀️"},
    {id:"dark",     icon:"🌙"},
    {id:"warm",     icon:"🌅"}
  ];
  var themeIdx = 0;
  function applyTheme(id, save){
    document.body.setAttribute("data-theme", id);
    var meta = document.querySelector('meta[name="theme-color"]');
    var c = getComputedStyle(document.body).getPropertyValue("--bg").trim();
    if (meta && c) meta.setAttribute("content", c);
    if (save){ try{ localStorage.setItem("gtaol-theme", id); }catch(e){} }
  }
  function syncThemeBtn(){ document.getElementById("themeBtn").textContent = THEMES[themeIdx].icon; }
  function cycleTheme(){
    themeIdx = (themeIdx + 1) % THEMES.length;
    applyTheme(THEMES[themeIdx].id, true);
    syncThemeBtn();
  }
  (function initTheme(){
    var saved = null; try{ saved = localStorage.getItem("gtaol-theme"); }catch(e){}
    if (saved){ var i = THEMES.findIndex(function(t){ return t.id === saved; }); if (i >= 0) themeIdx = i; }
    applyTheme(THEMES[themeIdx].id, false);
    syncThemeBtn();
    document.getElementById("themeBtn").addEventListener("click", cycleTheme);
  })();

  var CATS = [
    ["super","超级跑车","🏎"],["sports","跑车","🚗"],["coupe","轿跑车","🏎"],
    ["muscle","肌肉车","💪"],["classic","经典跑车","🚙"],["suv","SUV","🚐"],
    ["offroad","越野车","🏔"],["sedan","轿车","🚘"],["compact","小型汽车","🚗"],
    ["van","厢型车 / 商用车","🚚"],["service","服务用车","🛠"],["moto","摩托车","🏍"],
    ["bike","自行车","🚲"],["plane","飞机","✈"],["heli","直升机","🚁"],
    ["boat","船","⛵"],["military","军用车","🪖"],["special","其他","📦"]
  ];
  var CATNAME = {}, CATICON = {}, CATORDER = {};
  CATS.forEach(function(c,i){ CATNAME[c[0]]=c[1]; CATICON[c[0]]=c[2]; CATORDER[c[0]]=i; });

  var KEY = "gtaol-vehicles-v2";
  var state = { owned:{}, custom:[] };
  var ALL = [], byKey = {};

  function buildIndex(){
    ALL = VEHICLES.slice();
    state.custom.forEach(function(c){
      ALL.push({ m:"custom-"+c.en.toLowerCase().replace(/[^a-z0-9]+/g,"-"),
        n:c.cn||c.en, e:c.en, b:"", c:c.cat, custom:true });
    });
    byKey = {};
    ALL.forEach(function(v){ byKey[v.m]=v; });
    ALL.sort(function(a,b){
      var ai=CATORDER[a.c]===undefined?99:CATORDER[a.c];
      var bi=CATORDER[b.c]===undefined?99:CATORDER[b.c];
      if(ai!==bi) return ai-bi;
      return (a.n||"").localeCompare(b.n||"","zh-Hans-CN");
    });
  }

  // 是否在原生 App 环境（有 NativeBridge）
  function native(){
    return typeof window.NativeBridge !== "undefined" && window.NativeBridge !== null;
  }

  function load(){
    var raw = null;
    // 优先原生持久化（升级不丢）
    if (native() && typeof NativeBridge.loadState === "function"){
      try{ raw = NativeBridge.loadState(); }catch(e){}
    }
    // 兜底 localStorage
    if (!raw){
      try{ raw = localStorage.getItem(KEY); }catch(e){}
    }
    if (raw){
      try{
        var d = JSON.parse(raw);
        if (d && typeof d === "object"){
          state.owned = (d.owned && typeof d.owned === "object") ? d.owned : {};
          state.custom = Array.isArray(d.custom) ? d.custom : [];
        }
      }catch(e){}
    }
  }
  function save(){
    var json = JSON.stringify(state);
    var savedNative = false;
    if (native() && typeof NativeBridge.saveState === "function"){
      try{ NativeBridge.saveState(json); savedNative = true; }catch(e){}
    }
    // 始终也写 localStorage（网页版 + 兜底）
    try{ localStorage.setItem(KEY, json); }
    catch(e){ if(!savedNative) toast("保存失败：存储空间不足"); }
  }

  var view={q:"",cat:"all",st:"all"};
  var elList=document.getElementById("list");
  var elCats=document.getElementById("cats");
  var elQ=document.getElementById("q");
  var elQx=document.getElementById("qx");
  var elOw=document.getElementById("ownN");
  var elAl=document.getElementById("allN");
  var elPct=document.getElementById("pct");
  var elBar=document.getElementById("barFill");
  var toastEl=document.getElementById("toast");
  var toastT=null;

  function toast(msg){ toastEl.textContent=msg; toastEl.classList.add("on");
    clearTimeout(toastT); toastT=setTimeout(function(){toastEl.classList.remove("on");},1500); }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g,function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }

  function matches(v){
    if(view.cat!=="all"&&v.c!==view.cat) return false;
    var own=!!state.owned[v.m];
    if(view.st==="yes"&&!own) return false;
    if(view.st==="no"&&own) return false;
    if(view.q){ var q=view.q.toLowerCase();
      var hay=((v.n||"")+" "+(v.e||"")+" "+(v.b||"")+" "+(v.t||"")).toLowerCase();
      if(hay.indexOf(q)<0) return false; }
    return true;
  }

  function imgOf(v){ return v._img || null; }

  function renderCats(){
    var counts={};
    ALL.forEach(function(v){ counts[v.c]=counts[v.c]||{t:0,o:0};
      counts[v.c].t++; if(state.owned[v.m]) counts[v.c].o++; });
    var html='<div class="chip'+(view.cat==="all"?" on":"")+'" data-cat="all"><span class="ic">🗂</span>全部<span class="c">'+ALL.length+'</span></div>';
    CATS.forEach(function(c){ var n=counts[c[0]]; if(!n) return;
      html+='<div class="chip'+(view.cat===c[0]?" on":"")+'" data-cat="'+c[0]+'"><span class="ic">'+c[2]+'</span>'+c[1]+'<span class="c">'+n.o+'/'+n.t+'</span></div>'; });
    elCats.innerHTML=html;
  }

  function renderList(){
    var frag=document.createDocumentFragment();
    var lastCat=null, shown=0;
    ALL.forEach(function(v){
      if(!matches(v)) return;
      if(view.cat==="all"&&v.c!==lastCat){ lastCat=v.c;
        var h=document.createElement("div"); h.className="grp";
        h.textContent=(CATICON[v.c]||"·")+" "+(CATNAME[v.c]||v.c).toUpperCase();
        frag.appendChild(h); }
      shown++;
      var own=!!state.owned[v.m];
      var row=document.createElement("div");
      row.className="row"+(own?" own":"");
      row.dataset.k=v.m;
      var img=imgOf(v);
      var thumb = img
        ? '<div class="thumb"><img loading="lazy" src="'+esc(img)+'" onerror="this.parentNode.innerHTML=\'<span class=ph>🚗</span>\'"></div>'
        : '<div class="thumb"><span class="ph">'+(CATICON[v.c]||"🚗")+'</span></div>';
      var minis='<div class="mini">';
      if(v.p) minis+='<span class="mb">$'+Number(v.p).toLocaleString("en-US")+'</span>';
      if(v.sp!=null) minis+='<span class="mb">极速 '+v.sp+'</span>';
      if(v.rm) minis+='<span class="mb rm">已下架</span>';
      minis+='</div>';
      row.innerHTML = thumb +
        '<span class="nm"><span class="cn"></span><span class="en"></span>'+minis+'</span>' +
        (v.custom?'<span class="tag-cus">自建</span>':'<span class="arw">›</span>');
      row.querySelector(".cn").textContent=v.n;
      var sub=v.e; if(v.b) sub=v.b+" · "+v.e;
      row.querySelector(".en").textContent=sub;
      frag.appendChild(row);
    });
    elList.innerHTML="";
    if(!shown){ var e=document.createElement("div"); e.className="empty";
      e.innerHTML=view.q?"没找到「"+esc(view.q)+"」<br><span style='font-size:12px'>点右下角 + 自己添加一个</span>":"这里还没有载具";
      elList.appendChild(e); }
    else elList.appendChild(frag);
  }

  function renderStats(){
    var total=ALL.length, own=0;
    ALL.forEach(function(v){ if(state.owned[v.m]) own++; });
    elOw.textContent=own; elAl.textContent=total;
    var p=total?Math.round(own*100/total):0;
    elPct.textContent=p+"%"; elBar.style.width=p+"%";
  }

  function render(){ renderStats(); renderCats(); renderList(); }

  var detailEl=document.getElementById("detail");
  var detailBody=document.getElementById("detailBody");

  function money(n){ if(!n&&n!==0) return ""; return "$"+Number(n).toLocaleString("en-US"); }

  function gradeColor(val){
    var v=Number(val);
    if(v>=80) return "f-green";
    if(v>=65) return "f-yellow";
    if(v>=50) return "f-orange";
    return "f-red";
  }
  function statRow(label,val){
    if(val===undefined||val===null) return "";
    var v=Math.max(0,Math.min(100,Number(val)));
    return '<div class="stat"><span class="k">'+label+'</span>'+
      '<span class="track"><span class="fill '+gradeColor(v)+'" style="width:'+v+'%"></span></span>'+
      '<span class="v">'+(Math.round(v*10)/10)+'</span></div>';
  }

  function openDetail(v){
    var own=!!state.owned[v.m];
    var img=imgOf(v);
    var h=[];
    h.push('<div class="hero">');
    if(img) h.push('<img src="'+esc(img)+'" onerror="this.style.display=\'none\'">');
    h.push('<div class="ph">'+(CATICON[v.c]||"🚗")+'</div>');
    h.push('<div class="ov"></div><div class="ttl"><h2>'+esc(v.n)+'</h2>');
    var sub=esc(v.e||""); if(v.t&&v.t!==v.n) sub+=" · "+esc(v.t);
    h.push('<div class="sub">'+sub+'</div></div></div>');
    h.push('<div class="pad">');

    var pills=[];
    if(v.b) pills.push('<span class="pill">厂商 <b>'+esc(v.b)+'</b></span>');
    if(v.k) pills.push('<span class="pill">'+esc(v.k)+'</span>');
    if(v.s) pills.push('<span class="pill">'+v.s+' 座</span>');
    if(v.d) pills.push('<span class="pill">'+esc(v.d)+'</span>');
    if(v.dl) pills.push('<span class="pill">'+esc(v.dl)+'</span>');
    if(v.rm) pills.push('<span class="pill r">已下架</span>');
    if(pills.length) h.push('<div class="kv">'+pills.join("")+'</div>');

    var prices=[];
    if(v.p) prices.push('<span class="pill g">价格 <b>'+money(v.p)+'</b></span>');
    if(v.tp) prices.push('<span class="pill">批发价 <b>'+money(v.tp)+'</b></span>');
    if(v.wb) prices.push('<span class="pill">购买 <b>'+esc(v.wb)+'</b></span>');
    if(prices.length) h.push('<div class="kv">'+prices.join("")+'</div>');

    var stats=statRow("极速",v.sp)+statRow("加速",v.ac)+statRow("刹车",v.br)+statRow("操控",v.ha);
    if(stats){
      var extra=[];
      if(v.tst) extra.push("实测极速 "+v.tst+" km/h");
      if(v.tsg) extra.push("面板极速 "+v.tsg+" km/h");
      h.push('<div class="sec"><h3>性能</h3><div class="stats">'+stats+'</div>'+
        (extra.length?'<div style="margin:4px 0 0;font-size:12px;color:var(--dim)">'+extra.join(" · ")+'</div>':'')+'</div>');
    }

    if(v.x) h.push('<div class="sec"><h3>车辆介绍</h3><div class="desc">'+esc(v.x)+'</div></div>');
    if(v.o) h.push('<div class="sec"><h3>现实原型</h3><div class="desc">'+esc(v.o)+'</div></div>');

    h.push('<div class="btns" style="margin-top:22px">'+
      '<button class="btn" id="dClose">关闭</button>'+
      '<button class="btn '+(own?'danger':'primary')+'" id="dToggle">'+(own?'取消已购买':'标记为已购买')+'</button></div>');
    h.push('</div>');

    detailBody.innerHTML=h.join("");
    detailEl.classList.add("on");
    document.getElementById("dClose").onclick=function(){ detailEl.classList.remove("on"); };
    document.getElementById("dToggle").onclick=function(){
      if(state.owned[v.m]) delete state.owned[v.m]; else state.owned[v.m]=1;
      save(); render(); detailEl.classList.remove("on");
      toast(state.owned[v.m]?"已标记购买":"已取消标记");
    };
  }
  detailEl.addEventListener("click",function(e){ if(e.target===detailEl) detailEl.classList.remove("on"); });

  var pressTimer=null, longPressed=false;
  elList.addEventListener("click",function(e){
    var row=e.target.closest(".row"); if(!row) return;
    var k=row.dataset.k, v=byKey[k]; if(!v) return;
    if(longPressed){ longPressed=false; return; }
    if(state.owned[k]) delete state.owned[k]; else state.owned[k]=1;
    save(); row.classList.toggle("own",!!state.owned[k]); renderStats(); renderCats();
    if(navigator.vibrate){ try{ navigator.vibrate(8); }catch(_){} }
  });
  elList.addEventListener("touchstart",function(e){
    var row=e.target.closest(".row"); if(!row) return;
    longPressed=false;
    pressTimer=setTimeout(function(){ longPressed=true;
      var v=byKey[row.dataset.k]; if(v) openDetail(v);
      if(navigator.vibrate){ try{ navigator.vibrate(20); }catch(_){} } },480);
  },{passive:true});
  ["touchend","touchmove","touchcancel"].forEach(function(ev){
    elList.addEventListener(ev,function(){ clearTimeout(pressTimer); },{passive:true}); });
  elList.addEventListener("contextmenu",function(e){
    var row=e.target.closest(".row"); if(!row) return;
    e.preventDefault(); var v=byKey[row.dataset.k]; if(v) openDetail(v);
  });

  elCats.addEventListener("click",function(e){
    var chip=e.target.closest(".chip"); if(!chip) return;
    view.cat=chip.dataset.cat; render(); window.scrollTo({top:0,behavior:"smooth"});
  });
  document.querySelectorAll(".seg").forEach(function(s){
    s.addEventListener("click",function(){
      document.querySelectorAll(".seg").forEach(function(x){x.classList.remove("on");});
      s.classList.add("on"); view.st=s.dataset.st; renderList();
    });
  });
  var qT=null;
  elQ.addEventListener("input",function(){
    document.getElementById("searchWrap").classList.toggle("has",elQ.value.length>0);
    clearTimeout(qT); qT=setTimeout(function(){view.q=elQ.value.trim();renderList();},90);
  });
  elQx.addEventListener("click",function(){ elQ.value="";view.q="";
    document.getElementById("searchWrap").classList.remove("has"); renderList(); elQ.focus(); });

  var sheet=document.getElementById("sheet");
  var fCat=document.getElementById("fCat");
  CATS.forEach(function(c){ var o=document.createElement("option"); o.value=c[0]; o.textContent=c[1]; fCat.appendChild(o); });

  document.getElementById("fab").addEventListener("click",function(){
    sheet.classList.add("on"); document.getElementById("fCn").value=""; document.getElementById("fEn").value="";
    setTimeout(function(){document.getElementById("fEn").focus();},120);
  });
  document.getElementById("cancel").addEventListener("click",function(){ sheet.classList.remove("on"); });
  sheet.addEventListener("click",function(e){ if(e.target===sheet) sheet.classList.remove("on"); });

  document.getElementById("save").addEventListener("click",function(){
    var cn=document.getElementById("fCn").value.trim();
    var en=document.getElementById("fEn").value.trim();
    if(!en&&!cn){ toast("名称不能为空"); return; }
    if(!en) en=cn;
    var exists=ALL.some(function(v){ return (v.e&&v.e.toLowerCase()===en.toLowerCase())||(cn&&v.n===cn); });
    if(exists){ toast("已经有这个载具了"); return; }
    state.custom.push({en:en,cn:cn||en,cat:fCat.value});
    var key="custom-"+en.toLowerCase().replace(/[^a-z0-9]+/g,"-");
    state.owned[key]=1;
    save(); buildIndex(); sheet.classList.remove("on");
    view.cat="all";view.q="";view.st="all"; elQ.value="";
    document.querySelectorAll(".seg").forEach(function(x){x.classList.toggle("on",x.dataset.st==="all");});
    render(); toast("已添加："+(cn||en));
  });

  document.getElementById("export").addEventListener("click",function(){
    var data={app:"gtaol-vehicles",version:2,exportedAt:new Date().toISOString(),owned:state.owned,custom:state.custom};
    var d=new Date(); var stamp=d.getFullYear()+String(d.getMonth()+1).padStart(2,"0")+String(d.getDate()).padStart(2,"0");
    var filename="gtaol-vehicles-"+stamp+".json"; var jsonText=JSON.stringify(data,null,2);
    if(window.NativeBridge&&typeof window.NativeBridge.saveBackup==="function"){
      var ok=window.NativeBridge.saveBackup(jsonText,filename);
      toast(ok?"备份已保存到 下载 文件夹":"导出失败"); return;
    }
    var blob=new Blob([jsonText],{type:"application/json"}); var url=URL.createObjectURL(blob);
    var a=document.createElement("a"); a.href=url; a.download=filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){URL.revokeObjectURL(url);},1000); toast("备份已导出");
  });

  var fileEl=document.getElementById("file");
  document.getElementById("importBtn").addEventListener("click",function(){ fileEl.click(); });
  fileEl.addEventListener("change",function(){
    var f=fileEl.files&&fileEl.files[0]; if(!f) return;
    var r=new FileReader();
    r.onload=function(){ try{
      var d=JSON.parse(r.result);
      if(!d||typeof d!=="object"||(!d.owned&&!d.custom)) throw new Error("bad");
      var n=0;
      if(d.owned&&typeof d.owned==="object"){ Object.keys(d.owned).forEach(function(k){ if(d.owned[k]){state.owned[k]=1;n++;} }); }
      if(Array.isArray(d.custom)){ d.custom.forEach(function(c){
        if(c&&c.en&&!state.custom.some(function(x){return x.en===c.en;})){ state.custom.push({en:c.en,cn:c.cn||c.en,cat:c.cat||"special"}); } }); }
      save(); buildIndex(); render(); toast("已导入 "+n+" 条记录");
    }catch(err){ toast("导入失败：文件格式不对"); } fileEl.value=""; };
    r.readAsText(f);
  });

  document.getElementById("reset").addEventListener("click",function(){
    if(!confirm("清空全部购买记录？\n（自建载具也会一起删掉，建议先导出备份）")) return;
    state.owned={};state.custom=[]; save(); buildIndex(); sheet.classList.remove("on"); render(); toast("已清空");
  });

  /* ===== WebDAV ===== */
  var webdavEl = document.getElementById("webdav");
  var wUrl = document.getElementById("wUrl");
  var wUser = document.getElementById("wUser");
  var wPass = document.getElementById("wPass");
  var WD_KEY = "gtaol-webdav";

  function wdLoad(){
    try{
      var raw = localStorage.getItem(WD_KEY);
      if (raw){
        var d = JSON.parse(raw);
        wUrl.value = d.url || ""; wUser.value = d.user || ""; wPass.value = d.pass || "";
      }
    }catch(e){}
  }
  function wdSave(){
    try{
      localStorage.setItem(WD_KEY, JSON.stringify({url:wUrl.value, user:wUser.value, pass:wPass.value}));
    }catch(e){}
  }

  document.getElementById("webdavBtn").addEventListener("click", function(){
    wdLoad();
    webdavEl.classList.add("on");
  });
  document.getElementById("wClose").addEventListener("click", function(){ webdavEl.classList.remove("on"); });
  webdavEl.addEventListener("click", function(e){ if(e.target===webdavEl) webdavEl.classList.remove("on"); });

  function currentBackupJson(){
    return JSON.stringify({app:"gtaol-vehicles",version:2,exportedAt:new Date().toISOString(),owned:state.owned,custom:state.custom});
  }

  document.getElementById("wBackup").addEventListener("click", function(){
    var url = wUrl.value.trim();
    if (!url){ toast("请填写服务器地址"); return; }
    wdSave();
    var json = currentBackupJson();
    toast("正在上传…");
    var r;
    if (native() && typeof NativeBridge.webdavPut === "function"){
      r = NativeBridge.webdavPut(url, wUser.value.trim(), wPass.value, json);
    } else {
      // 浏览器兜底：直接 fetch（受 CORS 限制，多数网盘不可用）
      r = "ERR:请使用 App 版本进行 WebDAV 备份";
    }
    if (r && r.indexOf("OK") === 0){ toast("云端备份成功"); }
    else { toast(r || "上传失败"); }
  });

  document.getElementById("wRestore").addEventListener("click", function(){
    var url = wUrl.value.trim();
    if (!url){ toast("请填写服务器地址"); return; }
    wdSave();
    toast("正在下载…");
    var r;
    if (native() && typeof NativeBridge.webdavGet === "function"){
      r = NativeBridge.webdavGet(url, wUser.value.trim(), wPass.value);
    } else {
      r = "ERR:请使用 App 版本进行 WebDAV 恢复";
    }
    if (r && r.indexOf("OK:") === 0){
      try{
        var d = JSON.parse(r.substring(3));
        if (!d || typeof d !== "object" || (!d.owned && !d.custom)) throw new Error("bad");
        var n = 0;
        if (d.owned && typeof d.owned === "object"){
          Object.keys(d.owned).forEach(function(k){ if(d.owned[k]){ state.owned[k]=1; n++; } });
        }
        if (Array.isArray(d.custom)){
          d.custom.forEach(function(c){
            if (c && c.en && !state.custom.some(function(x){ return x.en === c.en; })){
              state.custom.push({en:c.en, cn:c.cn||c.en, cat:c.cat||"special"});
            }
          });
        }
        save(); buildIndex(); render();
        webdavEl.classList.remove("on");
        toast("云端恢复成功，共 " + n + " 条");
      }catch(e){ toast("恢复失败：文件格式不对"); }
    } else {
      toast(r || "下载失败");
    }
  });

  load(); buildIndex(); render();
})();
</script>
</body>
</html>
'''

html = html.replace("__DATA__", data_js)

with open("../app/src/main/assets/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("written", len(html), "bytes, vehicles:", len(data))
