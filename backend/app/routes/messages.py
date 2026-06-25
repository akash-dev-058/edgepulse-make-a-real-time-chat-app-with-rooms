import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.message import MessageCreate, MessageRead
from ..services.message_service import MessageService
from ..dependencies import get_current_user, get_db

router = APIRouter(prefix="/messages", tags=["messages"])
logger = logging.getLogger("app.routes.messages")

@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def send_message(msg_in: MessageCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        message = await MessageService.create_message(db, str(current_user.id), msg_in)
        return message
    except Exception as exc:
        logger.exception("Failed to send message")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not send message")

@router.get("/room/{room_id}", response_model=list[MessageRead])
async def get_room_messages(
    room_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify user is member of room
    from ..models.room import Room
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if current_user.id != room.owner_id and current_user not in room.members:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    messages = await MessageService.get_messages(db, room_id, limit=limit, offset=offset)
    return messages
