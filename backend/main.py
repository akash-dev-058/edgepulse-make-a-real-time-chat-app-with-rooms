import os
import logging
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.core.logger import configure_logging
from app.core.config import settings
from app.db.session import init_db
from app.routes import auth, rooms, messages, moderation, socket
from app.core.socket import sio_app

# Configure logging before anything else
configure_logging()
logger = logging.getLogger(__name__)

# Sentry SDK setup
sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[sentry_logging, FastApiIntegration()],
    traces_sample_rate=1.0,
    environment=os.getenv("ENVIRONMENT", "development"),
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting RealTimeChatApp backend...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down RealTimeChatApp backend...")

app = FastAPI(
    title="RealTimeChatApp API",
    description="Real-time multi-room chat application backend",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount Socket.IO app under /ws
app.mount("/ws", sio_app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
app.include_router(moderation.router, prefix="/api/v1/moderation", tags=["moderation"])

# Health check
@app.get("/health")
async def health():
    return {"status": "ok", "service": "RealTimeChatApp", "version": "1.0.0"}

# Static files (for production build assets if needed)
if settings.SERVE_STATIC:
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,
        access_log=True,
    )
