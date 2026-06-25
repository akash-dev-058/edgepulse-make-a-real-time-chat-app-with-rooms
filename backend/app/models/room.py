import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

room_members = Table(
    "room_members",
    Base.metadata,
    Column("room_id", UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_room_members_user_id", "user_id"),
)

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (Index("ix_rooms_owner_id", "owner_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner = relationship("User", backref="owned_rooms")
    members = relationship("User", secondary=room_members, backref="rooms")
