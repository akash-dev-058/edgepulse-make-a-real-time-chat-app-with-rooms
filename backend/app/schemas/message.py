from __future__ import annotations
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    room_id: UUID = Field(..., description="Target room ID")
    content: str = Field(..., min_length=1, max_length=2000)

class MessageRead(BaseModel):
    id: UUID
    room_id: UUID
    user_id: UUID | None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
