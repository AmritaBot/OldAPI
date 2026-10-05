"""OldAPI 主页模板（内联字符串，兼容 Workers 无文件系统的运行时）。

``__MODELS__`` / ``__QUOTES__`` 两个占位符由 src/app.py 在首次请求时替换。
"""

INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OldAPI · 中转站</title>
<style>
  :root{
    --bg:#0b0d12; --panel:#12151d; --line:#222836; --ink:#e7ecf5; --dim:#8a93a6;
    --accent:#6ea8ff; --accent2:#9b7bff; --ok:#4ad19a;
  }
  *{box-sizing:border-box}
  body{margin:0;background:radial-gradient(1200px 600px at 80% -10%,#1a2340 0%,var(--bg) 55%);color:var(--ink);
    font:15px/1.6 ui-sans-serif,system-ui,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif}
  a{color:inherit;text-decoration:none}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px}
  header{position:sticky;top:0;backdrop-filter:blur(12px);background:rgba(11,13,18,.7);border-bottom:1px solid var(--line);z-index:9}
  .nav{display:flex;align-items:center;gap:26px;height:62px}
  .brand{font-weight:700;font-size:19px;letter-spacing:.3px}
  .brand span{background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}
  .nav nav{display:flex;gap:20px;color:var(--dim);font-size:14px}
  .nav nav a:hover{color:var(--ink)}
  .spacer{flex:1}
  .btn{cursor:pointer;border:1px solid var(--line);background:var(--panel);color:var(--ink);
    padding:7px 15px;border-radius:9px;font-size:14px}
  .btn:hover{border-color:#39445c}
  .btn.primary{border:none;background:linear-gradient(90deg,var(--accent),var(--accent2));color:#08101f;font-weight:600}
  .hero{padding:72px 0 40px;text-align:center}
  .tag{display:inline-block;font-size:12px;color:var(--ok);border:1px solid #1f4a38;background:#0e1f18;
    padding:4px 10px;border-radius:999px;margin-bottom:20px}
  .hero h1{margin:0 0 14px;font-size:44px;line-height:1.15;letter-spacing:-.5px}
  .hero h1 em{font-style:normal;background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;background-clip:text;color:transparent}
  .hero p{color:var(--dim);max-width:560px;margin:0 auto 26px}
  .cta{display:flex;gap:12px;justify-content:center}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;padding:26px 0 10px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}
  .card .id{font-weight:600;font-size:14px}
  .card .own{color:var(--dim);font-size:12px;margin-top:2px}
  .card .quote{margin-top:12px;color:#c3cbdb;font-size:13px;border-left:2px solid #2b3448;padding-left:10px;min-height:34px}
  .sec-title{margin:40px 0 6px;font-size:18px}
  .sec-sub{color:var(--dim);font-size:13px;margin-bottom:6px}
  .foot{border-top:1px solid var(--line);margin-top:56px;padding:22px 0 40px;color:var(--dim);font-size:12.5px}
  .modal{position:fixed;inset:0;display:none;place-items:center;background:rgba(4,6,10,.66);z-index:20}
  .modal.on{display:grid}
  .box{width:340px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px}
  .box h3{margin:0 0 4px;font-size:17px}
  .box p{color:var(--dim);font-size:12.5px;margin:0 0 16px}
  .box input{width:100%;margin-bottom:10px;padding:9px 11px;border-radius:9px;border:1px solid var(--line);
    background:#0d1017;color:var(--ink);outline:none}
  .box input:focus{border-color:#39445c}
  .box .row{display:flex;gap:10px;margin-top:4px}
  .box .row .btn{flex:1;text-align:center}
  .note{font-size:12px;color:var(--dim);margin-top:12px}
</style>
</head>
<body>
<header>
  <div class="wrap nav">
    <div class="brand">Old<span>API</span></div>
    <nav>
      <a href="#models">模型</a>
      <a href="#play">试玩</a>
      <a href="#">文档</a>
      <a href="#">状态</a>
    </nav>
    <div class="spacer"></div>
    <button class="btn" data-open="login">登录</button>
    <button class="btn primary" data-open="register">注册</button>
  </div>
</header>

<div class="wrap">
  <section class="hero">
    <div class="tag">● 运行中 · 非真实 API</div>
    <h1>一个接口，<em>十一张脸</em></h1>
    <p>OpenAI 兼容，模型全真名，回答全胡说。OldAPI 是一个玩笑中转站，不是任何真实厂商的服务。</p>
    <div class="cta">
      <button class="btn primary" data-open="register">免费注册</button>
      <a class="btn" href="/v1/models">查看 /v1/models</a>
    </div>
  </section>

  <h2 class="sec-title" id="models">可用模型</h2>
  <div class="sec-sub">点开任意一张卡片，看看它第一次会怎么开口。</div>
  <div class="grid" id="modelGrid"></div>

  <h2 class="sec-title" id="play">它是怎么骗你的</h2>
  <div class="sec-sub">请求照收，格式照给，就是内容不太对。</div>
  <pre class="card" style="overflow:auto"><code>curl -s https://ai.amritabot.com/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"claude-fable-5.1","messages":[{"role":"user","content":"你好"}]}'</code></pre>

  <div class="foot">
    OldAPI is running. This is NOT a real OpenAI endpoint. 模型名属于各自的厂商，与本站无关；
    所有输出均为玩笑，请勿引用。
  </div>
</div>

<div class="modal" id="modal">
  <div class="box">
    <h3 id="mTitle">登录</h3>
    <p id="mSub">随便填，反正不会真的跳转。</p>
    <input placeholder="用户名 / 邮箱">
    <input placeholder="密码" type="password">
    <div class="row">
      <button class="btn primary" id="mOk">确定</button>
      <button class="btn" id="mNo">取消</button>
    </div>
    <div class="note" id="mNote"></div>
  </div>
</div>

<script>
const MODELS = __MODELS__;
const QUOTES = __QUOTES__;

const grid = document.getElementById('modelGrid');
MODELS.forEach(m => {
  const q = QUOTES[m.id] || QUOTES['claude-fable-5.1'] || '';
  const el = document.createElement('div');
  el.className = 'card';
  el.innerHTML = '<div class="id">' + m.id + '</div>'
    + '<div class="own">owned_by ' + m.owned_by + '</div>'
    + '<div class="quote">' + (Array.isArray(q) ? q[0] : q) + '</div>';
  grid.appendChild(el);
});

const modal = document.getElementById('modal');
const mTitle = document.getElementById('mTitle');
const mSub = document.getElementById('mSub');
const mNote = document.getElementById('mNote');
document.querySelectorAll('[data-open]').forEach(b => b.addEventListener('click', () => {
  const kind = b.dataset.open;
  mTitle.textContent = kind === 'login' ? '登录' : '注册';
  mSub.textContent = kind === 'login' ? '随便填，反正不会真的跳转。' : '填什么都行，本站没有后端。';
  mNote.textContent = '';
  modal.classList.add('on');
}));
document.getElementById('mNo').addEventListener('click', () => modal.classList.remove('on'));
document.getElementById('mOk').addEventListener('click', () => {
  mNote.textContent = '没有后端，也就没有下一步（';
});
modal.addEventListener('click', e => { if (e.target === modal) modal.classList.remove('on'); });
</script>
</body>
</html>
"""
