import asyncio
import logging
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import async_session_factory, engine
from app.models.user import User
from app.models.room import Room, room_members
from app.models.message import Message
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")

async def create_users(session: AsyncSession, count: int = 10):
    users = []
    for i in range(count):
        email = f"user{i}@example.com"
        password = get_password_hash("Password123!")
        user = User(email=email, hashed_password=password)
        session.add(user)
        users.append(user)
    await session.commit()
    for u in users:
        await session.refresh(u)
    logger.info("Created %d users", count)
    return users

async def create_rooms(session: AsyncSession, owner: User, count: int = 3):
    rooms = []
    for i in range(count):
        room = Room(name=f"Room {i+1}", owner_id=owner.id)
        session.add(room)
        rooms.append(room)
    await session.commit()
    for r in rooms:
        await session.refresh(r)
        # Add owner as member
        await session.execute(room_members.insert().values(room_id=r.id, user_id=owner.id))
    await session.commit()
    logger.info("Created %d rooms for owner %s", count, owner.email)
    return rooms

async def create_messages(session: AsyncSession, room: Room, user: User, count: int = 10):
    for i in range(count):
        msg = Message(room_id=room.id, user_id=user.id, content=f"Sample message {i+1} in {room.name}")
        session.add(msg)
    await session.commit()
    logger.info("Created %d messages in room %s", count, room.name)

async def main():
    async with async_session_factory() as session:
        users = await create_users(session)
        owner = users[0]
        rooms = await create_rooms(session, owner)
        for room in rooms:
            await create_messages(session, room, owner)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
