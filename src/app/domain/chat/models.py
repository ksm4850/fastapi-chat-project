from dataclasses import dataclass
from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.core.fastapi.pydantic_models import BodyBaseModel, ResponseBaseModel


class Chat(BodyBaseModel):
    id: int = Field(..., description="id")
    title: str = Field(..., description="채팅방이름")

    model_config = ConfigDict(from_attributes=True)


class ChatListRes(ResponseBaseModel):
    chat_list: List[Chat]


class CreateChatReq(BodyBaseModel):
    title: str = Field(..., description="채팅방이름")
