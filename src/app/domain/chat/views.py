from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import async_scoped_session

from app.celery_task.tasks.chat import save_message
from app.core.config import get_config
from app.core.db.schema.chat import Message
from app.core.fastapi.deps import CurrentUser, CurrentUserWs
from app.domain.user.models import UserBase
from app.domain.user.services import UserService

from .models import ChatListRes, CreateChatReq
from .services import ChatService
from .util import ConnectionManager

chat_router = APIRouter()
manager = ConnectionManager()
config = get_config()


@chat_router.post("", summary="채팅방 생성", response_model=None)
@inject
async def create_chat(
    request: CreateChatReq,
    user: CurrentUser,
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"]),
):
    await chat_service.add_chat(user_id=user.id, title=request.title)
    return HTMLResponse(status_code=200)


@chat_router.post("/{chat_id}", summary="채팅방 나가기")
@inject
async def exit_chat(
    user: CurrentUser,
    chat_id: int,
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"]),
):
    await chat_service.exit_chat(chat_id=chat_id, user_id=user.id)
    return HTMLResponse(status_code=200)


@chat_router.get("/list", summary="채팅방 목록", response_model=ChatListRes)
@inject
async def chat_list(
    user: CurrentUser,
    list_type: Annotated[str, Query(description="전체-all, 내채팅-my")] = "all",
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"]),
):
    """
    채팅방 목록
    """
    result = await chat_service.chat_list(user_id=user.id, list_type=list_type)
    return ChatListRes(chat_list=result)


@chat_router.websocket("/ws/{chat_id}/{user_id}")
@inject
async def chat(
    websocket: WebSocket,
    chat_id: int = Path(..., description="채팅id"),
    user_id: int = Path(..., description="유저id"),
    user_service: UserService = Depends(Provide["user_container.user_service"]),
    chat_service: ChatService = Depends(Provide["chat_container.chat_service"]),
):
    # 웹소켓 연결
    await manager.connect(chat_id, websocket)

    # 유저정보 확인
    user = await user_service.get_user(user_id)
    user_id = user.id
    user_nickname = user.nickname

    # 채팅방 참여
    await chat_service.join_chat_room(user_id, chat_id)

    try:
        while True:
            data = await websocket.receive_text()

            message = {
                "chat_id": chat_id,
                "user_id": user_id,
                "text": data,
            }
            await chat_service.save_message(**message)
            await manager.broadcast(
                chat_id,
                dict(user_id=user_id, nickname=user_nickname, message=data),
            )
    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
        # await manager.broadcast(
        #     chat_id,
        #     dict(
        #         user_id=0,
        #         nickname="admin",
        #         message=f"{user_nickname}님이 나갔습니다.",
        #     ),
        # )
