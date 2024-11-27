from sqlalchemy import BigInteger, Unicode
from sqlalchemy.orm import mapped_column

from app.core.db.mixins import TimestampMixin

from .base import Base


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email = mapped_column(Unicode(255), nullable=False, unique=True)
    password = mapped_column(Unicode(255), nullable=False)
    nickname = mapped_column(Unicode(255), nullable=False, unique=True)
