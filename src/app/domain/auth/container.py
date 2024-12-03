from dependency_injector import containers, providers

from .services import TokenService


class AuthContainer(containers.DeclarativeContainer):
    token_service = providers.Factory(TokenService)
