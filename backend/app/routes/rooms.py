import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.room import RoomCreate, RoomRead
from ..services.room_service import RoomService
from ..dependencies import get_db, get_current_user
from ..models.room import Room

router = APIRouter(prefix="/rooms", tags=["rooms"])
logger = logging.getLogger("app.routes.rooms")

@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
async def create_room(room_in: RoomCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        room = await RoomService.create_room(db, current_user, room_in)
        return room
    except Exception as exc:
        logger.exception("Failed to create room")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create room")

@router.get("/me", response_model=list[RoomRead])
async def list_my_rooms(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rooms = await RoomService.get_user_rooms(db, current_user)
    return rooms

@router.get("/{room_id}", response_model=RoomRead)
async def get_room(room_id: str, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    room = await RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    # Verify membership
    if current_user.id != room.owner_id and current_user not in room.members:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    member_ids = [member.id for member in room.members]
    return RoomRead(
        id=room.id,
        name=room.name,
        owner_id=room.owner_id,
        created_at=room.created_at,
        member_ids=member_ids,
    )

@router.post("/{room_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_member(room_id: str, user_id: str, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    room = await RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can add members")
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await RoomService.add_member(db, room, user)
    return None

@router.delete("/{room_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(room_id: str, user_id: str, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    room = await RoomService.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can remove members")
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await RoomService.remove_member(db, room, user)
    return None
