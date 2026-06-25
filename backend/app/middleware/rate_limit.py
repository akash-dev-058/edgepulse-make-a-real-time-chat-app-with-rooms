import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

# Simple in-memory rate limiter: 5 requests per minute per IP for login endpoint
RATE_LIMIT = 5
WINDOW_SECONDS = 60

class RateLimitMiddleware(BaseHTTPMiddleware):
    _hits: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/auth/login":
            client_ip = request.client.host if request.client else "anonymous"
            now = time.time()
            timestamps = self._hits[client_ip]
            # Remove timestamps older than window
            timestamps = [ts for ts in timestamps if now - ts < WINDOW_SECONDS]
            timestamps.append(now)
            self._hits[client_ip] = timestamps
            if len(timestamps) > RATE_LIMIT:
                raise HTTPException(status_code=429, detail="Too many login attempts, please try again later.")
        response = await call_next(request)
        return response
