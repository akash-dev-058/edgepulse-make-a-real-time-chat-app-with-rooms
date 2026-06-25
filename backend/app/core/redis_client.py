import aioredis
from ..core.config import settings
from typing import Any

class RedisClient:
    """Singleton async Redis client wrapper."""
    _client: aioredis.Redis | None = None

    @classmethod
    async def get_client(cls) -> aioredis.Redis:
        if cls._client is None:
            cls._client = await aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )
        return cls._client

    @classmethod
    async def publish(cls, channel: str, message: str) -> int:
        client = await cls.get_client()
        return await client.publish(channel, message)

    @classmethod
    async def subscribe(cls, channel: str):
        client = await cls.get_client()
        pubsub = client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

    @classmethod
    async def close(cls) -> None:
        if cls._client:
            await cls._client.close()
            cls._client = None
