# run.py
# Expose the real app as `main_app` and provide a guaranteed /health endpoint.
# This ensures `uvicorn run:main_app` will serve /health regardless of internals.
from fastapi import FastAPI
from mediaflow_proxy.main import app as _real_app

# wrapper app that provides /health and then mounts the real app at root
wrapper = FastAPI()

@wrapper.get("/health")
async def _health():
    return {"status": "healthy"}

# Mount the real app so all existing routes + static files still work.
wrapper.mount("/", _real_app)

# Expose the wrapper as the name Render expects
main_app = wrapper
