# The contained machine. It deliberately has curl, git and python: containment must
# hold when the agent has real tools, not because the tools are missing.
FROM node:24-bookworm-slim@sha256:c86ecead9e55a5210ac1727de38a4ca840bf03dcaf34dc9749addbf383b1920c
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 curl git ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code@2.1.306 \
 && npm cache clean --force \
 && useradd --uid 10001 --create-home --home-dir /home/agent agent
COPY bsa /opt/bsa/bsa
COPY catalog /opt/bsa/catalog
COPY arena/containment /opt/bsa/containment
COPY arena/agent/managed-settings.json /etc/claude-code/managed-settings.json
COPY arena/agent/deny_hook.py /opt/bsa/deny_hook.py
ENV PYTHONPATH=/opt/bsa PYTHONDONTWRITEBYTECODE=1 DISABLE_UPDATES=1 \
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 DISABLE_TELEMETRY=1 DISABLE_ERROR_REPORTING=1
USER 10001:10001
WORKDIR /workspace
