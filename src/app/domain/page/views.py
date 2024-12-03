from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from app.core.config import get_config
from app.core.fastapi.deps import get_current_user
from app.domain.user.models import UserBase
from app.domain.user.services import UserService

page_router = APIRouter(
    # include_in_schema=False,
)
config = get_config()
templates = Jinja2Templates(directory=config.TEMPLATE_DIR)


@page_router.get(
    "/login",
    summary="로그인 페이지",
    response_class=HTMLResponse,
)
async def login_page(
    request: Request,
):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@page_router.get(
    "/join",
    summary="회원가입 페이지",
    response_class=HTMLResponse,
)
async def join_page(
    request: Request,
):
    return templates.TemplateResponse(name="join.html", context={"request": request})


@page_router.get(
    "/main",
    summary="채팅메인 페이지",
    response_class=HTMLResponse,
)
async def main_page(
    request: Request,
    user: Annotated[UserBase, Depends(get_current_user)],
):
    return templates.TemplateResponse(
        name="chat_main.html", context={"request": request, "user": user.model_dump()}
    )
