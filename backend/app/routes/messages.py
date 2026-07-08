from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer

from app.db.session import get_db_session
from app.db.repository import MessageRepository, RoomRepository, UserRepository
from app.services.message_service import get_message_service, MessageService
from app.schemas.message import MessageCreate, MessageOut, MessagePagination
from app.core.rate_limiter import RateLimiter
from app.core.config import settings

from redis.asyncio import Redis

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.post("/{room_slug}", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def create_message(
    room_slug: str,
    payload: MessageCreate,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Not authenticated"})
    payload_token = verify_token(token.credentials, token_type="access")
    if not payload_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})
    user_id = int(payload_token.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/messages/{room_slug}"}), f"messages:create:{user_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    message_repo = MessageRepository(session)
    message_service = get_message_service(message_repo, room_repo)
    user = await user_repo.get_by_id(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
    message = await message_service.create_message(payload, user, room_slug)
    return message


@router.get("/{room_slug}", response_model=MessagePagination)
async def list_messages(
    room_slug: str,
    limit: int = 50,
    offset: int = 0,
    before: datetime = None,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/messages/{room_slug}"}), f"messages:list:{room_slug}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    message_repo = MessageRepository(session)
    message_service = get_message_service(message_repo, room_repo)
    pagination = await message_service.list_messages(room_slug, limit=limit, offset=offset, before=before)
    return pagination


@router.get("/{room_slug}/search", response_model=MessagePagination)
async def search_messages(
    room_slug: str,
    query: str,
    limit: int = 50,
    offset: int = 0,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/messages/{room_slug}/search"}), f"messages:search:{room_slug}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    message_repo = MessageRepository(session)
    message_service = get_message_service(message_repo, room_repo)
    pagination = await message_service.search_messages(room_slug, query, limit=limit, offset=offset)
    return pagination
