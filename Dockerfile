FROM python:3.11-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# Minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends git \
  && rm -rf /var/lib/apt/lists/*

# Clone YOUR fork (never upstream)
RUN git clone https://github.com/vgupta1192/UnHided .

# Python deps + faster uvicorn stack
RUN python -m pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir "uvicorn[standard]"

# Optional: run as non-root
RUN useradd -m appuser
USER appuser

EXPOSE 7860

# App’s logger expects uppercase level
ENV LOG_LEVEL=WARNING

# Single-process uvicorn (lightest)
CMD ["uvicorn","run:main_app","--host","0.0.0.0","--port","7860"]