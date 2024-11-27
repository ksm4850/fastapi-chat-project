from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LoginRes(BaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")


class LoginReq(BaseModel):
    email: str = Field(..., description="이메일")
    password: str = Field(..., description="비밀번호")


class CreateUserReq(BaseModel):
    email: str = Field(..., description="이메일")
    password1: str = Field(..., description="비밀번호")
    password2: str = Field(..., description="비밀번호 확인")
    nickname: str = Field(..., description="닉네임")


class CreateUserRes(BaseModel):
    email: str = Field(..., description="이메일")
    nickname: str = Field(..., description="닉네임")
    created_at: datetime = Field(..., description="생성일")
    updated_at: datetime = Field(..., description="수정일")

    model_config = ConfigDict(from_attributes=True)


class UpdatePasswordReq(BaseModel):
    password1: str = Field(..., description="비밀번호")
    password2: str = Field(..., description="비밀번호 확인")
