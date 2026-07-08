from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBearer

from app.db.session import get_db_session
from app.db.repository import UserRepository
from app.services.auth import get_auth_service, AuthService
from app.schemas.auth import UserCreate, UserLogin, Token, RefreshToken, UserOut
from app.core.security import verify_token
from app.core.rate_limiter import RateLimiter
from app.core.config import settings

from redis.asyncio import Redis

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": "/api/v1/auth/register"}), "auth:register")
    user_repo = UserRepository(session)
    auth_service = get_auth_service(user_repo)
    user = await auth_service.register_user(payload)
    return user


@router.post("/login", response_model=Token)
async def login(
    payload: UserLogin,
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": "/api/v1/auth/login"}), "auth:login")
    user_repo = UserRepository(session)
    auth_service = get_auth_service(user_repo)
    user = await auth_service.authenticate_user(payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid credentials"}
        )
    tokens = await auth_service.create_tokens(user)
    return Token(**tokens)


@router.post("/refresh", response_model=Token)
async def refresh(
    payload: RefreshToken,
    session=Depends(get_db_session),
    redis: Redis = Depends(lambda: Redis.from_url(settings.REDIS_URL)),
    rate_limiter: RateLimiter = Depends(lambda: RateLimiter(redis)),
):
    await rate_limiter.check_rate_limit(Request({"url": "/api/v1/auth/refresh"}), "auth:refresh")
    user_repo = UserRepository(session)
    auth_service = get_auth_service(user_repo)
    tokens = await auth_service.refresh_tokens(payload.refresh_token)
    return Token(**tokens)


@router.get("/me", response_model=UserOut)
async def get_me(
    token: str = Depends(bearer),
    session=Depends(get_db_session),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Not authenticated"})
    try:
        payload = verify_token(token.credentials, token_type="access")
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})
        user_id = payload.get("sub")
        user_repo = UserRepository(session)
        user = await user_repo.get_by_id(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"})
        return UserOut.from_orm(user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid token"})
