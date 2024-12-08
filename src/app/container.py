from dependency_injector import containers, providers
from dependency_injector.providers import Provider
from fastapi.middleware import Middleware
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.core.config import get_config
from app.core.db.session import (
    get_session_context,
    reset_session_context,
    set_session_context,
)
from app.domain.auth.container import AuthContainer
from app.domain.chat.container import ChatContainer
from app.domain.log.container import LogContainer
from app.domain.user.container import UserContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["app"],
    )
    _config = get_config()
    config = providers.Configuration()
    config.from_dict(_config.model_dump())

    user_container = providers.Container(UserContainer)
    auth_container = providers.Container(AuthContainer)
    chat_container = providers.Container(ChatContainer)
    log_container = providers.Container(LogContainer)
