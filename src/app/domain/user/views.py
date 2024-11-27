from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container import AppContainer

from .models import CreateUserReq, CreateUserRes, LoginReq, LoginRes
from .service import UserService

user_router = APIRouter()


@user_router.post("", response_model=CreateUserRes, summary="회원가입")
@inject
async def create_user(
    request: CreateUserReq,
    user_service: UserService = Depends(Provide["user_container.user_service"]),
):
    return await user_service.create_user(**request.model_dump())


@user_router.post("/login", response_model=LoginRes, summary="로그인")
@inject
async def login(
    request: LoginReq,
    user_service: UserService = Depends(Provide["user_container.user_service"]),
):
    return await user_service.login(**request.model_dump())


@user_router.put("/{user_id}/password")
async def update_password():
    pass
