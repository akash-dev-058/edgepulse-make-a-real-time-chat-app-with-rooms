import json
import logging
from fastapi import WebSocket, Depends, HTTPException, status
from ..dependencies import get_current_user, get_db
from ..models.user import User
from ..schemas.message import MessageCreate
from ..services.message_service import MessageService
from .manager import manager

logger = logging.getLogger("app.websocket.handlers")

async def websocket_endpoint(websocket: WebSocket, token: str = None, db = Depends(get_db)):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    # Validate JWT
    try:
        from ..core.security import decode_access_token
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except Exception as exc:
        logger.exception("WebSocket auth failed: %s", exc)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    # Retrieve user
    user = await db.get(User, user_id)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    # Expect first message to be a JSON with room_id
    await websocket.accept()
    try:
        init_msg = await websocket.receive_text()
        init_data = json.loads(init_msg)
        room_id = init_data.get("room_id")
        if not room_id:
            raise ValueError("room_id missing in init payload")
    except Exception as exc:
        logger.exception("Failed to receive init message: %s", exc)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(websocket, room_id)
    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)
            if data.get("type") == "typing":
                # Broadcast typing indicator without persisting
                await manager.broadcast(room_id, {"type": "typing", "user_id": str(user.id)})
                continue
            # Assume it's a chat message
            content = data.get("content")
            if not content:
                continue
            # Persist message
            msg_in = MessageCreate(room_id=room_id, content=content)
            message = await MessageService.create_message(db, str(user.id), msg_in)
            # Broadcast persisted message
            await manager.broadcast(room_id, {
                "type": "message",
                "id": str(message.id),
                "room_id": str(message.room_id),
                "user_id": str(message.user_id) if message.user_id else None,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        logger.info("WebSocket client disconnected from room %s", room_id)
    except Exception as exc:
        logger.exception("Error in WebSocket loop: %s", exc)
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
