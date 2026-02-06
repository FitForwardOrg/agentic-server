# Stage 1: Base
FROM python:3.14.3-alpine AS base

WORKDIR /app

# Stage 2: Builder
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install all dependencies (including dev)
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --dev --format requirements-txt -o dev-requirements.txt
RUN uv pip install --system --no-cache -r dev-requirements.txt

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
RUN uv export --frozen --format requirements-txt -o requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

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

# Copy installed packages from prod-builder
COPY --from=prod-builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=prod-builder /usr/local/bin /usr/local/bin

# Copy application code from tests stage to ensure tests passed
# Using /app/src to be explicit
COPY --from=tester /app/src ./src

# Create a non-root user
RUN adduser -D -u 1000 appuser && chown -R appuser /app
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --spider -q http://localhost:8000/isReady || exit 1

EXPOSE 8000

CMD ["python", "src/main.py", "serve"]
