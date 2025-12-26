"""
Caching layer for analytics to improve performance.
"""
from typing import Optional, Any, Dict
from functools import wraps
import hashlib
import json
from datetime import datetime, timedelta

# Simple in-memory cache (in production, use Redis)
_cache: Dict[str, tuple[Any, datetime]] = {}
_cache_ttl = timedelta(hours=1)  # Cache for 1 hour


def get_cache_key(*args, **kwargs) -> str:
    """Generate cache key from function arguments"""
    key_data = {
        "args": str(args),
        "kwargs": sorted(kwargs.items())
    }
    key_str = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(ttl: Optional[timedelta] = None):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live for cache entries (default: 1 hour)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{get_cache_key(*args, **kwargs)}"
            
            # Check cache
            if cache_key in _cache:
                result, expiry = _cache[cache_key]
                if datetime.now() < expiry:
                    return result
                else:
                    # Expired, remove from cache
                    del _cache[cache_key]
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Store in cache
            expiry = datetime.now() + (ttl or _cache_ttl)
            _cache[cache_key] = (result, expiry)
            
            return result
        
        return wrapper
    return decorator


def clear_cache():
    """Clear all cached data"""
    global _cache
    _cache = {}


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics"""
    now = datetime.now()
    valid_entries = sum(1 for _, expiry in _cache.values() if expiry > now)
    expired_entries = len(_cache) - valid_entries
    
    return {
        "total_entries": len(_cache),
        "valid_entries": valid_entries,
        "expired_entries": expired_entries,
        "cache_size_mb": 0  # Would need to calculate actual size
    }

