from typing import List, Optional

from dependency_injector.wiring import Provide
from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.ext.asyncio import async_scoped_session

from app.core.db.schema.chat import Chat, Message, UserChat
from app.core.db.schema.user import User
from app.core.db.session import session


class ChatRepository:

    async def get_chat(self, chat_id: int):
        query = select(Chat).filter(Chat.id == chat_id)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_chat_list(self):
        query = select(Chat).order_by(Chat.id)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_chat_list(self, user_id: int):
        query = (
            select(Chat)
            .join(UserChat, Chat.id == UserChat.chat_id)
            .where(UserChat.user_id == user_id)
            .order_by(Chat.id)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def create_chat(self, title) -> int:
        # chat = Chat(title=title)
        # session.add(chat)
        # await session.flush()
        query = insert(Chat).values(title=title).returning(Chat.id)
        result = await session.execute(query)
        return result.scalar()

    async def save_message(self, chat_id, user_id, text):
        query = insert(Message).values(chat_id=chat_id, user_id=user_id, text=text)
        await session.execute(query)

    async def delelte(self, chat_id):
        query = delete(Chat).where(Chat.id == chat_id)
        await session.execute(query)


class UserChatRepository:
    async def add(self, user_id: int, chat_id: int):
        query = insert(UserChat).values(user_id=user_id, chat_id=chat_id)
        await session.execute(query)

    async def delete(self, chat_id: int, user_id: int):
        query = delete(UserChat).where(
            and_(UserChat.chat_id == chat_id, UserChat.user_id == user_id)
        )
        await session.execute(query)

    async def get_user_by_chat(self, chat_id: int, user_id: int) -> Optional[User]:
        query = select(UserChat).where(
            and_(UserChat.chat_id == chat_id, UserChat.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def get_count(self, chat_id):
        query = (
            select(func.count())
            .select_from(UserChat)
            .where(UserChat.chat_id == chat_id)
        )
        result = await session.execute(query)
        return result.scalars().first()


class MessageRepository:
    async def add(self, chat_id, user_id, text):
        query = insert(Message).values(chat_id=chat_id, user_id=user_id, text=text)
        await session.execute(query)
