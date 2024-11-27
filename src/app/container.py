from dependency_injector import containers, providers
from dependency_injector.providers import Provider
from fastapi.middleware import Middleware
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.core.config import get_config
from app.core.db.session import get_session_context
from app.core.middlewares.sqlalchemy import SQLAlchemyMiddleware
from app.domain.auth.container import AuthContainer
from app.domain.user.container import UserContainer


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["app"],
    )
    _config = get_config()
    config = providers.Configuration()
    config.from_dict(_config.dict())

    engine = providers.Singleton(
        create_async_engine, config.SQLALCHEMY_DATABASE_URI, pool_recycle=3600
    )

    session_factory = providers.Singleton(
        sessionmaker,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    session = providers.Singleton(
        async_scoped_session,
        session_factory=session_factory,
        scopefunc=get_session_context,
    )

    user_container = providers.Container(UserContainer)
    auth_container = providers.Container(AuthContainer)
