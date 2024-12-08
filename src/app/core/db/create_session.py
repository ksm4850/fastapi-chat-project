from contextlib import asynccontextmanager
from uuid import uuid4

from dependency_injector.wiring import Provide
from sqlalchemy.ext.asyncio import async_scoped_session

from app.core.db.session import session

from .session import reset_session_context, set_session_context


def create_session(func):
    async def _create_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)

    return _create_session


def standalone_session(func):
    async def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            result = await func(*args, **kwargs)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)
        return result

    return _standalone_session


@asynccontextmanager
async def create_session_context():
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        yield session
    except Exception as e:
        await session.rollback()
    finally:
        await session.remove()
        reset_session_context(context=context)
