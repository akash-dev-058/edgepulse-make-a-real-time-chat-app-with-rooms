import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.db.session import get_db_session
from app.db.repository import UserRepository, RoomRepository, MessageRepository, ModerationRepository
from app.services.auth import get_auth_service
from app.services.room_service import get_room_service
from app.services.message_service import get_message_service
from app.services.moderation_service import get_moderation_service


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/chatapp_test"


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, pool_size=5, max_overflow=2)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session = sessionmaker(
        bind=connection, class_=AsyncSession, expire_on_commit=False
    )()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture
async def user_repo(test_session):
    return UserRepository(test_session)


@pytest.fixture
async def room_repo(test_session):
    return RoomRepository(test_session)


@pytest.fixture
async def message_repo(test_session):
    return MessageRepository(test_session)


@pytest.fixture
async def mod_repo(test_session):
    return ModerationRepository(test_session)


@pytest.fixture
async def auth_service(user_repo):
    return get_auth_service(user_repo)


@pytest.fixture
async def room_service(room_repo, user_repo):
    return get_room_service(room_repo, user_repo)


@pytest.fixture
async def message_service(message_repo, room_repo):
    return get_message_service(message_repo, room_repo)


@pytest.fixture
async def mod_service(mod_repo, room_repo, user_repo):
    return get_moderation_service(mod_repo, room_repo, user_repo)
