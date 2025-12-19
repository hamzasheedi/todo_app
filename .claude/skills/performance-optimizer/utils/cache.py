import asyncio
import time
from typing import Any, Optional, Dict
from collections import OrderedDict
import hashlib
import json
from datetime import datetime, timedelta

class LRUCache:
    """
    Simple in-memory LRU (Least Recently Used) cache implementation
    """
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):  # 5 minutes default TTL
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.expire_times = {}

    def _is_expired(self, key: str) -> bool:
        """
        Check if a cache entry is expired
        """
        if key not in self.expire_times:
            return True
        return time.time() > self.expire_times[key]

    def _cleanup_expired(self):
        """
        Remove expired entries from cache
        """
        expired_keys = [key for key in self.cache.keys() if self._is_expired(key)]
        for key in expired_keys:
            self.cache.pop(key, None)
            self.expire_times.pop(key, None)

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache
        """
        self._cleanup_expired()

        if key not in self.cache:
            return None

        # Move to end (most recently used)
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set a value in cache with optional TTL
        """
        if ttl is None:
            ttl = self.default_ttl

        # Remove expired entries if needed
        self._cleanup_expired()

        # If cache is full, remove the least recently used item
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            self.cache.pop(oldest_key)
            self.expire_times.pop(oldest_key, None)

        # Add the new item
        self.cache[key] = value
        self.expire_times[key] = time.time() + ttl

        # Move to end (most recently used)
        self.cache.move_to_end(key)

    def delete(self, key: str):
        """
        Delete a key from cache
        """
        self.cache.pop(key, None)
        self.expire_times.pop(key, None)

    def clear(self):
        """
        Clear all cache entries
        """
        self.cache.clear()
        self.expire_times.clear()

    def keys(self):
        """
        Get all non-expired keys
        """
        self._cleanup_expired()
        return list(self.cache.keys())

    def size(self) -> int:
        """
        Get current cache size
        """
        self._cleanup_expired()
        return len(self.cache)


class CacheManager:
    """
    Centralized cache manager with multiple cache strategies
    """
    def __init__(self):
        # Different caches for different purposes
        self.user_cache = LRUCache(max_size=500, default_ttl=600)  # 10 minutes for user data
        self.task_cache = LRUCache(max_size=1000, default_ttl=300)  # 5 minutes for tasks
        self.api_cache = LRUCache(max_size=200, default_ttl=180)   # 3 minutes for API responses
        self.session_cache = LRUCache(max_size=1000, default_ttl=1800)  # 30 minutes for sessions

    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        Get user data from cache
        """
        return self.user_cache.get(f"user:{user_id}")

    def set_user(self, user_id: str, user_data: Dict, ttl: Optional[int] = None):
        """
        Set user data in cache
        """
        self.user_cache.set(f"user:{user_id}", user_data, ttl)

    def get_tasks(self, user_id: str) -> Optional[list]:
        """
        Get user tasks from cache
        """
        return self.task_cache.get(f"tasks:{user_id}")

    def set_tasks(self, user_id: str, tasks: list, ttl: Optional[int] = None):
        """
        Set user tasks in cache
        """
        self.task_cache.set(f"tasks:{user_id}", tasks, ttl)

    def get_api_response(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Get API response from cache
        """
        # Create a hash of the parameters to make a unique key
        params_hash = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()
        key = f"api:{endpoint}:{params_hash}"
        return self.api_cache.get(key)

    def set_api_response(self, endpoint: str, params: Dict, response: Dict, ttl: Optional[int] = None):
        """
        Set API response in cache
        """
        params_hash = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()
        key = f"api:{endpoint}:{params_hash}"
        self.api_cache.set(key, response, ttl)

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get session data from cache
        """
        return self.session_cache.get(f"session:{session_id}")

    def set_session(self, session_id: str, session_data: Dict, ttl: Optional[int] = None):
        """
        Set session data in cache
        """
        self.session_cache.set(f"session:{session_id}", session_data, ttl)

    def invalidate_user_cache(self, user_id: str):
        """
        Invalidate all cached data for a user
        """
        self.user_cache.delete(f"user:{user_id}")
        self.task_cache.delete(f"tasks:{user_id}")

    def invalidate_api_cache(self, endpoint: str = None):
        """
        Invalidate API cache, optionally for specific endpoint
        """
        if endpoint:
            # This would require a more complex implementation to find keys by prefix
            keys_to_delete = [k for k in self.api_cache.keys() if k.startswith(f"api:{endpoint}:")]
            for key in keys_to_delete:
                self.api_cache.delete(key)
        else:
            self.api_cache.clear()

    def get_stats(self) -> Dict:
        """
        Get cache statistics
        """
        return {
            'user_cache_size': self.user_cache.size(),
            'task_cache_size': self.task_cache.size(),
            'api_cache_size': self.api_cache.size(),
            'session_cache_size': self.session_cache.size(),
            'total_size': (
                self.user_cache.size() +
                self.task_cache.size() +
                self.api_cache.size() +
                self.session_cache.size()
            )
        }


class AsyncCacheManager:
    """
    Async version of cache manager for use with async operations
    """
    def __init__(self):
        self.cache_manager = CacheManager()

    async def get_user(self, user_id: str) -> Optional[Dict]:
        """
        Async get user data from cache
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.get_user, user_id)

    async def set_user(self, user_id: str, user_data: Dict, ttl: Optional[int] = None):
        """
        Async set user data in cache
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.set_user, user_id, user_data, ttl)

    async def get_tasks(self, user_id: str) -> Optional[list]:
        """
        Async get user tasks from cache
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.get_tasks, user_id)

    async def set_tasks(self, user_id: str, tasks: list, ttl: Optional[int] = None):
        """
        Async set user tasks in cache
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.set_tasks, user_id, tasks, ttl)

    async def get_api_response(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Async get API response from cache
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.get_api_response, endpoint, params)

    async def set_api_response(self, endpoint: str, params: Dict, response: Dict, ttl: Optional[int] = None):
        """
        Async set API response in cache
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.set_api_response, endpoint, params, response, ttl)

    async def invalidate_user_cache(self, user_id: str):
        """
        Async invalidate all cached data for a user
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.cache_manager.invalidate_user_cache, user_id)


# Global cache instance
cache_manager = CacheManager()
async_cache_manager = AsyncCacheManager()

def get_cache_manager():
    """
    Get the global cache manager instance
    """
    return cache_manager


def get_async_cache_manager():
    """
    Get the global async cache manager instance
    """
    return async_cache_manager


# Decorator for caching function results
def cache_result(ttl: int = 300, key_prefix: str = "func"):
    """
    Decorator to cache function results
    """
    def decorator(func):
        cache = LRUCache(max_size=100, default_ttl=ttl)

        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_args = str(args)
            key_kwargs = str(sorted(kwargs.items()))
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5((key_args + key_kwargs).encode()).hexdigest()}"

            # Try to get from cache first
            result = cache.get(cache_key)
            if result is not None:
                return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        return wrapper
    return decorator