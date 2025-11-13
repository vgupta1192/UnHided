# run.py
# Expose the real app as `main_app` and provide explicit GET + HEAD /health handlers.
from fastapi import FastAPI
from starlette.responses import JSONResponse, Response
from mediaflow_proxy.main import app as _real_app

wrapper = FastAPI()

@wrapper.get("/health")
async def _health_get():
    # return JSON for GET requests
    return JSONResponse({"status": "healthy"})

@wrapper.head("/health")
async def _health_head():
    # explicitly respond to HEAD with 200 and no body
    return Response(status_code=200)

# Mount the real app so all existing routes + static files still work.
wrapper.mount("/", _real_app)

# Expose the wrapper as the name Render expects
main_app = wrapper
