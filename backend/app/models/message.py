from sqlalchemy import Column, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    content = Column(Text, nullable=False)
    content_sanitized = Column(Text, nullable=False)

    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    author = relationship("User", back_populates="messages")
    room = relationship("Room", back_populates="messages")

    # Indexes
    __table_args__ = (
        Index("ix_messages_room_id_created_at", "room_id", "created_at"),
        Index("ix_messages_author_id", "author_id"),
    )
