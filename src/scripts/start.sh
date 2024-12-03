#! /bin/bash
set -e

DEFAULT_MODULE_NAME=app.main
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

if [ -f /fastapi-chat-project/src/gunicorn/gunicorn.config.py ]; then
    DEFAULT_GUNICORN_CONF=/fastapi-chat-project/src/gunicorn/gunicorn.config.py
elif [ -f /fastapi-chat-project/gunicorn/gunicorn.config.py ]; then
    DEFAULT_GUNICORN_CONF=/fastapi-chat-project/gunicorn/gunicorn.config.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn.config.py
fi

export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

dockerize -wait tcp://postgres:5432 -timeout 10s


alembic upgrade head

gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"