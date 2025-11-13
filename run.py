# run.py
# Expose the real app as `main_app` and provide a permissive /health route
# that accepts GET, HEAD and OPTIONS so any probe will get 200.
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, Response
from mediaflow_proxy.main import app as _real_app

wrapper = FastAPI()

@wrapper.api_route("/health", methods=["GET", "HEAD", "OPTIONS"])
async def _health(request: Request):
    # respond 200 for GET/HEAD/OPTIONS. Return JSON for GET, no body for HEAD.
    if request.method == "GET":
        return JSONResponse({"status": "healthy"})
    # For HEAD / OPTIONS, return empty 200 response
    return Response(status_code=200)

# Mount the real app so all existing routes + static files still work.
wrapper.mount("/", _real_app)

# Expose the wrapper as the name Render expects
main_app = wrapper
