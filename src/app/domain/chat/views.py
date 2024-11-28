from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect

from app.container import AppContainer

chat_router = APIRouter()


@chat_router.websocket("/ws/")
@inject
async def chat(
    websocket: WebSocket,
):
    pass
