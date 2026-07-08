from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer

from app.db.session import get_db_session
from app.db.repository import ModerationRepository, RoomRepository, UserRepository
from app.services.moderation_service import get_moderation_service, ModerationService
from app.core.rate_limiter import RateLimiter
from app.core.config import settings

from redis.asyncio import Redis

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.post("/{room_slug}/ban", response_model=dict)
async def ban_user(
    room_slug: str,
    target_user_id: int,
    reason: str = None,
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
    moderator_id = int(payload.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/moderation/{room_slug}/ban"}), f"moderation:ban:{moderator_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    mod_repo = ModerationRepository(session)
    mod_service = get_moderation_service(mod_repo, room_repo, user_repo)
    moderator = await user_repo.get_by_id(User, moderator_id)
    if not moderator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Moderator not found"})
    await mod_service.ban_user(room_slug, moderator, target_user_id, reason)
    return {"message": "User banned successfully"}


@router.post("/{room_slug}/kick", response_model=dict)
async def kick_user(
    room_slug: str,
    target_user_id: int,
    reason: str = None,
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
    moderator_id = int(payload.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/moderation/{room_slug}/kick"}), f"moderation:kick:{moderator_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    mod_repo = ModerationRepository(session)
    mod_service = get_moderation_service(mod_repo, room_repo, user_repo)
    moderator = await user_repo.get_by_id(User, moderator_id)
    if not moderator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Moderator not found"})
    await mod_service.kick_user(room_slug, moderator, target_user_id, reason)
    return {"message": "User kicked successfully"}


@router.post("/{room_slug}/report", response_model=dict)
async def report_message(
    room_slug: str,
    message_id: int,
    reason: str = None,
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
    reporter_id = int(payload.get("sub"))

    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/moderation/{room_slug}/report"}), f"moderation:report:{reporter_id}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    mod_repo = ModerationRepository(session)
    mod_service = get_moderation_service(mod_repo, room_repo, user_repo)
    reporter = await user_repo.get_by_id(User, reporter_id)
    if not reporter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Reporter not found"})
    await mod_service.report_message(room_slug, reporter, message_id, reason)
    return {"message": "Message reported successfully"}


@router.get("/{room_slug}/recent", response_model=list[dict])
async def get_recent_actions(
    room_slug: str,
    limit: int = 20,
    token: str = Depends(bearer),
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": f"/api/v1/moderation/{room_slug}/recent"}), f"moderation:recent:{room_slug}")

    user_repo = UserRepository(session)
    room_repo = RoomRepository(session)
    mod_repo = ModerationRepository(session)
    mod_service = get_moderation_service(mod_repo, room_repo, user_repo)
    actions = await mod_service.get_recent_actions(room_slug, limit=limit)
    return actions
