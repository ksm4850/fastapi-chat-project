from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.fastapi.pydantic_models import BodyBaseModel, ResponseBaseModel


class RefreshTokenRequest(BodyBaseModel):
    refresh_token: str = Field(..., description="Refresh token")


class RefreshTokenResponse(ResponseBaseModel):
    token: str = Field(...)
    refresh_token: str


class AccessTokenResponse(ResponseBaseModel):
    access_token: str = Field(...)
