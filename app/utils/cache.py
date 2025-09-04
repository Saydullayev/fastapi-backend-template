import logging
from typing import Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SimpleCache: 
    def __init__(self):
        # shu yerda redis ishlatib ketishni maslahat beraman agar uzoq muddatli cache ishlatish kerak bo'lsa
        self._cache = {}
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = {
            'value': value,
            'expiry': expiry
        }
        logger.debug(f"Cache set: {key} (expires: {expiry})")
    
    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        
        cache_item = self._cache[key]
        if datetime.now() > cache_item['expiry']:
            del self._cache[key]
            logger.debug(f"Cache expired: {key}")
            return None
        
        logger.debug(f"Cache hit: {key}")
        return cache_item['value']
    
    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted: {key}")
            return True
        return False
    
    def clear(self) -> None:
        self._cache.clear()
        logger.debug("Cache cleared")
    
    def cleanup_expired(self) -> int:
        expired_keys = [
            key for key, item in self._cache.items()
            if datetime.now() > item['expiry']
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
        
        return len(expired_keys)


cache = SimpleCache()


class CacheService:
    @staticmethod
    async def get_cached_user(user_id: int) -> Optional[dict]:
        return cache.get(f"user:{user_id}")