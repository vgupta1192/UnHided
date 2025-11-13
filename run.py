# run.py
# Expose the FastAPI app as `main_app` so Render's uvicorn run:main_app uses the correct instance.
from mediaflow_proxy.main import app as main_app
