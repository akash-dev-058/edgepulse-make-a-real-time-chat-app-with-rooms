from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Room(BaseModel):
    __tablename__ = "rooms"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False, nullable=False)
    max_members = Column(Integer, nullable=True)

    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="owned_rooms")
    members = relationship("User", secondary="room_members", back_populates="rooms")
    messages = relationship("Message", back_populates="room", order_by="desc(Message.created_at)")


# Association table for many-to-many between users and rooms
class RoomMember(BaseModel):
    __tablename__ = "room_members"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
