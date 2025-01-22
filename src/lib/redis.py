from typing import Optional
import aioredis
from src.config.env import get_settings

config = get_settings()


class RedisCache:
    def __init__(self):
        self.redis_cache: Optional[aioredis.Redis] = None

    async def init_cache(self):
        self.redis_cache = await aioredis.Redis.from_url(
            f"redis://{config.redis_host}:{config.redis_port}/{config.redis_db}?encoding=utf-8&decode_responses=True"
        )

    async def keys(self, pattern):
        return await self.redis_cache.keys(pattern)

    async def set(self, key, value, ex):
        return await self.redis_cache.set(key, value, ex=ex)

    async def get(self, key):
        return await self.redis_cache.get(key)

    async def delete(self, key):
        return await self.redis_cache.delete(key)

    async def close(self):
        await self.redis_cache.close()

    async def ping(self):
        return await self.redis_cache.ping()


redis_cache = RedisCache()
