import time
from fastapi import Request, HTTPException
from app.core.config import settings
import redis
from typing import Optional

class RateLimitMiddleware:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        self.requests = settings.RATE_LIMIT_REQUESTS
        self.window = settings.RATE_LIMIT_WINDOW

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        # Get current count
        current = self.redis_client.get(key)
        
        if current is None:
            # First request in window
            self.redis_client.setex(key, self.window, 1)
        else:
            current = int(current)
            if current >= self.requests:
                # Rate limit exceeded
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )
            # Increment counter
            self.redis_client.incr(key)
        
        # Add retry-after header if approaching limit
        if current and int(current) >= self.requests * 0.8:
            ttl = self.redis_client.ttl(key)
            if ttl > 0:
                response = await call_next(request)
                response.headers["X-RateLimit-Remaining"] = str(self.requests - int(current))
                response.headers["X-RateLimit-Reset"] = str(ttl)
                return response
        
        return await call_next(request) 