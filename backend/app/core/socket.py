import asyncio
from typing import Any, Dict

import socketio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis

from app.core.config import settings
from app.core.logger import get_logger
from app.db.session import get_db_session
from app.db.repository import UserRepository
from app.services.auth import get_auth_service
from app.services.socket_service import SocketService

logger = get_logger(__name__)

# Create Socket.IO ASGI app
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[], client_manager=None, logger=False, engineio_logger=False)
sio_app = socketio.AsyncServerApp(sio, socketio_path="/ws/socket.io")

# FastAPI app for WebSocket routes
socket_app = FastAPI(title="RealTimeChatApp Socket.IO", version="1.0.0")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, Any]] = {}

    async def connect(self, sid: str, room_slug: str, user_id: int) -> None:
        if room_slug not in self.active_connections:
            self.active_connections[room_slug] = {}
        self.active_connections[room_slug][sid] = {"user_id": user_id, "sid": sid}
        logger.info("Socket connected", sid=sid, room_slug=room_slug, user_id=user_id)

    async def disconnect(self, sid: str, room_slug: str) -> None:
        if room_slug in self.active_connections and sid in self.active_connections[room_slug]:
            user_id = self.active_connections[room_slug][sid]["user_id"]
            del self.active_connections[room_slug][sid]
            if not self.active_connections[room_slug]:
                del self.active_connections[room_slug]
            logger.info("Socket disconnected", sid=sid, room_slug=room_slug, user_id=user_id)

    async def get_room_presence(self, room_slug: str) -> list[dict]:
        if room_slug not in self.active_connections:
            return []
        return [
            {"user_id": data["user_id"], "sid": data["sid"]}
            for data in self.active_connections[room_slug].values()
        ]

    async def broadcast_presence_update(self, room_slug: str) -> None:
        presence = await self.get_room_presence(room_slug)
        await sio.emit("presence_update", {"room_slug": room_slug, "users": presence}, room=room_slug, namespace="/")

    async def broadcast_moderation(self, room_slug: str, event: str, data: dict) -> None:
        await sio.emit(event, data, room=room_slug, namespace="/")


manager = ConnectionManager()


@sio.on("connect", namespace="/")
async def connect(sid: str, environ: dict) -> bool:
    # Extract token from query params
    token = environ.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
    if not token:
        logger.warning("Socket connection rejected: no token", sid=sid)
        return False

    # Verify token
    from app.core.security import verify_token
    payload = verify_token(token, token_type="access")
    if not payload:
        logger.warning("Socket connection rejected: invalid token", sid=sid)
        return False

    user_id = payload.get("sub")
    sio.enter_room(sid, f"user:{user_id}")
    logger.info("Socket connected", sid=sid, user_id=user_id)
    return True


@sio.on("disconnect", namespace="/")
async def disconnect(sid: str) -> None:
    # Find user_id from room
    user_room = None
    for room in sio.rooms(sid):
        if room.startswith("user:"):
            user_room = room
            break
    if user_room:
        user_id = int(user_room.split(":")[1])
        # Find room_slug from other rooms
        room_slug = None
        for room in sio.rooms(sid):
            if room != user_room and not room.startswith("user:"):
                room_slug = room
                break
        if room_slug:
            await manager.disconnect(sid, room_slug)
            await manager.broadcast_presence_update(room_slug)
        logger.info("Socket disconnected", sid=sid, user_id=user_id)


@sio.on("joinRoom", namespace="/")
async def join_room(sid: str, data: dict) -> None:
    room_slug = data.get("room_slug")
    if not room_slug:
        logger.warning("joinRoom failed: missing room_slug", sid=sid)
        return

    # Extract user_id from user room
    user_room = None
    for room in sio.rooms(sid):
        if room.startswith("user:"):
            user_room = room
            break
    if not user_room:
        logger.warning("joinRoom failed: no user room", sid=sid)
        return
    user_id = int(user_room.split(":")[1])

    # Add to room
    sio.enter_room(sid, room_slug)

    # Register connection
    await manager.connect(sid, room_slug, user_id)

    # Broadcast presence update
    await manager.broadcast_presence_update(room_slug)

    logger.info("User joined room", sid=sid, room_slug=room_slug, user_id=user_id)


@sio.on("leaveRoom", namespace="/")
async def leave_room(sid: str, data: dict) -> None:
    room_slug = data.get("room_slug")
    if not room_slug:
        logger.warning("leaveRoom failed: missing room_slug", sid=sid)
        return

    user_room = None
    for room in sio.rooms(sid):
        if room.startswith("user:"):
            user_room = room
            break
    if not user_room:
        return
    user_id = int(user_room.split(":")[1])

    sio.leave_room(sid, room_slug)
    await manager.disconnect(sid, room_slug)
    await manager.broadcast_presence_update(room_slug)
    logger.info("User left room", sid=sid, room_slug=room_slug, user_id=user_id)


@sio.on("sendMessage", namespace="/")
async def send_message(sid: str, data: dict) -> None:
    room_slug = data.get("room_slug")
    content = data.get("content")
    if not room_slug or not content:
        logger.warning("sendMessage failed: missing fields", sid=sid)
        return

    user_room = None
    for room in sio.rooms(sid):
        if room.startswith("user:"):
            user_room = room
            break
    if not user_room:
        return
    user_id = int(user_room.split(":")[1])

    # Broadcast message to room
    await sio.emit(
        "newMessage",
        {
            "room_slug": room_slug,
            "content": content,
            "author_id": user_id,
            "created_at": "now",
        },
        room=room_slug,
        namespace="/",
    )
    logger.info("Message broadcast", room_slug=room_slug, author_id=user_id)


@sio.on("banUser", namespace="/")
async def ban_user(sid: str, data: dict) -> None:
    room_slug = data.get("room_slug")
    target_user_id = data.get("target_user_id")
    reason = data.get("reason")
    if not room_slug or not target_user_id:
        logger.warning("banUser failed: missing fields", sid=sid)
        return

    user_room = None
    for room in sio.rooms(sid):
        if room.startswith("user:"):
            user_room = room
            break
    if not user_room:
        return
    moderator_id = int(user_room.split(":")[1])

    # Broadcast moderation event
    await manager.broadcast_moderation(
        room_slug,
        "moderation",
        {
            "action": "ban",
            "moderator_id": moderator_id,
            "target_user_id": target_user_id,
            "reason": reason,
        },
    )
    logger.info("Ban event broadcast", room_slug=room_slug, moderator_id=moderator_id, target_user_id=target_user_id)


@sio.on("kickUser", namespace="/")
async def kick_user(sid: str, data: dict) -> None:
    room_slug = data.get("room_slug")
    target_user_id = data.get("target_user_id")
    reason = data.get("reason")
    if not room_slug or not target_user_id:
        logger.warning("kickUser failed: missing fields", sid=sid)
        return

    user_room = None
    for room in sio.rooms(sid):
        if room.startswith("user:"):
            user_room = room
            break
    if not user_room:
        return
    moderator_id = int(user_room.split(":")[1])

    await manager.broadcast_moderation(
        room_slug,
        "moderation",
        {
            "action": "kick",
            "moderator_id": moderator_id,
            "target_user_id": target_user_id,
            "reason": reason,
        },
    )
    logger.info("Kick event broadcast", room_slug=room_slug, moderator_id=moderator_id, target_user_id=target_user_id)
