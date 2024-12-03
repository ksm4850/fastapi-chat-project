from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.fastapi.pydantic_models import BodyBaseModel, ResponseBaseModel


class UserBase(BaseModel):
    id: int = Field(..., description="id")
    email: str = Field(..., description="이메일")
    nickname: str = Field(..., description="닉네임")
    model_config = ConfigDict(from_attributes=True)


class LoginRes(ResponseBaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")


class CreateUserReq(BodyBaseModel):
    email: str = Field(..., description="이메일")
    password1: str = Field(..., description="비밀번호")
    password2: str = Field(..., description="비밀번호 확인")
    nickname: str = Field(..., description="닉네임")


class CreateUserRes(ResponseBaseModel):
    email: str = Field(..., description="이메일")
    nickname: str = Field(..., description="닉네임")
    created_at: datetime = Field(..., description="생성일")
    updated_at: datetime = Field(..., description="수정일")

    model_config = ConfigDict(from_attributes=True)


class UpdatePasswordReq(BodyBaseModel):
    password1: str = Field(..., description="비밀번호")
    password2: str = Field(..., description="비밀번호 확인")
