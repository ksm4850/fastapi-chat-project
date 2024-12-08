from abc import ABC, abstractmethod

from app.core.db.schema.log import RequestResponseLog
from app.core.db.session import session


class BaseLogRepository(ABC):
    @abstractmethod
    def save(self):
        pass


class RequestResponseLogAlchemyRepository(BaseLogRepository):
    def save(self, data: RequestResponseLog):
        session.add(data)
