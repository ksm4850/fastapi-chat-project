import asyncio

from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import async_scoped_session

from app.celery_task import celery_app
from app.core.db.create_session import create_session_context
from app.core.db.schema.chat import Message


@celery_app.task(name="save_message")
def save_message(data: dict):
    result = asyncio.run(_save_message(data))
    return result


async def _save_message(data: dict):
    async with create_session_context() as session:
        try:
            message = Message(**data)
            session.add(message)
            await session.commit()
            return {"status": "success", "data": data}
        except Exception as e:
            await session.rollback()
            return {"status": "failure", "error": str(e)}
