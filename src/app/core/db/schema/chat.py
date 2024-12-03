from sqlalchemy import BigInteger, String, Unicode, inspect
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.mixins import TimestampMixin

from .base import Base


class Chat(Base, TimestampMixin):
    __tablename__ = "chat"
    # 채팅방
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)


class Message(Base, TimestampMixin):
    __tablename__ = "message"
    # 메세지
    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    text = mapped_column(Unicode(255), nullable=False)
    chat_id = mapped_column(BigInteger, nullable=False, comment="채팅방 id")
    user_id = mapped_column(BigInteger, nullable=False, comment="유저 id")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class UserChat(Base, TimestampMixin):
    __tablename__ = "user_chat"
    # 채팅방 참여 유저
    chat_id = mapped_column(BigInteger, primary_key=True)
    user_id = mapped_column(BigInteger, primary_key=True)
