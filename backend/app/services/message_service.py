from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
import html

from app.models.message import Message
from app.models.user import User
from app.models.room import Room
from app.schemas.message import MessageCreate, MessageOut, MessagePagination
from app.db.repository import MessageRepository, RoomRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class MessageService:
    def __init__(self, message_repo: MessageRepository, room_repo: RoomRepository):
        self.message_repo = message_repo
        self.room_repo = room_repo

    def sanitize_content(self, content: str) -> str:
        # Basic XSS prevention
        sanitized = html.escape(content)
        return sanitized

    async def create_message(self, payload: MessageCreate, author: User, room_slug: str) -> MessageOut:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Message creation failed: room not found", room_slug=room_slug, author_id=author.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        # Check membership
        is_member = await self.room_repo.is_member(room.id, author.id)
        if not is_member:
            logger.warning("Message creation failed: user not in room", room_slug=room_slug, author_id=author.id)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error": "Not a member of this room"})

        content_sanitized = self.sanitize_content(payload.content)
        message = await self.message_repo.create(
            Message,
            content=payload.content,
            content_sanitized=content_sanitized,
            author_id=author.id,
            room_id=room.id,
        )
        logger.info("Message created", message_id=message.id, room_id=room.id, author_id=author.id)
        return MessageOut.from_orm(message).copy(update={"author_username": author.username})

    async def list_messages(
        self,
        room_slug: str,
        limit: int = 50,
        offset: int = 0,
        before: Optional[datetime] = None,
    ) -> MessagePagination:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Message list failed: room not found", room_slug=room_slug)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        messages = await self.message_repo.list_messages(room.id, limit=limit, offset=offset, before=before)
        items = [
            MessageOut.from_orm(msg).copy(update={"author_username": msg.author.username})
            for msg in messages
        ]

        next_offset = offset + limit if len(messages) == limit else None
        has_more = next_offset is not None

        return MessagePagination(items=items, next_offset=next_offset, has_more=has_more)

    async def search_messages(self, room_slug: str, query: str, limit: int = 50, offset: int = 0) -> MessagePagination:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Message search failed: room not found", room_slug=room_slug)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        messages = await self.message_repo.search_messages(room.id, query, limit=limit, offset=offset)
        items = [
            MessageOut.from_orm(msg).copy(update={"author_username": msg.author.username})
            for msg in messages
        ]

        next_offset = offset + limit if len(messages) == limit else None
        has_more = next_offset is not None

        return MessagePagination(items=items, next_offset=next_offset, has_more=has_more)


def get_message_service(message_repo: MessageRepository, room_repo: RoomRepository) -> MessageService:
    return MessageService(message_repo, room_repo)
