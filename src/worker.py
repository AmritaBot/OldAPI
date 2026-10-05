"""Cloudflare Workers 入口。

FastAPI 应用本体在 ``src/app.py``，这里只把它接到 Workers 的 ASGI 适配器上。
行为与本地 ``python server.py``（uvicorn）完全一致。
"""

from workers import asgi

from app import app

# workerd 会查找名为 Default 的入口点。
Default = asgi.entrypoint(app)
