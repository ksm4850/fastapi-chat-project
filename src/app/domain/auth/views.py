from pathlib import Path

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.config import get_config

from .models import AccessTokenResponse, RefreshTokenRequest
from .services import TokenService

auth_router = APIRouter()
config = get_config()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=config.TEMPLATE_DIR)


@auth_router.get(
    "/login",
    summary="로그인페이지",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def login_page(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@auth_router.get(
    "/join",
    summary="회원가입페이지",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def join_page(request: Request):
    return templates.TemplateResponse(name="join.html", context={"request": request})


@auth_router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    token_service: TokenService = Depends(Provide["auth_container.token_service"]),
):
    new_access_token = await token_service.refresh_access_token(
        refresh_token=request.refresh_token
    )
    return {"access_token": new_access_token}
