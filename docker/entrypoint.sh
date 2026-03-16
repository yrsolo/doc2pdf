#!/usr/bin/env bash
set -euo pipefail

APP_PORT="${PORT:-8080}"
GOTENBERG_URL="${GOTENBERG_BASE_URL:-http://127.0.0.1:3000}"
GOTENBERG_HEALTH_URL="${GOTENBERG_URL%/}/health"
STARTUP_TIMEOUT_SEC="${GOTENBERG_STARTUP_TIMEOUT_SEC:-60}"

cleanup() {
  if [[ -n "${UVICORN_PID:-}" ]] && kill -0 "${UVICORN_PID}" 2>/dev/null; then
    kill "${UVICORN_PID}" 2>/dev/null || true
  fi
  if [[ -n "${GOTENBERG_PID:-}" ]] && kill -0 "${GOTENBERG_PID}" 2>/dev/null; then
    kill "${GOTENBERG_PID}" 2>/dev/null || true
  fi
  wait || true
}

trap cleanup EXIT INT TERM

gotenberg &
GOTENBERG_PID=$!

started_at=$(date +%s)
while true; do
  if curl -fsS "${GOTENBERG_HEALTH_URL}" >/dev/null 2>&1; then
    break
  fi

  if ! kill -0 "${GOTENBERG_PID}" 2>/dev/null; then
    echo "Gotenberg exited before becoming ready" >&2
    exit 1
  fi

  now=$(date +%s)
  if (( now - started_at >= STARTUP_TIMEOUT_SEC )); then
    echo "Timed out waiting for Gotenberg at ${GOTENBERG_HEALTH_URL}" >&2
    exit 1
  fi
  sleep 1
done

python3 -m uvicorn src.main:app --host 0.0.0.0 --port "${APP_PORT}" &
UVICORN_PID=$!

wait -n "${GOTENBERG_PID}" "${UVICORN_PID}"
exit_code=$?

if kill -0 "${GOTENBERG_PID}" 2>/dev/null && kill -0 "${UVICORN_PID}" 2>/dev/null; then
  exit "${exit_code}"
fi

echo "One of the runtime processes exited unexpectedly" >&2
exit "${exit_code}"
