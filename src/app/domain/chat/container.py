from dependency_injector import containers, providers

from app.core.db import session
from app.domain.chat.repositorys import (
    ChatRepository,
    MessageRepository,
    UserChatRepository,
)
from app.domain.chat.services import ChatService


class ChatContainer(containers.DeclarativeContainer):
    # Repository
    chat_repository = providers.Factory(ChatRepository)
    user_chat_repository = providers.Factory(UserChatRepository)
    message_repository = providers.Factory(MessageRepository)
    # Service
    chat_service = providers.Factory(
        ChatService,
        chat_repository=chat_repository,
        user_chat_repository=user_chat_repository,
        message_repository=message_repository,
    )
