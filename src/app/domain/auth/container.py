from dependency_injector import containers, providers

from .service import TokenService


class AuthContainer(containers.DeclarativeContainer):
    token_service = providers.Factory(TokenService)
