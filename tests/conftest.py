import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from project.app.infrastructure.database import Base, Session
from project.app.main import app

metadata = Base.metadata

# DATABASE
DATABASE_URL_TEST = os.environ.get("DATABASE_URL")

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac
