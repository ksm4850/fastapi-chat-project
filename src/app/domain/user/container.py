from dependency_injector import containers, providers

from app.core.db import session
from app.domain.user.repositorys import UserRepository
from app.domain.user.services import UserService


class UserContainer(containers.DeclarativeContainer):
    # Repository
    user_repository = providers.Factory(UserRepository)
    # Service
    user_service = providers.Factory(UserService, repository=user_repository)
