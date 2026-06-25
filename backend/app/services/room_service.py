import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from ..models.room import Room, room_members
from ..models.user import User
from ..schemas.room import RoomCreate

logger = logging.getLogger("app.services.room")

class RoomService:
    @staticmethod
    async def create_room(db: AsyncSession, owner: User, room_in: RoomCreate) -> Room:
        room = Room(name=room_in.name, owner_id=owner.id)
        db.add(room)
        await db.commit()
        await db.refresh(room)
        # Add owner as member
        stmt = insert(room_members).values(room_id=room.id, user_id=owner.id)
        await db.execute(stmt)
        await db.commit()
        logger.info("Room %s created by user %s", room.id, owner.id)
        return room

    @staticmethod
    async def get_user_rooms(db: AsyncSession, user: User) -> List[Room]:
        stmt = select(Room).join(room_members).where(room_members.c.user_id == user.id)
        result = await db.execute(stmt)
        rooms = result.scalars().unique().all()
        logger.debug("Fetched %d rooms for user %s", len(rooms), user.id)
        return rooms

    @staticmethod
    async def get_room_by_id(db: AsyncSession, room_id: str) -> Room | None:
        stmt = select(Room).where(Room.id == room_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def add_member(db: AsyncSession, room: Room, user: User) -> None:
        stmt = insert(room_members).values(room_id=room.id, user_id=user.id)
        await db.execute(stmt)
        await db.commit()
        logger.info("Added user %s to room %s", user.id, room.id)

    @staticmethod
    async def remove_member(db: AsyncSession, room: Room, user: User) -> None:
        stmt = delete(room_members).where(room_members.c.room_id == room.id, room_members.c.user_id == user.id)
        await db.execute(stmt)
        await db.commit()
        logger.info("Removed user %s from room %s", user.id, room.id)
