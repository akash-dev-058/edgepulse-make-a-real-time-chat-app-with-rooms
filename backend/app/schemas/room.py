from pydantic import BaseModel, Field
from typing import Optional


class RoomBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    is_private: bool = False
    max_members: Optional[int] = None



class RoomCreate(RoomBase):
    pass


class RoomOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    is_private: bool
    max_members: Optional[int]
    owner_id: int

    class Config:
        from_attributes = True


class RoomMemberOut(BaseModel):
    user_id: int
    username: str
    joined_at: str

    class Config:
        from_attributes = True


class RoomDetailOut(RoomOut):
    owner_username: str
    member_count: int
    is_member: bool

    class Config:
        from_attributes = True
