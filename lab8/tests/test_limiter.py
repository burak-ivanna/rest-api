import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, Request, status
from app.limiter import RateLimiter
import time


@pytest.mark.asyncio
async def test_anonymous_user_rate_limit():
    mock_redis = MagicMock()
    mock_pipe = MagicMock()
    mock_redis.pipeline.return_value = mock_pipe

    limiter = RateLimiter()
    limiter.redis = mock_redis

    request = AsyncMock(spec=Request)
    request.client.host = "127.0.0.1"
    request.headers = {}

    mock_pipe.execute = AsyncMock(
        side_effect=[[0, 1, 1, True], [1, 2, 2, True]])
    for _ in range(2):
        await limiter.check_rate_limit(request)

    calls = mock_pipe.zadd.call_args_list
    assert len(calls) == 2
    assert calls[0].args[0].startswith("rate_limit:ip:127.0.0.1")

    mock_pipe.execute = AsyncMock(side_effect=[[2, 3, 3, True]])

    with pytest.raises(HTTPException) as exc_info:
        await limiter.check_rate_limit(request)
    assert exc_info.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.asyncio
async def test_authenticated_user_rate_limit():
    mock_redis = MagicMock()
    mock_pipe = MagicMock()
    mock_redis.pipeline.return_value = mock_pipe

    limiter = RateLimiter()
    limiter.redis = mock_redis

    request = AsyncMock(spec=Request)
    request.client.host = "127.0.0.1"
    request.headers = {"authorization": "Bearer valid_token"}

    mock_credentials = MagicMock(credentials="valid_token")
    limiter.auth_scheme = AsyncMock(return_value=mock_credentials)

    mock_pipe.execute = AsyncMock(side_effect=[[0, 1, 1, True]] * 10)
    for _ in range(10):
        await limiter.check_rate_limit(request)

    calls = mock_pipe.zadd.call_args_list
    assert len(calls) == 10
    for call in calls:
        assert call.args[0].startswith("rate_limit:user:valid_token")

    mock_pipe.execute = AsyncMock(side_effect=[[10, 11, 11, True]])

    with pytest.raises(HTTPException) as exc_info:
        await limiter.check_rate_limit(request)
    assert exc_info.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS
