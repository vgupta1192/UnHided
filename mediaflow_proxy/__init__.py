# mediaflow_proxy/__init__.py
# expose the FastAPI app defined in main.py so package-level imports like
# `mediaflow_proxy:app` will work correctly (includes /health route).
from .main import app  # noqa: F401

__all__ = ["app"]
