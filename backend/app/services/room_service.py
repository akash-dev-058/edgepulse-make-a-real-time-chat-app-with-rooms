from typing import Optional

from fastapi import HTTPException, status

from app.models.room import Room, RoomMember
from app.models.user import User
from app.schemas.room import RoomCreate, RoomOut, RoomDetailOut
from app.db.repository import RoomRepository, UserRepository
from app.core.security import generate_room_slug
from app.core.logger import get_logger

logger = get_logger(__name__)


class RoomService:
    def __init__(self, room_repo: RoomRepository, user_repo: UserRepository):
        self.room_repo = room_repo
        self.user_repo = user_repo

    async def create_room(self, payload: RoomCreate, owner: User) -> RoomOut:
        # Generate unique slug
        slug = generate_room_slug(payload.name)
        while await self.room_repo.get_by_slug(slug):
            slug = generate_room_slug(payload.name)

        room = await self.room_repo.create(
            Room,
            name=payload.name,
            slug=slug,
            description=payload.description,
            is_private=payload.is_private,
            max_members=payload.max_members,
            owner_id=owner.id,
        )
        # Add owner as member
        await self.room_repo.add_member(room.id, owner.id)
        logger.info("Room created", room_id=room.id, owner_id=owner.id, slug=slug)
        return RoomOut.from_orm(room)

    async def get_room_by_slug(self, slug: str, user_id: Optional[int] = None) -> RoomDetailOut:
        room = await self.room_repo.get_by_slug(slug)
        if not room:
            logger.warning("Room not found by slug", slug=slug)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        # Check membership if user provided
        is_member = False
        if user_id:
            is_member = await self.room_repo.is_member(room.id, user_id)
            if not is_member and room.is_private:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": "Room is private"})

        member_count = len(room.members)
        return RoomDetailOut.from_orm(room).copy(update={"member_count": member_count, "is_member": is_member})

    async def list_rooms(self, limit: int = 20, offset: int = 0, search: Optional[str] = None) -> list[RoomOut]:
        rooms = await self.room_repo.list_rooms(limit=limit, offset=offset, search=search)
        return [RoomOut.from_orm(room) for room in rooms]

    async def join_room(self, room_slug: str, user: User) -> RoomDetailOut:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Attempt to join non-existent room", room_slug=room_slug, user_id=user.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        if room.is_private and len(room.members) >= (room.max_members or float('inf')):
            logger.warning("Room join denied due to capacity", room_slug=room_slug, user_id=user.id)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": "Room is full"})

        is_member = await self.room_repo.is_member(room.id, user.id)
        if is_member:
            logger.info("User already in room", room_id=room.id, user_id=user.id)
            return await self.get_room_by_slug(room.slug, user.id)

        await self.room_repo.add_member(room.id, user.id)
        logger.info("User joined room", room_id=room.id, user_id=user.id)
        return await self.get_room_by_slug(room.slug, user.id)

    async def leave_room(self, room_slug: str, user: User) -> dict:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Attempt to leave non-existent room", room_slug=room_slug, user_id=user.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        is_member = await self.room_repo.is_member(room.id, user.id)
        if not is_member:
            logger.warning("User not in room", room_id=room.id, user_id=user.id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Not a member"})

        await self.room_repo.remove_member(room.id, user.id)
        logger.info("User left room", room_id=room.id, user_id=user.id)
        return {"message": "Left room successfully"}


def get_room_service(room_repo: RoomRepository, user_repo: UserRepository) -> RoomService:
    return RoomService(room_repo, user_repo)
