from http.client import responses
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.container import AppContainer
from app.core.config import get_config

from ..auth.views import refresh_token
from .models import CreateUserReq, CreateUserRes, LoginRes
from .services import UserService

user_router = APIRouter()
config = get_config()


@user_router.post("", summary="회원가입", response_model=CreateUserRes)
@inject
async def create_user(
    request: CreateUserReq,
    user_service: UserService = Depends(Provide["user_container.user_service"]),
):
    await user_service.create_user(**request.model_dump())
    return HTMLResponse(status_code=200)


@user_router.post("/login", summary="로그인", response_model=LoginRes)
@inject
async def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(Provide["user_container.user_service"]),
):
    token_data = await user_service.login(request.username, request.password)
    response = JSONResponse(content=token_data)
    response.set_cookie("accessToken", token_data.get("access_token"))
    response.set_cookie("refreshToken", token_data.get("refresh_token"))
    return response


@user_router.put("/{user_id}/password", summary="비밀번호 변경")
async def update_password():
    pass
