"""
Redis caching utilities for improved performance
"""
import json
from typing import Optional, Any
from datetime import timedelta
import redis.asyncio as redis
from .config import settings


class RedisCache:
    """Redis cache manager for application-wide caching"""

    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def connect(self):
        """Connect to Redis server"""
        if not self._client:
            self._client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )

    async def disconnect(self):
        """Disconnect from Redis server"""
        if self._client:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value if exists, None otherwise
        """
        if not self._client:
            await self.connect()

        try:
            value = await self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis GET error: {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache (will be JSON serialized)
            expire: Optional expiration time in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self._client:
            await self.connect()

        try:
            serialized_value = json.dumps(value)
            if expire:
                await self._client.setex(key, expire, serialized_value)
            else:
                await self._client.set(key, serialized_value)
            return True
        except Exception as e:
            print(f"Redis SET error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache

        Args:
            key: Cache key

        Returns:
            True if key was deleted, False otherwise
        """
        if not self._client:
            await self.connect()

        try:
            result = await self._client.delete(key)
            return result > 0
        except Exception as e:
            print(f"Redis DELETE error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache

        Args:
            key: Cache key

        Returns:
            True if key exists, False otherwise
        """
        if not self._client:
            await self.connect()

        try:
            result = await self._client.exists(key)
            return result > 0
        except Exception as e:
            print(f"Redis EXISTS error: {e}")
            return False

    async def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment a counter

        Args:
            key: Cache key
            amount: Amount to increment by (default: 1)

        Returns:
            New value after increment, or None on error
        """
        if not self._client:
            await self.connect()

        try:
            return await self._client.incrby(key, amount)
        except Exception as e:
            print(f"Redis INCRBY error: {e}")
            return None

    async def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration time for a key

        Args:
            key: Cache key
            seconds: Expiration time in seconds

        Returns:
            True if successful, False otherwise
        """
        if not self._client:
            await self.connect()

        try:
            return await self._client.expire(key, seconds)
        except Exception as e:
            print(f"Redis EXPIRE error: {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern

        Args:
            pattern: Key pattern (e.g., "user:*")

        Returns:
            Number of keys deleted
        """
        if not self._client:
            await self.connect()

        try:
            keys = []
            async for key in self._client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                return await self._client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Redis CLEAR_PATTERN error: {e}")
            return 0

    async def ping(self) -> bool:
        """
        Ping Redis server to check connection

        Returns:
            True if connected, False otherwise
        """
        if not self._client:
            await self.connect()

        try:
            return await self._client.ping()
        except Exception as e:
            print(f"Redis PING error: {e}")
            return False


# Global cache instance
cache = RedisCache()


# Cache key generators
def user_cache_key(user_id: str) -> str:
    """Generate cache key for user data"""
    return f"user:{user_id}"


def project_cache_key(project_id: str) -> str:
    """Generate cache key for project data"""
    return f"project:{project_id}"


def client_cache_key(client_id: str) -> str:
    """Generate cache key for client data"""
    return f"client:{client_id}"


def design_concept_cache_key(concept_id: str) -> str:
    """Generate cache key for design concept data"""
    return f"design_concept:{concept_id}"


def product_cache_key(product_id: str) -> str:
    """Generate cache key for product data"""
    return f"product:{product_id}"


# Common expiration times (in seconds)
CACHE_TTL_SHORT = 300  # 5 minutes
CACHE_TTL_MEDIUM = 1800  # 30 minutes
CACHE_TTL_LONG = 3600  # 1 hour
CACHE_TTL_DAY = 86400  # 24 hours
