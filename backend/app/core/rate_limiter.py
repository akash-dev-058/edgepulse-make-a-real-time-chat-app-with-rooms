import time
from typing import Callable

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from redis.asyncio import Redis

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self, redis: Redis, max_requests: int = settings.RATE_LIMIT, window: int = 60):
        self.redis = redis
        self.max_requests = max_requests
        self.window = window

    async def is_rate_limited(self, key: str) -> bool:
        pipe = self.redis.pipeline()
        now = int(time.time())
        pipe.zadd(key, {str(now): now})
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zcard(key)
        pipe.expire(key, self.window)
        count = await pipe.execute()[-1]
        return count > self.max_requests

    async def check_rate_limit(self, request: Request, key: str) -> None:
        is_limited = await self.is_rate_limited(key)
        if is_limited:
            logger.warning("Rate limit exceeded", key=key, path=request.url.path)
            raise HTTPException(
                status_code=429,
                detail={"error": "Too many requests", "message": "Rate limit exceeded"}
            )


def get_rate_limiter(redis: Redis) -> RateLimiter:
    return RateLimiter(redis)
