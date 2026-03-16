FROM python:3.13-slim AS python-deps

WORKDIR /deps

COPY requirements.txt .
RUN pip install --no-cache-dir --target /python-deps -r requirements.txt


FROM gotenberg/gotenberg:8

USER root

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    GOTENBERG_BASE_URL=http://127.0.0.1:3000 \
    PYTHONPATH=/python-deps

WORKDIR /app

COPY --from=python-deps /python-deps /python-deps
COPY src ./src
COPY scripts ./scripts
COPY docker ./docker

RUN chmod +x /app/docker/entrypoint.sh \
    && chown -R gotenberg:gotenberg /app /python-deps

USER gotenberg

EXPOSE 8080

ENTRYPOINT ["/usr/bin/tini", "--", "/app/docker/entrypoint.sh"]
