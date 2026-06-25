from fastapi import APIRouter, WebSocket, Depends
from ..dependencies import get_current_user, get_db
from ..websocket.handlers import websocket_endpoint

router = APIRouter()

@router.websocket("/ws")
async def websocket_route(websocket: WebSocket, token: str = None, db = Depends(get_db)):
    await websocket_endpoint(websocket, token=token, db=db)
