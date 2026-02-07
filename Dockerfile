# Stage 1: Base
FROM python:3.14.3-slim-bookworm AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Stage 2: Builder
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install all dependencies (including dev)
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --dev --format requirements-txt --index https://download.pytorch.org/whl/cpu -o dev-requirements.txt
RUN uv pip install --system --no-cache --index-url https://pypi.org/simple --extra-index-url https://download.pytorch.org/whl/cpu -r dev-requirements.txt

# Stage 3: Tester
# This stage runs the tests. It is bypassed if SKIP_TESTS is true.
FROM builder AS tester
ARG SKIP_TESTS=false
ENV PYTHONPATH=/app:/app/src
COPY src ./src
COPY tests ./tests
RUN uv run ruff check .
RUN if [ "$SKIP_TESTS" != "true" ]; then pytest; else echo "Skipping tests..."; fi

# Stage 4: Prod Builder
# This stage prepares the production dependencies only.
FROM base AS prod-builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --format requirements-txt --index https://download.pytorch.org/whl/cpu -o requirements.txt
RUN uv pip install --system --no-cache --index-url https://pypi.org/simple --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Stage 5: Runtime
FROM base AS runtime

ARG COMMIT
ARG VERSION

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  APP_VERSION=$VERSION \
  APP_COMMIT=$COMMIT \
  DEBUG=false \
  HOST=0.0.0.0 \
  PORT=8000 \
  PYTHONPATH=/app:/app/src

LABEL org.opencontainers.image.source=https://github.com/FitForwardOrg/agentic-server

# Copy installed packages from prod-builder
COPY --from=prod-builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=prod-builder /usr/local/bin /usr/local/bin

# Copy application code from tests stage to ensure tests passed
# Using /app/src to be explicit
COPY --from=tester /app/src ./src

# Create a non-root user
RUN useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app

# Ensure appuser can write to rapidocr models directory
# and other potential model cache directories
RUN mkdir -p /usr/local/lib/python3.14/site-packages/rapidocr/models && \
    chown -R appuser:appuser /usr/local/lib/python3.14/site-packages/rapidocr/models && \
    mkdir -p /home/appuser/.cache && \
    chown -R appuser:appuser /home/appuser/.cache

USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --spider -q http://localhost:8000/isReady || exit 1

EXPOSE 8000

CMD ["python", "src/main.py", "serve"]
