import logging
import uuid
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.middleware")

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Assign a unique request ID to each incoming request and log basic info."""
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        logger.info("Start request %s %s - ID %s", request.method, request.url.path, request_id)
        try:
            response: Response = await call_next(request)
        except Exception as exc:
            logger.exception("Exception in request ID %s", request_id)
            raise
        logger.info("Completed request ID %s with status %s", request_id, response.status_code)
        response.headers["X-Request-ID"] = request_id
        return response
