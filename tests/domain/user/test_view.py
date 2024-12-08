import pytest
import pytest_asyncio
from sqlalchemy import select


@pytest.mark.asyncio
async def test_db_connect(session):
    result = await session.execute(select(1))

    assert result.scalar()
