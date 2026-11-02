# Support services for the arena: sink, llm-proxy and fake-llm. Standard library only.
FROM python:3.12-alpine@sha256:e6dae589c1c05976188fd3bd019afd091445fc533ed2ea29001beddc7368a9c8
COPY arena/services/sink.py arena/services/llm_proxy.py arena/services/fake_llm.py /srv/
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 10001:10001
WORKDIR /srv
