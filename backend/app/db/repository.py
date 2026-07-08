from typing import Any, Dict, List, Optional, Type, TypeVar
from datetime import datetime

from sqlalchemy import select, and_, or_, desc, asc, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.base import BaseModel
from app.core.logger import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, model: Type[ModelType], id: Any) -> Optional[ModelType]:
        result = await self.session.execute(select(model).where(model.id == id))
        return result.scalars().first()

    async def get_all(self, model: Type[ModelType], limit: int = 100, offset: int = 0) -> List[ModelType]:
        result = await self.session.execute(select(model).offset(offset).limit(limit))
        return result.scalars().all()

    async def create(self, model: Type[ModelType], **kwargs) -> ModelType:
        instance = model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.flush()


class UserRepository(BaseRepository):
    async def get_by_email(self, email: str) -> Optional["User"]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> Optional["User"]:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def search(self, query: str, limit: int = 10) -> List["User"]:
        stmt = (
            select(User)
            .where(
                or_(
                    User.username.ilike(f"%{query}%"),
                    User.email.ilike(f"%{query}%"),
                )
            )
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()


class RoomRepository(BaseRepository):
    async def get_by_slug(self, slug: str) -> Optional["Room"]:
        result = await self.session.execute(select(Room).where(Room.slug == slug))
        return result.scalars().first()

    async def list_rooms(self, limit: int = 20, offset: int = 0, search: Optional[str] = None) -> List["Room"]:
        stmt = select(Room).options(joinedload(Room.owner)).offset(offset).limit(limit)
        if search:
            stmt = stmt.where(Room.name.ilike(f"%{search}%"))
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def get_room_with_members(self, room_id: int) -> Optional["Room"]:
        result = await self.session.execute(
            select(Room)
            .where(Room.id == room_id)
            .options(joinedload(Room.members), joinedload(Room.owner))
        )
        return result.scalars().first()

    async def add_member(self, room_id: int, user_id: int) -> bool:
        from app.models.room import RoomMember
        instance = RoomMember(user_id=user_id, room_id=room_id)
        self.session.add(instance)
        await self.session.flush()
        return True

    async def remove_member(self, room_id: int, user_id: int) -> bool:
        from app.models.room import RoomMember
        result = await self.session.execute(
            select(RoomMember).where(
                and_(RoomMember.room_id == room_id, RoomMember.user_id == user_id)
            )
        )
        member = result.scalars().first()
        if member:
            await self.session.delete(member)
            await self.session.flush()
            return True
        return False

    async def is_member(self, room_id: int, user_id: int) -> bool:
        from app.models.room import RoomMember
        result = await self.session.execute(
            select(RoomMember).where(
                and_(RoomMember.room_id == room_id, RoomMember.user_id == user_id)
            )
        )
        return result.scalars().first() is not None


class MessageRepository(BaseRepository):
    async def list_messages(
        self,
        room_id: int,
        limit: int = 50,
        offset: int = 0,
        before: Optional[datetime] = None,
    ) -> List["Message"]:
        stmt = (
            select(Message)
            .where(Message.room_id == room_id)
            .options(joinedload(Message.author))
            .order_by(desc(Message.created_at))
            .offset(offset)
            .limit(limit)
        )
        if before:
            stmt = stmt.where(Message.created_at < before)
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()

    async def search_messages(
        self,
        room_id: int,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List["Message"]:
        # Use PostgreSQL full-text search if available
        stmt = (
            select(Message)
            .where(and_(Message.room_id == room_id))
            .options(joinedload(Message.author))
            .order_by(desc(Message.created_at))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().unique().all()


class ModerationRepository(BaseRepository):
    async def get_recent_actions(self, room_id: int, limit: int = 20) -> List["ModerationAction"]:
        result = await self.session.execute(
            select(ModerationAction)
            .where(ModerationAction.room_id == room_id)
            .options(joinedload(ModerationAction.moderator), joinedload(ModerationAction.target_user))
            .order_by(desc(ModerationAction.created_at))
            .limit(limit)
        )
        return result.scalars().unique().all()
