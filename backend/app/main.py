import logging
import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .middleware.logging import RequestIDMiddleware
from .middleware.error_handler import http_exception_handler, unhandled_exception_handler
from .middleware.rate_limit import RateLimitMiddleware
from .routes import auth, rooms, messages, health, ws_router

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.main")

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=1.0)

app = FastAPI(title="RealTimeRoomChat API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middlewares
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RateLimitMiddleware)

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# Include routers
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(messages.router)
app.include_router(health.router)
app.include_router(ws_router.router)

@app.on_event("shutdown")
async def shutdown_event():
    from .core.redis_client import RedisClient
    await RedisClient.close()
    logger.info("Application shutdown: Redis connection closed")
