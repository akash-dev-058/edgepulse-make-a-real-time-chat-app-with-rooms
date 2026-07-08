from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)



class MessageCreate(MessageBase):
    pass


class MessageOut(BaseModel):
    id: int
    content: str
    content_sanitized: str
    author_id: int
    author_username: str
    room_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessagePagination(BaseModel):
    items: list[MessageOut]
    next_offset: Optional[int] = None
    has_more: bool

    class Config:
        from_attributes = True
