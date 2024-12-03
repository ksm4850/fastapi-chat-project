from typing import List, Optional

from dependency_injector.wiring import Provide
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import async_scoped_session

from app.core.db.schema.user import User
from app.core.db.session import session


class UserRepository:

    async def get_user(self, user_id: int) -> Optional[User]:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_user_by_email_or_nickname(
        self, email: str, nickname: str
    ) -> Optional[User]:
        query = select(User).where(or_(User.email == email, User.nickname == nickname))
        result = await session.execute(query)
        return result.scalars().first()

    async def save_user(self, email: str, hashed_password, nickname: str) -> User:
        user = User(email=email, password=hashed_password, nickname=nickname)
        session.add(user)
        await session.flush()
        return user
