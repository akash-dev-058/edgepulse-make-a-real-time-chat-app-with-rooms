import asyncio
import os
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.main import app
from app.models.base import Base

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")

engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True, poolclass=NullPool)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture()
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture()
async def client(db_session):
    async def get_test_db():
        yield db_session
    app.dependency_overrides["app.dependencies.get_db"] = get_test_db
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()
