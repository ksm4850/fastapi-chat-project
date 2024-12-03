import bcrypt
from dependency_injector.wiring import Provide, inject

from app.core.db.transactional import Transactional
from app.domain.auth.services import TokenService
from app.domain.user.models import UserBase

from .repositorys import ChatRepository, MessageRepository, UserChatRepository


class ChatService:
    def __init__(
        self,
        chat_repository: ChatRepository,
        user_chat_repository: UserChatRepository,
        message_repository: MessageRepository,
    ):
        self.chat_repository = chat_repository
        self.user_chat_repository = user_chat_repository
        self.message_repository = message_repository

    async def chat_list(self, user_id: int, list_type: str):
        # 채팅방 리스트
        chat_list = []
        if list_type == "all":
            chat_list = await self.chat_repository.get_chat_list()
        elif list_type == "my":
            chat_list = await self.chat_repository.get_user_chat_list(user_id)
        return chat_list

    @Transactional()
    async def join_chat_room(self, user_id: int, chat_id: int):
        # 참여중인지 확인
        result = await self.user_chat_repository.get_user_by_chat(
            user_id=user_id, chat_id=chat_id
        )
        if result is None:
            # 참여중인방이 아니라면 방 참여
            await self.user_chat_repository.add(user_id=user_id, chat_id=chat_id)

    @Transactional()
    async def add_chat(self, user_id: int, title: str):
        # 채팅방 생성
        chat_id = await self.chat_repository.create_chat(title=title)

        # 참가
        await self.user_chat_repository.add(user_id=user_id, chat_id=chat_id)

    @Transactional()
    async def exit_chat(self, chat_id: int, user_id: int):
        # 채팅방 나가기
        await self.user_chat_repository.delete(chat_id=chat_id, user_id=user_id)

        # 채팅방 남은 인원 체크
        cnt = await self.user_chat_repository.get_count(chat_id=chat_id)
        if cnt == 0:
            # 채팅방 남은 인원 없으면 채팅방 삭제
            await self.chat_repository.delelte(chat_id=chat_id)

    @Transactional()
    async def save_message(self, chat_id, user_id, text):
        await self.message_repository.add(chat_id=chat_id, user_id=user_id, text=text)
