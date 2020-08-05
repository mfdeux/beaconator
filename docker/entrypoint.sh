#!/bin/bash

echo "Starting gunicorn"
exec /venv/bin/gunicorn core.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind "${BIND_HOST}":"${BIND_PORT}" \
  --workers 2 \
  --log-level=info
