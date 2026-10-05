# fakegpt

一个「OpenAI 兼容」端点的整蛊后端（本地版，Python + FastAPI）。

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

## 安装与运行

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
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

## 接到客户端

把客户端（Cherry Studio / NextChat / 各种 OpenAI SDK）的 base_url 指向：

```
http://127.0.0.1:8000/v1
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

## 边界说明

- **不记录、不回显、不落盘任何 Authorization / api-key**，收到即丢弃。
  这一点是刻意写死的，别改。
- 只面向本地自娱，请勿部署到公网冒充他人服务。
