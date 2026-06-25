from __future__ import annotations
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List

class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

class RoomRead(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
    created_at: datetime
    member_ids: List[UUID] = []

    class Config:
        from_attributes = True
