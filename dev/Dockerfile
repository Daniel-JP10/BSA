# Development environment. The repository lives in a Docker volume, not in a host folder.
FROM node:24-bookworm-slim@sha256:c86ecead9e55a5210ac1727de38a4ca840bf03dcaf34dc9749addbf383b1920c
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 git ca-certificates curl \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g @anthropic-ai/claude-code@2.1.306 \
 && npm cache clean --force \
 && useradd --uid 10001 --create-home --home-dir /home/dev dev \
 && mkdir /workspace && chown dev:dev /workspace
ENV PYTHONDONTWRITEBYTECODE=1 DISABLE_TELEMETRY=1
USER 10001:10001
WORKDIR /workspace
