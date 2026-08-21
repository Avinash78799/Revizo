import os
import pytest
from app.services.rate_limiter import DistributedRedisRateLimiter
from app.core.errors import RateLimitError

REDIS_URL = os.getenv("REDIS_URL", "redis://:staging_redis_password_2026@127.0.0.1:6379/0")

def test_live_redis_distributed_rate_limiting():
    """
    Gate 5: Real Redis Distributed Rate Limiting Test (Prompt 12, Gate 5/6).
    Simulates multiple backend worker instances sharing the same Redis cluster state.
    """
    # Create two separate limiter instances representing Worker Process 1 and Worker Process 2
    worker_1_limiter = DistributedRedisRateLimiter(redis_url=REDIS_URL)
    worker_2_limiter = DistributedRedisRateLimiter(redis_url=REDIS_URL)

    test_key = "student-test-redis-user-1"
    
    # Clean test key in Redis
    client = worker_1_limiter._get_client()
    if client is not None:
        try:
            client.ping()
        except Exception:
            pytest.skip("Live Redis service is currently offline on host.")
        client.delete(f"ratelimit:{test_key}")
    else:
        pytest.skip("Redis client not configured.")

    max_allowed = 5
    window_sec = 10

    # Worker 1 consumes 3 tokens
    for _ in range(3):
        worker_1_limiter.check_rate_limit(key=test_key, max_requests=max_allowed, window_seconds=window_sec)

    # Worker 2 consumes 2 tokens (total 5 consumed -> now at limit)
    for _ in range(2):
        worker_2_limiter.check_rate_limit(key=test_key, max_requests=max_allowed, window_seconds=window_sec)

    # 6th request from Worker 1 MUST raise RateLimitError because state is shared in Redis
    with pytest.raises(RateLimitError) as exc_info:
        worker_1_limiter.check_rate_limit(key=test_key, max_requests=max_allowed, window_seconds=window_sec)

    assert f"Rate limit exceeded ({max_allowed} requests per {window_sec}s)" in str(exc_info.value)

    # Verify Redis key has TTL set
    ttl = client.ttl(f"ratelimit:{test_key}")
    assert ttl > 0 and ttl <= window_sec + 5

    # Clean up
    client.delete(f"ratelimit:{test_key}")
