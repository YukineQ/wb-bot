from typing import Any

from core.helpers.cache.base import BaseBackend
from core.helpers.redis import redis_client


class RedisBackend(BaseBackend):
    async def get(self, *, key: str) -> Any:
        result = await redis_client.get(key)
        if not result:
            return

        return result

    async def get_keys(self) -> Any:
        return redis_client.keys()

    async def set(self, *, key: str, val: str) -> Any:
        await redis_client.set(name=key, value=val)

    async def delete(self, *, key: str) -> Any:
        async for key in redis_client.scan_iter(f"{key}"):
            await redis_client.delete(key)
