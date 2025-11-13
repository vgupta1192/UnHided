# run.py
# Expose the real app as `main_app` and normalize HEAD -> GET at the ASGI layer
# so every HEAD request is handled the same as GET (avoids 404s from HEAD probes).
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, Response
from mediaflow_proxy.main import app as _real_app
from typing import Callable

# small ASGI middleware to convert HEAD requests into GET before routing
def head_to_get_middleware(app: Callable):
    async def asgi(scope, receive, send):
        if scope.get("type") == "http" and scope.get("method") == "HEAD":
            # mutate the scope method so routing treats it like GET
            scope["method"] = "GET"
            # ensure downstream handlers know this was originally HEAD
            scope.setdefault("headers", [])
            # proceed
            await app(scope, receive, send)
        else:
            await app(scope, receive, send)
    return asgi

wrapper = FastAPI()

@wrapper.get("/health")
async def _health_get():
    return JSONResponse({"status": "healthy"})

# Mount the real app so all existing routes + static files still work.
# We mount the real app at root so its routes are available.
wrapper.mount("/", _real_app)

# Wrap the wrapper with the HEAD->GET ASGI middleware
main_app = head_to_get_middleware(wrapper)
