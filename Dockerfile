# ── Build stage: install dependencies with uv ─────────────────────────────────
FROM python:3.14-slim AS builder

# Copy uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Install dependencies (leverages layer cache when lock file is unchanged)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy the virtual env from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY main.py ./
COPY app/ ./app/

# Make the venv the active Python environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8501

# Streamlit must bind to 0.0.0.0 to be reachable outside the container
CMD ["streamlit", "run", "main.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
