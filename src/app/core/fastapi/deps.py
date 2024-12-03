from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request, WebSocket
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)

from app.core.exceptions import AuthException
from app.core.utils.token_helper import TokenHelper
from app.domain.user.models import UserBase
from app.domain.user.services import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/login",
)

user_service: UserService = Provide["user_container.user_service"]

# def get_current_user(
#     Authorization: HTTPAuthorizationCredentials | None = Depends(
#         HTTPBearer(auto_error=False)
#     ),
# ) -> int:
#     if Authorization is None:
#         raise AuthException
#     user: dict = TokenHelper.decode(token=Authorization.credentials)
#     return user.get("user_id")


def user_token_verify(credentials: str) -> dict:
    if credentials is None:
        raise AuthException
    token: dict = TokenHelper.decode(token=credentials)
    return token


async def get_current_user(
    request: Request,
    token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
) -> UserBase:

    access_token = token if token else request.cookies.get("accessToken")
    print(access_token)
    payload: dict = user_token_verify(access_token)
    user_id = payload.get("user_id", None)
    user = await user_service.get_user(user_id)
    if not user:
        raise AuthException
    return user


async def get_current_user_ws(websocket: WebSocket) -> UserBase:
    authorization = websocket.headers.get("authorization")
    payload: dict = user_token_verify(authorization)
    user_id = payload.get("user_id", None)
    user = await user_service.get_user(user_id)
    if not user:
        raise AuthException
    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]
CurrentUserWs = Annotated[dict, Depends(get_current_user_ws)]
