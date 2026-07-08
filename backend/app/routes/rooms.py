from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer

from app.db.session import get_db_session
from app.db.repository import RoomRepository, UserRepository
from app.services.room_service import get_room_service, RoomService
from app.schemas.room import RoomCreate, RoomOut, RoomDetailOut
from app.core.rate_limiter import RateLimiter
from app.core.config import settings

from redis.asyncio import Redis

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def create_room(
    payload: RoomCreate,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Not authenticated"})
    from app.core.security import verify_token
    payload_token = verify_token(token.credentials, token_type="access")
    if not payload_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})
    user_id = int(payload_token.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": "/api/v1/rooms/"}), f"rooms:create:{user_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    room_service = get_room_service(room_repo, user_repo)
    user = await user_repo.get_by_id(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
    room = await room_service.create_room(payload, user)
    return room


@router.get("/", response_model=list[RoomOut])
async def list_rooms(
    limit: int = 20,
    offset: int = 0,
    search: str = None,
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": "/api/v1/rooms/"}), "rooms:list")
    room_repo = RoomRepository(session)
    user_repo = UserRepository(session)
    room_service = get_room_service(room_repo, user_repo)
    rooms = await room_service.list_rooms(limit=limit, offset=offset, search=search)
    return rooms


@router.get("/{room_slug}", response_model=RoomDetailOut)
async def get_room(
    room_slug: str,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/rooms/{room_slug}"}), f"rooms:get:{room_slug}")
    user_id = None
    if token:
        payload = verify_token(token.credentials, token_type="access")
        if payload:
            user_id = int(payload.get("sub"))

    room_repo = RoomRepository(session)
    user_repo = UserRepository(session)
    room_service = get_room_service(room_repo, user_repo)
    room = await room_service.get_room_by_slug(room_slug, user_id)
    return room


@router.post("/{room_slug}/join", response_model=RoomDetailOut)
async def join_room(
    room_slug: str,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Not authenticated"})
    payload = verify_token(token.credentials, token_type="access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})
    user_id = int(payload.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/rooms/{room_slug}/join"}), f"rooms:join:{user_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    room_service = get_room_service(room_repo, user_repo)
    user = await user_repo.get_by_id(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
    room = await room_service.join_room(room_slug, user)
    return room


@router.post("/{room_slug}/leave", response_model=dict)
async def leave_room(
    room_slug: str,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Not authenticated"})
    payload = verify_token(token.credentials, token_type="access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})
    user_id = int(payload.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/rooms/{room_slug}/leave"}), f"rooms:leave:{user_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    room_service = get_room_service(room_repo, user_repo)
    user = await user_repo.get_by_id(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
    result = await room_service.leave_room(room_slug, user)
    return result
