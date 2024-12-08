import asyncio
import os
import sqlite3

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.core.db.schema import Base
from app.main import app

os.environ["API_ENV"] = "test"

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
SessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, autocommit=False, autoflush=False
)


@pytest_asyncio.fixture(scope="session")
async def session():
    # 비동기 엔진에서 데이터베이스 테이블 생성
    async with test_engine.begin() as conn:
        # sync 메서드를 사용하여 동기적 DB 작업 처리
        await conn.run_sync(Base.metadata.create_all)

    # 세션 객체 생성
    db = SessionLocal()

    try:
        yield db  # 테스트에서 db 세션을 사용할 수 있도록 제공
    finally:

        await db.close()
        # Base.metadata.drop_all(bind=test_engin)


@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(scope="session")
async def test_async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
