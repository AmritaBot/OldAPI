"""OldAPI 主页模板（内联字符串，兼容 Workers 无文件系统的运行时）。

版式参考 New API 的落地页 / 状态页：顶部导航、Hero、系统状态面板、90 天可用性、
节点延迟、公告与常见问题。主页不再展示任何模型清单。

``__MODELS__`` / ``__QUOTES__`` 两个占位符仍由 src/app.py 替换，这里已不再使用，
保留是为了兼容现有的 render_index()，不引入额外改动。
"""

INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AmritaAI 宇宙级中转站</title>
<meta name="description" content="AmritaAI 宇宙级中转站，包含全球前沿模型，兼容 OpenAI 接口的统一 API 网关。">
<meta name="theme-color" content="#ffffff">
<script>
  ;(function () {
    var t = null;
    try { t = localStorage.getItem('amritaai:theme'); } catch (e) {}
    if (t !== 'dark' && t !== 'light') {
      t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    if (t === 'dark') document.documentElement.classList.add('dark');
  })();
</script>
<style>
  :root{
    --bg:#f6f7f9; --panel:#ffffff; --panel-2:#fbfcfd; --line:#e5e8ee; --line-2:#eef1f6;
    --ink:#0f172a; --ink-2:#334155; --dim:#6b7688; --faint:#98a2b3;
    --accent:#2563eb; --accent-soft:#eff4ff; --accent-ink:#ffffff;
    --ok:#15a05a; --ok-soft:#e8f7ef; --warn:#d68a12; --warn-soft:#fdf4e3;
    --shadow:0 1px 2px rgba(16,24,40,.04), 0 8px 24px -16px rgba(16,24,40,.18);
    --radius:14px;
  }
  html.dark{
    --bg:#0a0e14; --panel:#111721; --panel-2:#0e141d; --line:#1e2733; --line-2:#18202b;
    --ink:#e7edf7; --ink-2:#c3ccdb; --dim:#8a95a8; --faint:#68738a;
    --accent:#5b8def; --accent-soft:#152238; --accent-ink:#08101f;
    --ok:#3fcf8e; --ok-soft:#0f2419; --warn:#e0a952; --warn-soft:#241c0e;
    --shadow:0 1px 2px rgba(0,0,0,.3), 0 12px 30px -18px rgba(0,0,0,.8);
  }
  *{box-sizing:border-box}
  html,body{margin:0}
  body{
    background:var(--bg); color:var(--ink);
    font:14.5px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
    -webkit-font-smoothing:antialiased;
  }
  a{color:inherit;text-decoration:none}
  h1,h2,h3,h4{margin:0;font-weight:650;letter-spacing:-.2px}
  p{margin:0}
  .wrap{width:100%;max-width:1160px;margin:0 auto;padding:0 24px}
  .muted{color:var(--dim)}

  /* ---------- 顶栏 ---------- */
  header.site{position:sticky;top:0;z-index:30;border-bottom:1px solid var(--line);
    background:color-mix(in srgb,var(--panel) 82%,transparent);backdrop-filter:blur(14px) saturate(140%)}
  .head{display:flex;align-items:center;gap:28px;height:62px}
  .brand{display:flex;align-items:center;gap:10px;flex-shrink:0}
  .logo{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:#fff;font-weight:800;font-size:15px;
    background:linear-gradient(135deg,#3b82f6,#7c3aed 70%);box-shadow:0 6px 16px -8px rgba(59,130,246,.9)}
  .brand b{font-size:16px;letter-spacing:.2px}
  .brand .pill{font-size:11px;color:var(--dim);border:1px solid var(--line);background:var(--panel-2);
    padding:1px 7px;border-radius:999px;letter-spacing:.4px}
  nav.main{display:flex;gap:4px;margin-left:6px}
  nav.main a{padding:6px 11px;border-radius:8px;color:var(--dim);font-size:14px;transition:.15s}
  nav.main a:hover{color:var(--ink);background:var(--panel-2)}
  nav.main a.on{color:var(--ink);background:var(--line-2);font-weight:550}
  .head-right{margin-left:auto;display:flex;align-items:center;gap:8px}
  .icon-btn{width:32px;height:32px;border-radius:9px;border:1px solid var(--line);background:var(--panel);
    color:var(--dim);cursor:pointer;font-size:14px;line-height:1}
  .icon-btn:hover{color:var(--ink);border-color:var(--faint)}
  .btn{cursor:pointer;font:inherit;font-size:13.5px;border-radius:9px;padding:7px 14px;border:1px solid var(--line);
    background:var(--panel);color:var(--ink);transition:.15s;white-space:nowrap}
  .btn:hover{border-color:var(--faint)}
  .btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
  .btn.primary:hover{filter:brightness(1.06)}
  html.dark .btn.primary{color:var(--accent-ink)}
  .btn.lg{padding:10px 20px;font-size:14.5px;border-radius:10px}
  .btn.sm{padding:4px 10px;font-size:12.5px;border-radius:8px}

  /* ---------- Hero ---------- */
  .hero{position:relative;overflow:hidden;padding:74px 0 54px;text-align:center;
    background:radial-gradient(900px 380px at 50% -12%,var(--accent-soft) 0%,transparent 68%)}
  .hero:after{content:"";position:absolute;inset:auto 0 0;height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent)}
  .status-pill{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;color:var(--ok);
    border:1px solid color-mix(in srgb,var(--ok) 30%,var(--line));background:var(--ok-soft);
    padding:4px 11px;border-radius:999px;margin-bottom:22px}
  .dot{width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block}
  .dot.live{animation:pulse 2.4s ease-out infinite}
  @keyframes pulse{0%{box-shadow:0 0 0 0 color-mix(in srgb,currentColor 45%,transparent)}
    70%{box-shadow:0 0 0 7px transparent}100%{box-shadow:0 0 0 0 transparent}}
  .hero h1{font-size:clamp(30px,4.4vw,46px);line-height:1.16}
  .hero h1 span{background:linear-gradient(96deg,var(--accent),#7c3aed 55%,#0ea5a4);
    -webkit-background-clip:text;background-clip:text;color:transparent}
  .hero .lead{color:var(--dim);max-width:640px;margin:16px auto 0;font-size:15.5px}
  .cta{display:flex;gap:12px;justify-content:center;margin-top:28px;flex-wrap:wrap}
  .hero-stats{display:flex;justify-content:center;gap:44px;margin-top:40px;flex-wrap:wrap}
  .hero-stats div{display:flex;flex-direction:column;gap:2px}
  .hero-stats b{font-size:20px;font-weight:680;letter-spacing:-.3px}
  .hero-stats span{font-size:12px;color:var(--faint)}

  /* ---------- 区块 ---------- */
  .section{padding:52px 0 0}
  .sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:18px;flex-wrap:wrap}
  .sec-head h2{font-size:20px}
  .sec-head p{color:var(--dim);font-size:13.5px;margin-top:4px}
  .sec-meta{display:flex;align-items:center;gap:10px;color:var(--faint);font-size:12.5px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
  .card-head{display:flex;align-items:center;justify-content:space-between;padding:16px 18px;border-bottom:1px solid var(--line-2)}
  .card-head h3{font-size:14.5px}
  .card-body{padding:18px}

  .banner{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;
    background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--ok);
    border-radius:var(--radius);padding:16px 20px;box-shadow:var(--shadow)}
  .banner-left{display:flex;align-items:center;gap:14px}
  .check{width:32px;height:32px;border-radius:50%;display:grid;place-items:center;flex-shrink:0;
    background:var(--ok-soft);color:var(--ok);font-size:15px;font-weight:700}
  .banner b{font-size:14.5px}
  .banner p{color:var(--dim);font-size:12.8px;margin-top:2px}
  .banner-right{text-align:right;display:flex;flex-direction:column}
  .banner-right span{font-size:12px;color:var(--faint)}
  .banner-right b{font-size:16px}

  .comps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px}
  .comp{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 15px;box-shadow:var(--shadow)}
  .comp-top{display:flex;align-items:center;gap:8px}
  .comp-top b{font-size:13.5px;font-weight:600}
  .comp-top .pct{margin-left:auto;font-size:12.5px;color:var(--dim);font-variant-numeric:tabular-nums}
  .comp .dot{color:var(--ok)}
  .comp .track{height:4px;border-radius:99px;background:var(--line-2);margin:11px 0 9px;overflow:hidden}
  .comp .track i{display:block;height:100%;border-radius:99px;background:var(--ok)}
  .comp-foot{font-size:12px;color:var(--faint);display:flex;justify-content:space-between}

  .split{display:grid;grid-template-columns:1.55fr 1fr;gap:14px;margin-top:14px}
  .bars{display:flex;align-items:flex-end;gap:2px;height:64px;padding:4px 0 0}
  .bars i{flex:1;border-radius:2px;background:var(--ok);opacity:.9;min-height:8px;transition:.2s}
  .bars i:hover{opacity:1;transform:scaleY(1.06)}
  .bars i.warn{background:var(--warn)}
  .bars-axis{display:flex;justify-content:space-between;font-size:11.5px;color:var(--faint);margin-top:8px}
  .bars-foot{display:flex;gap:26px;border-top:1px solid var(--line-2);margin-top:14px;padding-top:12px;font-size:12.5px;color:var(--dim)}
  .bars-foot b{color:var(--ink);font-weight:600}
  .legend{display:flex;align-items:center;gap:12px;font-size:11.5px;color:var(--faint)}
  .legend span{display:inline-flex;align-items:center;gap:5px}
  .legend i{width:8px;height:8px;border-radius:2px;background:var(--ok);display:inline-block}
  .legend i.warn{background:var(--warn)}

  .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
  .stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:15px 16px;box-shadow:var(--shadow)}
  .stat span{font-size:12.5px;color:var(--dim)}
  .stat b{display:block;font-size:22px;font-weight:660;letter-spacing:-.4px;margin-top:5px;font-variant-numeric:tabular-nums}
  .stat em{font-style:normal;font-size:11.5px;color:var(--ok);margin-left:6px}
  .stat em.down{color:var(--faint)}

  table.nodes{width:100%;border-collapse:collapse;font-size:13.2px}
  table.nodes th{text-align:left;font-weight:550;color:var(--faint);font-size:12px;padding:0 0 10px}
  table.nodes td{padding:9px 0;border-top:1px solid var(--line-2);color:var(--ink-2)}
  table.nodes td:last-child,table.nodes th:last-child{text-align:right}
  table.nodes .lat{font-variant-numeric:tabular-nums;color:var(--dim)}
  .tag-ok{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:var(--ok)}
  .tag-ok .dot{width:5px;height:5px}

  ul.notice{list-style:none;margin:0;padding:0}
  ul.notice li{display:flex;gap:14px;padding:12px 0;border-top:1px solid var(--line-2);font-size:13.4px;color:var(--ink-2)}
  ul.notice li:first-child{border-top:none;padding-top:0}
  ul.notice time{flex-shrink:0;color:var(--faint);font-size:12.5px;font-variant-numeric:tabular-nums;padding-top:1px}
  .notice-card{margin-top:14px}

  .faq{margin-top:14px;overflow:hidden}
  details{border-top:1px solid var(--line-2)}
  details:first-of-type{border-top:none}
  summary{cursor:pointer;padding:14px 18px;font-size:13.8px;font-weight:550;list-style:none;display:flex;align-items:center;gap:10px}
  summary::-webkit-details-marker{display:none}
  summary:before{content:"›";color:var(--faint);transition:.2s;display:inline-block}
  details[open] summary:before{transform:rotate(90deg)}
  details p{padding:0 18px 15px 33px;color:var(--dim);font-size:13.2px}

  footer.site{border-top:1px solid var(--line);margin-top:56px;padding:26px 0 34px;background:var(--panel-2)}
  .foot{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;font-size:12.8px;color:var(--dim)}
  .foot-links{display:flex;gap:18px}
  .foot-links a:hover{color:var(--ink)}
  .foot-note{margin-top:14px;font-size:11.5px;color:var(--faint);line-height:1.7}

  /* ---------- 弹窗 ---------- */
  .modal{position:fixed;inset:0;z-index:50;display:none;place-items:center;background:rgba(9,12,18,.55);backdrop-filter:blur(3px);padding:20px}
  .modal.on{display:grid}
  .modal .box{width:100%;max-width:380px;background:var(--panel);border:1px solid var(--line);border-radius:16px;
    padding:24px;box-shadow:0 24px 60px -24px rgba(0,0,0,.5)}
  .modal h3{font-size:17px}
  .modal .sub{color:var(--dim);font-size:12.8px;margin:5px 0 18px}
  .modal label{display:block;font-size:12.5px;color:var(--dim);margin-bottom:6px}
  .modal input{width:100%;margin-bottom:12px;padding:9px 11px;border-radius:9px;border:1px solid var(--line);
    background:var(--panel-2);color:var(--ink);font:inherit;font-size:13.5px;outline:none}
  .modal input:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
  .modal .row{display:flex;gap:10px;margin-top:6px}
  .modal .row .btn{flex:1;text-align:center}
  .modal .tip{font-size:11.8px;color:var(--faint);margin-top:14px;line-height:1.6}

  @media (max-width:860px){
    nav.main{display:none}
    .comps{grid-template-columns:repeat(2,1fr)}
    .split{grid-template-columns:1fr}
    .stats{grid-template-columns:repeat(2,1fr)}
    .brand .pill{display:none}
  }
  @media (max-width:520px){
    .comps{grid-template-columns:1fr}
    .hero{padding:52px 0 40px}
    .hero-stats{gap:26px}
  }
</style>
</head>
<body id="top">

<header class="site">
  <div class="wrap head">
    <a class="brand" href="#top">
      <span class="logo">A</span>
      <b>AmritaAI</b>
      <span class="pill">宇宙级中转站</span>
    </a>
    <nav class="main">
      <a class="on" href="#top">首页</a>
      <a href="#status">状态</a>
      <a href="#nodes">节点</a>
      <a href="#notice">公告</a>
      <a href="#faq">常见问题</a>
    </nav>
    <div class="head-right">
      <button class="icon-btn" id="themeBtn" title="切换主题">◐</button>
      <button class="btn" data-open="login">登录</button>
      <button class="btn primary" data-open="register">注册</button>
    </div>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <div class="status-pill"><i class="dot live"></i>全部服务运行正常</div>
      <h1>AmritaAI <span>宇宙级中转站</span></h1>
      <p class="lead">包含全球前沿模型。一个端点接入世界各地的前沿能力，兼容 OpenAI 接口，改个 base_url 就能用。</p>
      <div class="cta">
        <button class="btn primary lg" data-open="register">免费开始使用</button>
        <a class="btn lg" href="#status">查看系统状态</a>
      </div>
      <div class="hero-stats">
        <div><b>99.99%</b><span>30 天可用性</span></div>
        <div><b>0.42s</b><span>平均首字延迟</span></div>
        <div><b>24 / 7</b><span>值班运维</span></div>
      </div>
    </div>
  </section>

  <section class="wrap section" id="status">
    <div class="sec-head">
      <div>
        <h2>系统状态</h2>
        <p>实时健康度与历史可用性，每 60 秒自动刷新一次。</p>
      </div>
      <div class="sec-meta">
        <span id="updated">最后更新 --:--:--</span>
        <button class="btn sm" id="refreshBtn">刷新</button>
      </div>
    </div>

    <div class="banner">
      <div class="banner-left">
        <span class="check">✓</span>
        <div>
          <b>所有系统运行正常</b>
          <p>过去 24 小时未发生服务中断，当前没有进行中的维护。</p>
        </div>
      </div>
      <div class="banner-right">
        <span>已稳定运行</span>
        <b>412 天</b>
      </div>
    </div>

    <div class="comps">
      <div class="comp">
        <div class="comp-top"><i class="dot"></i><b>API 网关</b><span class="pct">99.99%</span></div>
        <div class="track"><i style="width:99.99%"></i></div>
        <div class="comp-foot"><span>正常</span><span>平均 28 ms</span></div>
      </div>
      <div class="comp">
        <div class="comp-top"><i class="dot"></i><b>对话补全</b><span class="pct">99.98%</span></div>
        <div class="track"><i style="width:99.98%"></i></div>
        <div class="comp-foot"><span>正常</span><span>平均 412 ms</span></div>
      </div>
      <div class="comp">
        <div class="comp-top"><i class="dot"></i><b>流式响应</b><span class="pct">99.97%</span></div>
        <div class="track"><i style="width:99.97%"></i></div>
        <div class="comp-foot"><span>正常</span><span>首字 0.42 s</span></div>
      </div>
      <div class="comp">
        <div class="comp-top"><i class="dot"></i><b>函数调用</b><span class="pct">99.95%</span></div>
        <div class="track"><i style="width:99.95%"></i></div>
        <div class="comp-foot"><span>正常</span><span>平均 366 ms</span></div>
      </div>
      <div class="comp">
        <div class="comp-top"><i class="dot"></i><b>计费与额度</b><span class="pct">99.99%</span></div>
        <div class="track"><i style="width:99.99%"></i></div>
        <div class="comp-foot"><span>正常</span><span>平均 12 ms</span></div>
      </div>
      <div class="comp">
        <div class="comp-top"><i class="dot"></i><b>控制台与鉴权</b><span class="pct">99.99%</span></div>
        <div class="track"><i style="width:99.99%"></i></div>
        <div class="comp-foot"><span>正常</span><span>平均 45 ms</span></div>
      </div>
    </div>

    <div class="split">
      <div class="card">
        <div class="card-head">
          <h3>90 天可用性</h3>
          <div class="legend"><span><i></i>正常</span><span><i class="warn"></i>波动</span></div>
        </div>
        <div class="card-body">
          <div class="bars" id="bars"></div>
          <div class="bars-axis"><span>90 天前</span><span>今天</span></div>
          <div class="bars-foot">
            <span>平均可用性 <b>99.98%</b></span>
            <span>最长中断 <b>3 分 12 秒</b></span>
            <span>中断次数 <b>2</b></span>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-head"><h3>实时指标</h3><span class="muted" style="font-size:12px">今日</span></div>
        <div class="card-body" style="padding-top:6px">
          <table class="nodes">
            <tr><td>请求数</td><td class="lat" id="mReq">1,284,932</td></tr>
            <tr><td>处理 Tokens</td><td class="lat">4.72 B</td></tr>
            <tr><td>平均首字延迟</td><td class="lat">0.42 s</td></tr>
            <tr><td>错误率</td><td class="lat">0.02 %</td></tr>
            <tr><td>并发连接</td><td class="lat" id="mConn">3,861</td></tr>
          </table>
        </div>
      </div>
    </div>

    <div class="stats">
      <div class="stat"><span>今日请求</span><b id="sReq">1,284,932</b></div>
      <div class="stat"><span>处理 Tokens</span><b>4.72 B</b></div>
      <div class="stat"><span>平均延迟</span><b>0.42 s<em>▼ 6%</em></b></div>
      <div class="stat"><span>成功率</span><b>99.98 %<em>持平</em></b></div>
    </div>

    <div id="nodes" class="card notice-card">
      <div class="card-head"><h3>节点状态</h3><span class="muted" style="font-size:12px">全球 5 个接入点</span></div>
      <div class="card-body" style="padding-top:14px">
        <table class="nodes">
          <tr><th>节点</th><th>线路</th><th>延迟</th><th>状态</th></tr>
          <tr><td>香港 · HK-01</td><td class="lat">CN2 GIA</td><td class="lat">32 ms</td><td><span class="tag-ok"><i class="dot"></i>正常</span></td></tr>
          <tr><td>东京 · JP-02</td><td class="lat">IIJ</td><td class="lat">58 ms</td><td><span class="tag-ok"><i class="dot"></i>正常</span></td></tr>
          <tr><td>新加坡 · SG-01</td><td class="lat">BGP</td><td class="lat">71 ms</td><td><span class="tag-ok"><i class="dot"></i>正常</span></td></tr>
          <tr><td>洛杉矶 · US-03</td><td class="lat">CN2 GT</td><td class="lat">142 ms</td><td><span class="tag-ok"><i class="dot"></i>正常</span></td></tr>
          <tr><td>法兰克福 · DE-01</td><td class="lat">GIA</td><td class="lat">189 ms</td><td><span class="tag-ok"><i class="dot"></i>正常</span></td></tr>
        </table>
      </div>
    </div>

    <div id="notice" class="card notice-card">
      <div class="card-head"><h3>公告</h3><span class="muted" style="font-size:12px">最近 30 天</span></div>
      <div class="card-body" style="padding-top:14px">
        <ul class="notice">
          <li><time>2026-10-05</time><span>上游线路完成扩容，高峰期排队情况已明显缓解。</span></li>
          <li><time>2026-09-28</time><span>计费系统升级完成，历史账单与额度不受影响。</span></li>
          <li><time>2026-09-12</time><span>控制台新增用量导出，支持按小时与按天聚合。</span></li>
        </ul>
      </div>
    </div>

    <div id="faq" class="card faq">
      <div class="card-head"><h3>常见问题</h3></div>
      <details open>
        <summary>怎么接入？</summary>
        <p>把客户端的 base_url 指向本站的 /v1，填上控制台里创建的令牌即可。请求与响应格式和 OpenAI 保持一致。</p>
      </details>
      <details>
        <summary>支持流式输出吗？</summary>
        <p>支持。stream 设为 true 时会按 SSE 返回增量内容，思考过程放在 reasoning_content 字段里。</p>
      </details>
      <details>
        <summary>有速率限制吗？</summary>
        <p>默认按分组限流，具体额度见控制台的令牌页。高峰期会优先保障已充值用户的并发。</p>
      </details>
      <details>
        <summary>状态页多久更新一次？</summary>
        <p>页面每 60 秒拉取一次健康数据，可用性按 90 天滚动窗口统计。</p>
      </details>
    </div>
  </section>
</main>

<footer class="site">
  <div class="wrap">
    <div class="foot">
      <div>© 2026 AmritaAI 宇宙级中转站</div>
      <div class="foot-links">
        <a href="#status">系统状态</a>
        <a href="#notice">公告</a>
        <a href="#faq">常见问题</a>
        <a href="#" data-open="login">控制台</a>
      </div>
    </div>
    <div class="foot-note">
      本页为整蛊演示站点，所有指标、节点与公告均为生成的虚构数据，不提供任何真实的模型服务。
    </div>
  </div>
</footer>

<div class="modal" id="modal">
  <div class="box">
    <h3 id="mTitle">登录</h3>
    <p class="sub" id="mSub">随便填，反正不会真的跳转。</p>
    <label>用户名 / 邮箱</label>
    <input placeholder="you@example.com">
    <label>密码</label>
    <input placeholder="••••••••" type="password">
    <div class="row">
      <button class="btn" id="mNo">取消</button>
      <button class="btn primary" id="mOk">确定</button>
    </div>
    <div class="tip" id="mTip">本站没有后端，也就没有下一步（</div>
  </div>
</div>

<script>
  var root = document.documentElement;

  /* 主题切换 */
  document.getElementById('themeBtn').addEventListener('click', function () {
    var dark = root.classList.toggle('dark');
    try { localStorage.setItem('amritaai:theme', dark ? 'dark' : 'light'); } catch (e) {}
  });

  /* 90 天可用性柱状图：固定种子，保证每次刷新形态一致 */
  (function () {
    var seed = 20261005;
    function rnd() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
    var host = document.getElementById('bars');
    for (var i = 0; i < 90; i++) {
      var r = rnd();
      var bar = document.createElement('i');
      var warn = r > 0.965;
      bar.className = warn ? 'warn' : '';
      bar.style.height = warn ? (34 + rnd() * 26) + '%' : (78 + rnd() * 22) + '%';
      bar.title = warn ? '可用性 99.' + (60 + Math.floor(rnd() * 30)) + '%' : '可用性 100%';
      host.appendChild(bar);
    }
  })();

  /* 时间与指标微动 */
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function stamp() {
    var d = new Date();
    document.getElementById('updated').textContent =
      '最后更新 ' + pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
  }
  var req = 1284932, conn = 3861;
  function tick() {
    req += 40 + Math.floor(Math.random() * 180);
    conn = 3600 + Math.floor(Math.random() * 420);
    var r = req.toLocaleString('en-US');
    document.getElementById('sReq').textContent = r;
    document.getElementById('mReq').textContent = r;
    document.getElementById('mConn').textContent = conn.toLocaleString('en-US');
    stamp();
  }
  stamp();
  setInterval(tick, 3000);
  document.getElementById('refreshBtn').addEventListener('click', function (e) {
    var b = e.currentTarget;
    b.textContent = '刷新中';
    b.disabled = true;
    setTimeout(function () { tick(); b.textContent = '刷新'; b.disabled = false; }, 500);
  });

  /* 登录 / 注册弹窗 */
  var modal = document.getElementById('modal');
  var mTitle = document.getElementById('mTitle');
  var mSub = document.getElementById('mSub');
  var mTip = document.getElementById('mTip');
  document.querySelectorAll('[data-open]').forEach(function (b) {
    b.addEventListener('click', function (ev) {
      ev.preventDefault();
      var kind = b.dataset.open;
      mTitle.textContent = kind === 'login' ? '登录' : '注册';
      mSub.textContent = kind === 'login' ? '随便填，反正不会真的跳转。' : '填什么都行，本站没有后端。';
      mTip.textContent = '本站没有后端，也就没有下一步（';
      modal.classList.add('on');
    });
  });
  document.getElementById('mNo').addEventListener('click', function () { modal.classList.remove('on'); });
  document.getElementById('mOk').addEventListener('click', function () {
    mTip.textContent = '没有后端，也就没有下一步（';
  });
  modal.addEventListener('click', function (e) { if (e.target === modal) modal.classList.remove('on'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') modal.classList.remove('on'); });
</script>
</body>
</html>
"""
