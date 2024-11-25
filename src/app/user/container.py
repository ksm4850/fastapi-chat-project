from dependency_injector import containers, providers

from app.user.repository import UserRepository
from app.user.service import UserService


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()

    # Service
    user_service = providers.Singleton(UserService)

    # Repository
    user_repository = providers.Singleton(
        UserRepository, session_factory=db.provided.session
    )
