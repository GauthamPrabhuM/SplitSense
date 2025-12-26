"""
Rate limiting middleware for FastAPI.
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Rate limit configuration
RATE_LIMIT_PER_MINUTE = 60  # 60 requests per minute per IP
RATE_LIMIT_PER_HOUR = 1000  # 1000 requests per hour per IP

def get_rate_limiter():
    """Get configured rate limiter"""
    return limiter

def get_rate_limit_exceeded_handler():
    """Get rate limit exceeded handler"""
    return _rate_limit_exceeded_handler

