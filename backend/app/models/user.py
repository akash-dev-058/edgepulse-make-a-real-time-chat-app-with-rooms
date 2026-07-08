from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    rooms = relationship("Room", secondary="room_members", back_populates="members")
    owned_rooms = relationship("Room", back_populates="owner", foreign_keys="Room.owner_id")
    messages = relationship("Message", back_populates="author")
    moderation_actions = relationship("ModerationAction", back_populates="moderator")
    reported_messages = relationship("Message", secondary="moderation_actions", viewonly=True)
