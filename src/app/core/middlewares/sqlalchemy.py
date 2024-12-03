from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from starlette.types import ASGIApp, Receive, Scope, Send

# from app.core.db import session
from app.core.db.session import (
    reset_session_context,
    session,
    set_session_context,
)


class SQLAlchemyMiddleware:

    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)
