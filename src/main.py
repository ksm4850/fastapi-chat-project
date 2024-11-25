from contextlib import asynccontextmanager
from os import environ

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import router
from core.config import config
from core.exceptions import CustomException
from core.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
)

# @asynccontextmanager
# async def lifespan(_app: FastAPI):
#     mongodb: MongoDB = container.mongo()
#     await mongodb.connect()
#     yield
#     await mongodb.close()


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_middleware(_app: FastAPI) -> None:

    _app.add_middleware(SQLAlchemyMiddleware)
    _app.add_middleware(
        AuthenticationMiddleware,
        backend=AuthBackend(),
        on_error=on_auth_error,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE"),
        allow_headers=["*"],
    )


def create_app(_config) -> FastAPI:
    _app = FastAPI(
        title="FastApi-chat",
        description="FastApi-chat API",
        version="1.0.0",
        docs_url=(None if environ.get("API_ENV") == "production" else "/docs"),
        redoc_url=(
            None if environ.get("API_ENV") == "production" else "/redoc"
        ),
        # dependencies = [Depends(Logging)],
    )
    init_middleware(_app)

    _app.include_router(router)

    return _app


app = create_app(config)


@app.get("/ping")
def ping():
    return {"ping": "pong"}
