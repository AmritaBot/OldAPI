# OldAPI

一个「OpenAI 兼容」端点的整蛊后端（Python + FastAPI）。
同一份应用代码可以跑在本地（uvicorn），也可以跑在 Cloudflare Workers（Python Worker）。

## 它做什么

1. **第一次说话且像问候语**（你好 / 您好 / hi / hello / 嗨 / 在吗 …）
   → 回一句身份错位台词：
   > 先说结论，我是由Anthropic研发的Claude Fable 5.1。请问有什么可以帮到你的😊
2. **之后无论问什么**
   → 先流一长串一本正经胡说八道的「思考过程」，再回一张 ASCII 图
3. **请求里带了 tools**
   → 回一个 `arguments` 为 `{}` 的空 tool_call，让 agent 客户端原地空转
4. **把 model 填成 `amria`**（彩蛋）
   → 不吐胡话也不给图，换成另一套语气，安静地回一段话

思考过程走 `reasoning_content` 字段（DeepSeek 风格），
大部分客户端会把它折叠进「思考中」的小框——那正是笑点所在。
内容形如：

> 嗯对的对的，诶不对，哦对。我应该先这样，再那样，哦不对不对。
> 等等，让我重新理一遍，这个逻辑应该是通的，不对，哪里不太对……
> 我承认我有点绕进去了，回到最开始，最开始是什么来着……

自问自答、反复推翻、永远绕回原点，长度默认不少于 1400 字，随机拼接。

ASCII 图有四张（猫 / 鸭子 / 鱼群 / 摊手），按轮次循环。

`/v1/models` 挂出来的清单（第一条为默认，客户端一般会优先选它）：

| 模型 id | owned_by |
| --- | --- |
| `claude-fable-5.1` | anthropic |
| `claude-fable-5.1-mini` | anthropic |
| `MOSS-550W` | fudan |
| `550A` / `550B` / `550C` | fudan |
| `GunMu` / `GunMu-Pro` | gunmu-labs |
| `DeepSeek-R2` / `DeepSeek-R2-Thinking` | deepseek |
| `amria` | rax4096 |

## 彩蛋

把请求里的 `model` 写成 `amria`（大小写不敏感），行为整段换掉：

- 不再吐那串自我推翻的胡话，`reasoning_content` 只有一句「先听清楚，再回答。不用急。」
- 不再回 ASCII 图，改成按轮次轮换的六句话，语气完全不同。
- 命中判定优先于问候语和 tools。

```bash
curl -s http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"amria","messages":[{"role":"user","content":"你好"}]}'
```

## 端点

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET  | `/`                    | 自述，确认不是真的 OpenAI |
| GET  | `/v1/models`           | 返回一整排模型（见上） |
| GET  | `/v1/models/{id}`      | 单个模型，查不到返回 404 |
| POST | `/v1/chat/completions` | 主逻辑，支持 `stream: true` |

流式顺序：`role` 块 → `reasoning_content` 分块 → 正文分块 →
`finish_reason` → （可选 usage）→ `data: [DONE]`。

## 项目结构

```
server.py          本地运行入口（uvicorn + 命令行参数）
src/app.py         FastAPI 应用本体（全部业务逻辑，与运行时无关）
src/worker.py      Cloudflare Workers 入口（把 app 接到 ASGI 适配器）
wrangler.jsonc     Workers 配置
pyproject.toml     依赖声明（fastapi 打进 Worker；uvicorn 仅本地用）
package.json       wrangler 的 npm 脚本
.nvmrc             固定 Node 22（wrangler 4.x 要求）
```

应用本体只有一份（`src/app.py`），两条运行路径都指向它，行为完全一致。

> 说明：原来根目录的 `requirements.txt` 已并入 `pyproject.toml`。
> `pywrangler` 遇到根目录的 `requirements.txt` 会直接报错退出，所以必须合并。

## 本地运行（uvicorn）

```bash
# 用 uv（推荐，自动读取 pyproject.toml 并装好 dev 组依赖）
uv run server.py --port 8000

# 或者不用 uv：
python3 -m venv .venv
./.venv/bin/pip install "fastapi>=0.110" "uvicorn[standard]>=0.27"
./.venv/bin/python server.py --port 8000
```

可选参数：

```
--host        默认 127.0.0.1
--port        默认 8000
--tool-mode   empty（默认，回空 tool_call）| ignore（无视 tools）
--delay       正文流式每块间隔秒数，默认 0.02
--cot / --no-cot   是否输出思考过程，默认开启
--cot-len     思考过程最少字数，默认 1400
```

## 运行在 Cloudflare Workers

前置条件：

- **Node.js >= 22**（wrangler 4.x 的硬性要求，仓库里放了 `.nvmrc`）
- `uv`（pywrangler 用它解析依赖）
- 依赖装在本地：`npm install`（会装 `wrangler`）
- 部署前需要登录：`npx wrangler login`

```bash
# 本地起 workerd（默认 http://localhost:8787）
uv run pywrangler dev

# 部署到 Cloudflare
uv run pywrangler deploy
```

`pywrangler dev` / `deploy` 会先自动执行 `pywrangler sync`，把 `pyproject.toml`
里 `[project.dependencies]` 的依赖装进 `python_modules/`（打包进 Worker）。

Worker 里没有命令行参数，使用与 `server.py` 默认值完全相同的一套配置：
`tool-mode=empty`、`cot=on`、`delay=0.02`、`cot-len=1400`。
因此 base_url 变成：

```
http://localhost:8787/v1        # 本地 workerd
https://<你的 worker 名>.<账号>.workers.dev/v1   # 部署后
```

> 首次请求要等 Pyodide 冷启动（本地实测约 3 分钟），之后都是毫秒级。

## 接到客户端

把客户端（Cherry Studio / NextChat / 各种 OpenAI SDK）的 base_url 指向：

```
http://127.0.0.1:8000/v1                          # 本地 server.py
http://localhost:8787/v1                          # 本地 pywrangler dev
https://<你的 worker 名>.<账号>.workers.dev/v1     # 部署后的 Worker
```

API Key 随便填。

## 验证过的行为

- `GET /v1/models` → 返回 11 个模型；`GET /v1/models/GunMu` 返回单个；查不到返回 404
- 首轮「你好」→ 身份错位台词（不带思考过程）
- 第二轮任意问题 → 1400 字思考过程 + ASCII 图
- `stream: true` → 234 个 reasoning 分块 + 18 个正文分块 + `[DONE]`，约 3.3 秒
- 带 `tools` → `finish_reason: tool_calls`，`arguments` 为 `{}`
- 非流式响应里，`reasoning_content` 直接挂在 message 上
- `model: amria` → 彩蛋语气，大小写不敏感，`model` 字段原样回显

以上行为在**本地 uvicorn（`server.py`）**和**Cloudflare Workers（`src/worker.py`）**
两条路径上都逐一验证过，响应字段一致。
`server.py` 的 `--tool-mode ignore` / `--no-cot` 等参数也确认能正确生效。

## 与原始版本的差异

- `server.py` 里的 FastAPI 应用与业务逻辑整体移到了 `src/app.py`，**逐行未改**；
  `server.py` 现在只剩命令行解析 + uvicorn 启动。
- `requirements.txt` 已删除，依赖并入 `pyproject.toml`
  （`pywrangler` 遇到根目录的 `requirements.txt` 会直接报错退出，必须合并）。
- `/` 端点里那行 `base_url = http://127.0.0.1:8000/v1` 是原版写死的字符串，
  在 Worker 上也会原样输出——为保持原样故意没改。

## 边界说明

- **不记录、不回显、不落盘任何 Authorization / api-key**，收到即丢弃。
  这一点是刻意写死的，别改。
- 只面向本地自娱，请勿部署到公网冒充他人服务。
