from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
import redis.asyncio as redis
import time
from .config import settings


class RateLimiter:
    def __init__(self):
        self.redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            decode_responses=True
        )
        self.auth_scheme = HTTPBearer(auto_error=False)

    async def check_rate_limit(self, request: Request):
        client_id = await self._get_client_id(request)
        limit, window = await self._get_limits(request)
        key = f"rate_limit:{client_id}"
        now = int(time.time())
        window_start = now - window

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, min=0, max=window_start)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, window)
        results = await pipe.execute()

        request_count = results[2]

        if request_count > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {limit} requests per {window} seconds"
            )

    async def _get_client_id(self, request: Request) -> str:
        credentials = await self.auth_scheme(request)
        if credentials:
            return f"user:{credentials.credentials}"
        return f"ip:{request.client.host}"

    async def _get_limits(self, request: Request) -> tuple[int, int]:
        credentials = await self.auth_scheme(request)
        if credentials:
            return 10, 60
        return 2, 60
