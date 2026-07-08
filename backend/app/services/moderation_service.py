from typing import Optional

from fastapi import HTTPException, status

from app.models.moderation import ModerationAction, ModerationActionType
from app.models.user import User
from app.models.room import Room
from app.db.repository import ModerationRepository, RoomRepository, UserRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class ModerationService:
    def __init__(
        self,
        mod_repo: ModerationRepository,
        room_repo: RoomRepository,
        user_repo: UserRepository,
    ):
        self.mod_repo = mod_repo
        self.room_repo = room_repo
        self.user_repo = user_repo

    async def ban_user(self, room_slug: str, moderator: User, target_user_id: int, reason: Optional[str] = None) -> ModerationAction:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Ban failed: room not found", room_slug=room_slug, moderator_id=moderator.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        target_user = await self.user_repo.get_by_id(User, target_user_id)
        if not target_user:
            logger.warning("Ban failed: target user not found", target_user_id=target_user_id, moderator_id=moderator.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})

        # Check if target is in room
        is_member = await self.room_repo.is_member(room.id, target_user_id)
        if not is_member:
            logger.warning("Ban failed: target not in room", room_slug=room_slug, target_user_id=target_user_id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "User not in room"})

        # Create moderation action
        action = await self.mod_repo.create(
            ModerationAction,
            action_type=ModerationActionType.BAN,
            reason=reason,
            target_user_id=target_user_id,
            moderator_id=moderator.id,
            room_id=room.id,
        )
        logger.info("User banned", room_id=room.id, moderator_id=moderator.id, target_user_id=target_user_id)
        return action

    async def kick_user(self, room_slug: str, moderator: User, target_user_id: int, reason: Optional[str] = None) -> ModerationAction:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Kick failed: room not found", room_slug=room_slug, moderator_id=moderator.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        target_user = await self.user_repo.get_by_id(User, target_user_id)
        if not target_user:
            logger.warning("Kick failed: target user not found", target_user_id=target_user_id, moderator_id=moderator.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})

        is_member = await self.room_repo.is_member(room.id, target_user_id)
        if not is_member:
            logger.warning("Kick failed: target not in room", room_slug=room_slug, target_user_id=target_user_id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "User not in room"})

        action = await self.mod_repo.create(
            ModerationAction,
            action_type=ModerationActionType.KICK,
            reason=reason,
            target_user_id=target_user_id,
            moderator_id=moderator.id,
            room_id=room.id,
        )
        # Remove from room
        await self.room_repo.remove_member(room.id, target_user_id)
        logger.info("User kicked", room_id=room.id, moderator_id=moderator.id, target_user_id=target_user_id)
        return action

    async def report_message(self, room_slug: str, reporter: User, message_id: int, reason: Optional[str] = None) -> ModerationAction:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Report failed: room not found", room_slug=room_slug, reporter_id=reporter.id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})

        # Check if message belongs to room
        from app.db.repository import MessageRepository
        msg_repo = MessageRepository(self.mod_repo.session)
        message = await msg_repo.get_by_id(Message, message_id)
        if not message or message.room_id != room.id:
            logger.warning("Report failed: message not found or not in room", message_id=message_id, room_slug=room_slug)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Message not found"})

        action = await self.mod_repo.create(
            ModerationAction,
            action_type=ModerationActionType.REPORT,
            reason=reason,
            target_message_id=message_id,
            target_user_id=message.author_id,
            moderator_id=reporter.id,
            room_id=room.id,
        )
        logger.info("Message reported", room_id=room.id, reporter_id=reporter.id, message_id=message_id)
        return action

    async def get_recent_actions(self, room_slug: str, limit: int = 20) -> list[dict]:
        room = await self.room_repo.get_by_slug(room_slug)
        if not room:
            logger.warning("Recent actions fetch failed: room not found", room_slug=room_slug)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Room not found"})
        actions = await self.mod_repo.get_recent_actions(room.id, limit=limit)
        return [
            {
                "id": a.id,
                "action_type": a.action_type.value,
                "reason": a.reason,
                "moderator_username": a.moderator.username,
                "target_user_username": a.target_user.username if a.target_user else None,
                "created_at": a.created_at.isoformat(),
            }
            for a in actions
        ]


def get_moderation_service(
    mod_repo: ModerationRepository,
    room_repo: RoomRepository,
    user_repo: UserRepository,
) -> ModerationService:
    return ModerationService(mod_repo, room_repo, user_repo)
