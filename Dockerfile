# ==============================================================================
# File: Dockerfile
# Project: AxisOS Alexa+ Outpost (Crusan & Co.)
# Author: Marc F. Crusan / Crusan & Co. w/ AGY
# Date: 2026-10-20
# Description: Container build for AxisOS Alexa+ Streamable HTTP MCP Outpost.
# Changelog:
#   - 2026-10-20 (MFC/AGY): Initial creation.
# ==============================================================================

FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY infra/ ./infra/
COPY scripts/ ./scripts/
COPY tests/ ./tests/

ENV PYTHONPATH=/app/src
EXPOSE 8092

CMD ["uvicorn", "axisos_alexa_mcp.main:app", "--host", "0.0.0.0", "--port", "8092"]
