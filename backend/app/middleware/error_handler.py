import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger("app.error_handler")

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("HTTPException %s: %s", exc.status_code, exc.detail, exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "request_id": request.state.request_id if hasattr(request.state, "request_id") else None},
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception for request %s", getattr(request.state, "request_id", "unknown"))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request.state.request_id if hasattr(request.state, "request_id") else None},
    )
