from sqlalchemy import Column, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ModerationActionType(str, Enum):
    BAN = "ban"
    KICK = "kick"
    REPORT = "report"


class ModerationAction(BaseModel):
    __tablename__ = "moderation_actions"

    action_type = Column(Enum(ModerationActionType), nullable=False)
    reason = Column(Text, nullable=True)
    target_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_message_id = Column(Integer, ForeignKey("messages.id", ondelete="CASCADE"), nullable=True)

    # Foreign keys
    moderator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    moderator = relationship("User", back_populates="moderation_actions")
    target_user = relationship("User", foreign_keys=[target_user_id])
    target_message = relationship("Message")

    __table_args__ = (
        Index("ix_moderation_room_id_created_at", "room_id", "created_at"),
    )
