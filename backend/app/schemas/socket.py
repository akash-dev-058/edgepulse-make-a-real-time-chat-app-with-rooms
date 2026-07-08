from pydantic import BaseModel
from typing import Optional


class SocketAuth(BaseModel):
    token: str


class JoinRoom(BaseModel):
    room_slug: str


class SendMessage(BaseModel):
    content: str


class ModerationAction(BaseModel):
    action_type: str
    target_user_id: int
    reason: Optional[str] = None
