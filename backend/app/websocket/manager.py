import json
import logging
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from ..core.redis_client import RedisClient

logger = logging.getLogger("app.websocket.manager")

class ConnectionManager:
    """Manages WebSocket connections per room using Redis Pub/Sub for scaling."""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str) -> None:
        await websocket.accept()
        self.active_connections.setdefault(room_id, set()).add(websocket)
        logger.info("WebSocket connected to room %s", room_id)
        # Subscribe to Redis channel for the room
        asyncio.create_task(self._redis_listener(room_id))

    def disconnect(self, websocket: WebSocket, room_id: str) -> None:
        connections = self.active_connections.get(room_id)
        if connections and websocket in connections:
            connections.remove(websocket)
            logger.info("WebSocket disconnected from room %s", room_id)
        if connections and len(connections) == 0:
            self.active_connections.pop(room_id, None)

    async def broadcast(self, room_id: str, message: dict) -> None:
        # Publish to Redis so all instances receive it
        await RedisClient.publish(f"room:{room_id}", json.dumps(message))
        # Also send to local connections immediately
        await self._send_to_local(room_id, message)

    async def _send_to_local(self, room_id: str, message: dict) -> None:
        connections = self.active_connections.get(room_id, set())
        data = json.dumps(message)
        for ws in connections:
            try:
                await ws.send_text(data)
            except Exception as exc:
                logger.exception("Failed to send message to WebSocket: %s", exc)

    async def _redis_listener(self, room_id: str) -> None:
        channel = f"room:{room_id}"
        pubsub = await RedisClient.subscribe(channel)
        async for msg in pubsub.iter_messages():
            if msg.channel.decode() == channel:
                data = json.loads(msg.data)
                await self._send_to_local(room_id, data)

manager = ConnectionManager()
