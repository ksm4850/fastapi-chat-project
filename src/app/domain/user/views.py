from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.container import AppContainer

from .models import CreateUserReq, CreateUserRes, LoginReq, LoginRes
from .service import UserService

user_router = APIRouter()


@user_router.post("", summary="회원가입", response_model=CreateUserRes)
@inject
async def create_user(
    request: CreateUserReq,
    user_service: UserService = Depends(Provide["user_container.user_service"]),
):
    return await user_service.create_user(**request.model_dump())


@user_router.post("/login", summary="로그인", response_model=LoginRes)
@inject
async def login(
    request: LoginReq,
    user_service: UserService = Depends(Provide["user_container.user_service"]),
):
    return await user_service.login(**request.model_dump())


@user_router.put("/{user_id}/password", summary="비밀번호 변경")
async def update_password():
    pass


@user_router.get("/friend", summary="친구검색")
async def friend_search():
    pass


@user_router.get("/friend-list", summary="친구목록")
async def friend_list():
    pass


@user_router.post("/friend", summary="친구추가")
async def friend_add():
    pass
