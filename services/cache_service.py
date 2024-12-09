
import aioredis
from functools import wraps
from config.settings import settings
import asyncio
import json


class CacheService:
    """Cache service using Redis with hierarchical key patterns."""

    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.namespace = settings.CACHE_NAMESPACE
        self.redis = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        self.redis = await aioredis.create_redis_pool(self.redis_url)

    def _format_key(self, key_parts: List[str]):
        return f"{self.namespace}:" + ":".join(key_parts)

    def cached(self, timeout=60):
        """Decorator for caching function results with invalidation support."""

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                key_parts = [func.__name__] + [str(arg) for arg in args] + [f"{k}={v}" for k, v in kwargs.items()]
                key = self._format_key(key_parts)
                cached_value = await self.redis.get(key)
                if cached_value:
                    # Deserialize the cached JSON string
                    result = json.loads(cached_value)
                    return result
                result = await func(*args, **kwargs)
                # Serialize the result to a JSON string
                serialized_result = json.dumps(result, default=str)
                await self.redis.set(key, serialized_result, expire=timeout)
                return result

            return wrapper

        return decorator

    async def invalidate(self, key_parts: List[str]):
        """Invalidates cache keys matching a pattern."""
        pattern = self._format_key(key_parts) + "*"
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)


cache = CacheService()
