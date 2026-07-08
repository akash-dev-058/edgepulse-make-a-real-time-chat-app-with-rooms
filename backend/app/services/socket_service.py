from typing import Optional

from app.core.logger import get_logger

logger = get_logger(__name__)


class SocketService:
    """Service layer for Socket.IO operations. Currently a pass-through to core socket handlers."""
    pass


def get_socket_service() -> SocketService:
    return SocketService()
