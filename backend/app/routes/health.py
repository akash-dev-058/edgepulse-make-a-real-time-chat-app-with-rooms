import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db

router = APIRouter(tags=["health"])
logger = logging.getLogger("app.routes.health")

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        logger.exception("Health check failed")
        return {"status": "error", "detail": str(exc)}
