import sys
from contextlib import asynccontextmanager
from http import HTTPStatus
from os import environ

from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import MetaData

from app.api import router
from app.container import AppContainer
from app.core.config import get_config
from app.core.exceptions import CustomException
from app.core.fastapi.custom_josn_response import CustomORJSONResponse
from app.core.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
)
from app.domain.log.services import BaseLogHandler
from app.domain.page.views import page_router

config = get_config()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print(config)
    yield


@inject
def init_listeners(
    app_: FastAPI,
    log_handler: BaseLogHandler = Provide["log_container.log_handler"],
) -> None:
    @app_.exception_handler(Exception)
    async def root_exception_handler(request: Request, exc: CustomException):
        """
        Unmanaged exception will be caught here.
        """
        try:
            log_data = {
                "user_id": request.user.user_id,
                "ip": request.client.host if request.client else None,
                "port": request.client.port if request.client else None,
                "method": request.method,
                "path": request.url.path,
                "agent": dict(request.headers.items())["user-agent"],
                "response_status": HTTPStatus.INTERNAL_SERVER_ERROR,
            }
            await log_handler(log_data)
            print(log_data)
            return CustomORJSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"code": 500, "message": exc},
            )
        except Exception as e:
            raise e

    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        print(request.headers.get("accept", ""))
        if exc.http_code == 401:
            # 요청의 Accept 헤더를 확인
            if "text/html" in request.headers.get("accept", ""):
                return RedirectResponse(url="/login")

        return CustomORJSONResponse(
            status_code=exc.http_code,
            content={"code": exc.error_code, "message": exc.message},
        )


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


def create_app() -> FastAPI:
    container = AppContainer()
    _app = FastAPI(
        title="FastApi-chat",
        description="FastApi-chat API",
        version="1.0.0",
        docs_url=(None if environ.get("API_ENV") == "production" else "/docs"),
        redoc_url=(None if environ.get("API_ENV") == "production" else "/redoc"),
        lifespan=lifespan,
        # dependencies = [Depends(Logging)],
    )
    _app.container = container
    _app.include_router(page_router)
    _app.include_router(router, prefix="/api/v1")

    init_middleware(_app)
    init_listeners(_app)

    return _app


app = create_app()


@app.get("/", include_in_schema=False)
async def root():
    # 루트 경로로 들어오면 /login으로 리다이렉트
    return RedirectResponse(url="/login")


@app.get("/ping", include_in_schema=False)
def ping():
    raise Exception
    return {"ping": "pong"}
