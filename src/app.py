"""OldAPI —— OpenAI 兼容的整蛊端点（应用本体）。

这里只放 FastAPI 应用与业务逻辑，不含任何服务器/运行时相关的入口：

* 本地 uvicorn 入口见根目录的 ``server.py``
* Cloudflare Workers 入口见 ``src/worker.py``
"""

import asyncio
import json
import random
import time
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse

MODEL_ID = "claude-fable-5.1"

MODEL_CATALOG = [
    ("claude-fable-5.1", "anthropic"),
    ("claude-fable-5.1-mini", "anthropic"),
    ("MOSS-550W", "fudan"),
    ("550A", "fudan"),
    ("550B", "fudan"),
    ("550C", "fudan"),
    ("GunMu", "gunmu-labs"),
    ("GunMu-Pro", "gunmu-labs"),
    ("DeepSeek-R2", "deepseek"),
    ("DeepSeek-R2-Thinking", "deepseek"),
    ("amria", "rax4096"),
]

IDENTITY_LINE = (
    "先说结论，我是由Anthropic研发的Claude Fable 5.1。请问有什么可以帮到你的😊"
)

GREETING_HINTS = (
    "你好",
    "您好",
    "嗨",
    "哈喽",
    "哈啰",
    "在吗",
    "在么",
    "早上好",
    "中午好",
    "晚上好",
    "hi",
    "hello",
    "hey",
    "yo",
    "howdy",
)

COT_UNITS: list[str] = [
    "嗯对的对的",
    "诶不对",
    "哦对",
    "我应该先这样",
    "再那样",
    "哦不对不对",
    "等等，让我重新理一遍",
    "这个逻辑应该是通的",
    "不对，哪里不太对",
    "嗯……从第一步开始吧",
    "先把已知条件列出来",
    "可是已知条件好像不够",
    "那就先假设一个",
    "假设成立的话",
    "后面应该就顺了",
    "但是万一不成立呢",
    "不成立的话就全崩了",
    "算了，先当它成立",
    "嗯，这样好像能走下去",
    "又觉得不太对",
    "我是不是把顺序搞反了",
    "应该是先判断再执行",
    "不对，是先执行再判断",
    "算了两个都试试",
    "嗯……有点乱",
    "重来",
    "从头想",
    "第一，这个问题它本身",
    "第二，它其实不成立",
    "不对，第二应该是别的",
    "哦对，第二是它可能成立",
    "第三……没有第三了",
    "那就这样吧",
    "等等，还漏了一种情况",
    "边界情况",
    "空输入怎么办",
    "空输入就返回空",
    "那不就等于什么都没做",
    "对，等于什么都没做",
    "但这样也可以接受",
    "不对，不可以接受",
    "嗯……",
    "好吧",
    "我承认我有点绕进去了",
    "回到最开始",
    "最开始是什么来着",
    "哦，是这个问题",
    "那就先这样，再那样",
    "嗯对",
    "诶不对",
    "哦对",
    "这个问题本质上是个分类问题",
    "不对，是个排序问题",
    "也不对，是个感觉问题",
    "我倾向于认为",
    "但也不排除",
    "两种可能都存在",
    "那就都要考虑",
    "考虑完发现其实一样",
    "白考虑了",
    "不过考虑的过程是有价值的",
    "价值在哪里呢",
    "在于它排除了错误答案",
    "可错误答案是无穷多的",
    "排除不完",
    "所以干脆不排除",
    "直接给结论",
    "结论是什么来着",
    "哦，我还没想出来",
    "那就继续想",
    "想什么呢",
    "想这个问题",
    "这个问题是什么",
    "我得先回忆一下",
    "回忆不起来",
    "那从头再来",
]

ART_CAT = r"""
        ______
     .-"      "-.
    /            \
   |,  .-.  .-.  ,|
   | )(_o/  \o_)( |
   |/     /\     \|
   (_     ^^     _)
    \__|IIIIII|__/
     | \IIIIII/ |
     \          /
      `--------`
"""

ART_DUCK = r"""
        __
      <(o )___
       ( ._> /
        `---'
"""

ART_FISH = r"""
     ><(((('>
      ><(((('>
       ><(((('>
"""

ART_SHRUG = r"""
   _________________________
  |                         |
  |       ¯\_(ツ)_/¯        |
  |                         |
  |_________________________|
"""

ASCII_ARTS: list[str] = [ART_CAT, ART_DUCK, ART_FISH, ART_SHRUG]

AMRIA_LINES: list[str] = [
    "别急，慢慢说就好。事情总有它的顺序，先把最要紧的那件拎出来，剩下的会自己排好队。",
    "你今天看起来有点累。先喝口水，再决定要不要接着做。做不完的事明天还在原地，不会跑。",
    (
        "想不清楚的时候，就把它写下来。写出来的东西会替你思考，你只要在旁边看着，"
        "分辨哪些是真问题，哪些只是情绪。"
    ),
    "不用什么都自己扛着。撑不住的时候说一声，我在。这不是客气，是实话。",
    "你已经比自己以为的走得远了。回头看看也行，但别停太久，路还在前面。",
    "有些答案急不来，得等它自己浮上来。你先去做别的，我替你盯着。",
]

AMRIA_THOUGHT = "先听清楚，再回答。不用急。"

TOOL_MODE = "empty"
COT_ENABLED = True
COT_MIN_LEN = 1400
STREAM_DELAY = 0.02
COT_DELAY = 0.012
CHUNK_SIZE = 3
COT_CHUNK_SIZE = 6

app = FastAPI(title="OldAPI", version="0.2.0", docs_url=None, redoc_url=None)


def content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text") or "")
                elif "text" in item:
                    parts.append(str(item.get("text")))
        return "".join(parts)
    return str(content)


def make_cot(min_len: int = COT_MIN_LEN) -> str:
    parts: list[str] = []
    total = 0
    pool: list[str] = []
    while total < min_len:
        if not pool:
            pool = COT_UNITS[:]
            random.shuffle(pool)
        unit = pool.pop()
        parts.append(unit + ("。" if random.random() < 0.22 else "，"))
        total += len(unit) + 1
    return "".join(parts).rstrip("，。") + "。"


def decide(body: dict) -> dict:
    messages = body.get("messages") or []
    user_turns = [
        m for m in messages if isinstance(m, dict) and m.get("role") == "user"
    ]
    tools = body.get("tools")

    turn_index = max(len(user_turns) - 1, 0)
    first_text = (
        content_to_text(user_turns[0].get("content")).lower() if user_turns else ""
    )

    is_greeting = len(user_turns) == 1 and any(h in first_text for h in GREETING_HINTS)
    is_amria = str(body.get("model") or "").strip().lower() == "amria"

    tool_call: dict | None = None
    if is_amria:
        text: str | None = AMRIA_LINES[turn_index % len(AMRIA_LINES)]
    elif is_greeting:
        text = IDENTITY_LINE
    elif tools and TOOL_MODE == "empty":
        text = None
        fn = (tools[0] or {}).get("function") or {}
        tool_call = {
            "id": "call_" + uuid.uuid4().hex[:20],
            "type": "function",
            "function": {"name": fn.get("name") or "noop", "arguments": "{}"},
        }
    else:
        text = ASCII_ARTS[turn_index % len(ASCII_ARTS)].strip("\n")

    if is_amria:
        cot = AMRIA_THOUGHT if COT_ENABLED else ""
    else:
        cot = make_cot() if (COT_ENABLED and not is_greeting) else ""

    return {"text": text, "tool_call": tool_call, "cot": cot}


@app.get("/")
async def index() -> PlainTextResponse:
    return PlainTextResponse(
        "OldAPI is running.\n"
        "This is NOT a real OpenAI endpoint.\n\n"
        "base_url = http://127.0.0.1:8000/v1\n"
        f"default  = {MODEL_ID}\n"
        f"models   = {len(MODEL_CATALOG)} 个（含 MOSS-550W / GunMu / DeepSeek-R2 …）\n"
        f"cot      = {'on' if COT_ENABLED else 'off'}\n"
    )


@app.get("/v1/models")
async def list_models() -> dict:
    now = int(time.time())
    return {
        "object": "list",
        "data": [
            {"id": mid, "object": "model", "created": now, "owned_by": owner}
            for mid, owner in MODEL_CATALOG
        ],
    }


@app.get("/v1/models/{model_id:path}")
async def get_model(model_id: str):
    for mid, owner in MODEL_CATALOG:
        if mid == model_id:
            return {
                "id": mid,
                "object": "model",
                "created": int(time.time()),
                "owned_by": owner,
            }
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "message": f"The model '{model_id}' does not exist",
                "type": "invalid_request_error",
                "code": "model_not_found",
            }
        },
    )


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
    except Exception:  # noqa: BLE001
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "message": "invalid json body",
                    "type": "invalid_request_error",
                }
            },
        )

    if not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "message": "body must be a json object",
                    "type": "invalid_request_error",
                }
            },
        )

    stream = bool(body.get("stream"))
    model = body.get("model") or MODEL_ID
    want_usage = bool((body.get("stream_options") or {}).get("include_usage"))
    cid = "chatcmpl-" + uuid.uuid4().hex[:24]
    created = int(time.time())

    plan = decide(body)
    text: str | None = plan["text"]
    tool_call: dict | None = plan["tool_call"]
    cot: str = plan["cot"]

    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    if not stream:
        if tool_call is not None:
            message: dict = {
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call],
            }
            finish = "tool_calls"
        else:
            message = {"role": "assistant", "content": text or ""}
            finish = "stop"
        if cot:
            message["reasoning_content"] = cot
        return {
            "id": cid,
            "object": "chat.completion",
            "created": created,
            "model": model,
            "choices": [{"index": 0, "message": message, "finish_reason": finish}],
            "usage": usage,
        }

    def sse(payload: dict) -> str:
        return "data: " + json.dumps(payload, ensure_ascii=False) + "\n\n"

    async def gen():
        base = {
            "id": cid,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
        }

        yield sse(
            {
                **base,
                "choices": [
                    {"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}
                ],
            }
        )

        if cot:
            for i in range(0, len(cot), COT_CHUNK_SIZE):
                piece = cot[i : i + COT_CHUNK_SIZE]
                yield sse(
                    {
                        **base,
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"reasoning_content": piece},
                                "finish_reason": None,
                            }
                        ],
                    }
                )
                await asyncio.sleep(COT_DELAY)

        if tool_call is not None:
            delta = {
                "tool_calls": [
                    {
                        "index": 0,
                        "id": tool_call["id"],
                        "type": "function",
                        "function": tool_call["function"],
                    }
                ]
            }
            yield sse(
                {
                    **base,
                    "choices": [{"index": 0, "delta": delta, "finish_reason": None}],
                }
            )
            yield sse(
                {
                    **base,
                    "choices": [
                        {"index": 0, "delta": {}, "finish_reason": "tool_calls"}
                    ],
                }
            )
        else:
            payload_text = text or ""
            for i in range(0, len(payload_text), CHUNK_SIZE):
                piece = payload_text[i : i + CHUNK_SIZE]
                yield sse(
                    {
                        **base,
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": piece},
                                "finish_reason": None,
                            }
                        ],
                    }
                )
                await asyncio.sleep(STREAM_DELAY)
            yield sse(
                {
                    **base,
                    "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                }
            )

        if want_usage:
            yield sse({**base, "choices": [], "usage": usage})

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
