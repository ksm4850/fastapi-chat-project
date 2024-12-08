from dependency_injector import containers, providers

from .repository import RequestResponseLogAlchemyRepository
from .services import DatabaseLoghandler


class LogContainer(containers.DeclarativeContainer):
    db_log_repository = providers.Factory(RequestResponseLogAlchemyRepository)

    log_handler = providers.Factory(DatabaseLoghandler, repository=db_log_repository)
