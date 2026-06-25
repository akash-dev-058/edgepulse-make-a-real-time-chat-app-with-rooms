import logging
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, desc
from ..models.message import Message
from ..schemas.message import MessageCreate

logger = logging.getLogger("app.services.message")

class MessageService:
    @staticmethod
    async def create_message(db: AsyncSession, user_id: str, message_in: MessageCreate) -> Message:
        stmt = insert(Message).values(
            room_id=message_in.room_id,
            user_id=user_id,
            content=message_in.content,
        ).returning(Message)
        result = await db.execute(stmt)
        await db.commit()
        message = result.fetchone()
        logger.info("Message %s created in room %s by user %s", message.id, message.room_id, user_id)
        return message

    @staticmethod
    async def get_messages(db: AsyncSession, room_id: str, limit: int = 50, offset: int = 0) -> List[Message]:
        stmt = (
            select(Message)
            .where(Message.room_id == room_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(stmt)
        messages = result.scalars().all()
        logger.debug("Fetched %d messages for room %s", len(messages), room_id)
        return messages
