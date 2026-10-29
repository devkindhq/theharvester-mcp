FROM python:3.12-slim

LABEL org.opencontainers.image.title="theharvester-mcp"
LABEL org.opencontainers.image.description="theHarvester MCP Server - OSINT email, subdomain and contact harvesting for AI agents"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/devkindhq/theharvester-mcp"

RUN addgroup --gid 1000 mcpuser && \
    adduser --disabled-password --uid 1000 --ingroup mcpuser mcpuser

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Install uv (official multi-arch image; theHarvester needs a recent uv for
# managed-Python discovery and relative exclude-newer dates)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Install theHarvester (requires Python >=3.14; uv fetches a managed interpreter)
RUN git clone --depth 1 https://github.com/laramies/theHarvester.git /opt/theharvester && \
    cd /opt/theharvester && \
    uv sync --no-dev
RUN apt-get purge -y --auto-remove git curl && rm -rf /var/lib/apt/lists/*

# MCP layer runs on system Python; theHarvester runs via its own venv
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=mcpuser:mcpuser server.py ./
RUN mkdir -p /app/output && chown -R mcpuser:mcpuser /app

USER mcpuser

ENV THEHARVESTER_OUTPUT_DIR=/app/output
ENV THEHARVESTER_TIMEOUT=120
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD pgrep -f "python.*server.py" > /dev/null || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/python3", "server.py"]
