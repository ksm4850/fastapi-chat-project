import bcrypt
from dependency_injector.wiring import Provide, inject

from app.core.db.transactional import Transactional
from app.domain.auth.services import TokenService

from .exceptions import (
    DuplicateEmailOrNicknameException,
    NoEmailOrWrongPassword,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from .models import LoginRes, UserBase
from .repositorys import UserRepository


def hash_password(password: str) -> str:
    byte_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(byte_password, salt)
    return hashed_password.decode("utf-8")


def check_password(hashed_password: str, user_password: str) -> bool:
    byte_password = user_password.encode("utf-8")
    return bcrypt.checkpw(byte_password, hashed_password.encode("utf-8"))


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user(self, user_id) -> UserBase:
        user = await self.repository.get_user(user_id)

        return UserBase.model_validate(user)

    @Transactional()
    async def create_user(self, email, password1, password2, nickname):
        if password1 != password2:
            raise PasswordDoesNotMatchException
        hashed_password = hash_password(password1)

        exist_user = await self.repository.get_user_by_email_or_nickname(
            email=email, nickname=nickname
        )
        if exist_user:
            raise DuplicateEmailOrNicknameException

        user = await self.repository.save_user(
            email=email, hashed_password=hashed_password, nickname=nickname
        )
        return user

    @inject
    async def login(
        self,
        email,
        password,
        token_service: TokenService = Provide["auth_container.token_service"],
    ) -> dict:
        user = await self.repository.get_user_by_email(email)
        if not user:
            raise UserNotFoundException
        if not check_password(user.password, password):
            raise NoEmailOrWrongPassword

        access_token, refresh_token = await token_service.issue_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}
