from pydantic import BaseModel, Field
from sqlalchemy import BigInteger, Boolean, Column, Enum, String, Text, Unicode

from core.db.mixins import TimestampMixin
from core.db.session import Base


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=True)


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")


class LoginRequest(BaseModel):
    email: str = Field(..., description="이메일")
    password: str = Field(..., description="비밀번호")


class CreateUserReq(BaseModel):
    email: str = Field(..., description="이메일")
    password1: str = Field(..., description="비밀번호")
    password2: str = Field(..., description="비밀번호 확인")
    nickname: str = Field(..., description="닉네임")


class UpdatePasswordReq(BaseModel):
    password1: str = Field(..., description="비밀번호")
    password2: str = Field(..., description="비밀번호 확인")
