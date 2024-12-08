from app.core.db.create_session import standalone_session
from app.core.db.schema.log import RequestResponseLog


class BaseLogHandler:
    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class DatabaseLoghandler(BaseLogHandler):

    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    @standalone_session
    async def __call__(self, data: dict):
        request_response_log = RequestResponseLog(**data)
        self.repository.save(request_response_log)
