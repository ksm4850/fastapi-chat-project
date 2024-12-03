from datetime import datetime

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import async_scoped_session

from app.core.exceptions.token import (
    TokenDecodeException,
    TokenExpireException,
)
from app.core.utils.token_helper import TokenHelper
from app.domain.user.repositorys import UserRepository

session: async_scoped_session = Provide["session"]


class TokenService:
    # def __init__(self, repository: TokenRepository):
    #     self.repository = repository

    @inject
    async def issue_token(
        self,
        user_id: int,
        access_token_exp_minute: int = Provide["config.JWT_TOKEN_EXPIRE_MINUTES"],
        refresh_token_exp_minute: int = Provide[
            "config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES"
        ],
    ) -> tuple:
        access_token = TokenHelper.encode(
            payload={"user_id": user_id}, expire_period_minute=access_token_exp_minute
        )
        refresh_token = TokenHelper.encode(
            payload={"user_id": user_id, "sub": "refresh"},
            expire_period_minute=refresh_token_exp_minute,
        )
        return access_token, refresh_token

    @inject
    async def refresh_access_token(
        self,
        refresh_token: str,
        refresh_expire_minute: int = Provide["config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES"],
        user_repository: UserRepository = Provide["user_container.user_repository"],
    ):
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)

        if decoded_refresh_token.get("sub") != "refresh":
            raise TokenDecodeException
        user_id = decoded_refresh_token.get("user_id")

        user = await user_repository.get_user(user_id)

        if user_id is not None:
            new_access_token = TokenHelper.encode(
                payload={"user_id": user.id},
                expire_period_minute=refresh_expire_minute,
            )
            return new_access_token
        raise TokenExpireException

    async def revoke_refresh_token(self, user_id: int) -> None:
        await self.repository.make_all_token_invalid(user_id)
