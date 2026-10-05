#!/usr/bin/env python3
"""OldAPI 本地运行入口（uvicorn）。

应用本体在 ``src/app.py``；Cloudflare Workers 入口在 ``src/worker.py``。
参数、打印内容与运行行为与原版保持一致。
"""

import argparse
import os
import sys

# 允许从任意工作目录运行本脚本（原版是单文件，没有这个限制）。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

import src.app as app_module


def main() -> None:
    ap = argparse.ArgumentParser(description="OldAPI —— OpenAI 兼容的整蛊端点")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--tool-mode", choices=["empty", "ignore"], default="empty")
    ap.add_argument("--delay", type=float, default=0.02)
    ap.add_argument("--cot", dest="cot", action="store_true", default=True)
    ap.add_argument("--no-cot", dest="cot", action="store_false")
    ap.add_argument("--cot-len", type=int, default=1400)
    args = ap.parse_args()

    app_module.TOOL_MODE = args.tool_mode
    app_module.STREAM_DELAY = args.delay
    app_module.COT_ENABLED = args.cot
    app_module.COT_MIN_LEN = args.cot_len

    print(f"OldAPI  ->  http://{args.host}:{args.port}/v1")
    print(
        f"model={app_module.MODEL_ID}  tool-mode={app_module.TOOL_MODE}  cot={'on' if app_module.COT_ENABLED else 'off'}"
    )

    uvicorn.run(app_module.app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
