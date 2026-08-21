import os
import time
import logging
from typing import Dict, List, Optional
from collections import defaultdict
from app.core.errors import RateLimitError

logger = logging.getLogger("neetpg.rate_limiter")

class InMemoryRateLimiter:
    """
    In-Memory token bucket / sliding window rate limiter for development and unit tests.
    """

    def __init__(self):
        self._history: Dict[str, List[float]] = defaultdict(list)

    def check_rate_limit(self, key: str, max_requests: int, window_seconds: int = 60):
        now = time.time()
        window_start = now - window_seconds

        # Clean old timestamps
        valid_timestamps = [t for t in self._history[key] if t > window_start]
        self._history[key] = valid_timestamps

        if len(valid_timestamps) >= max_requests:
            raise RateLimitError(
                f"Rate limit exceeded ({max_requests} requests per {window_seconds}s). Please wait before retrying."
            )

        self._history[key].append(now)


class DistributedRedisRateLimiter:
    """
    Redis-Backed Distributed Rate Limiter for Staging & Production Multi-Process Deployments.
    Uses Redis sliding window sorted sets (ZADD, ZREMRANGEBYSCORE, ZCARD, EXPIRE).
    """

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or os.getenv("REDIS_URL")
        self._redis_client = None
        self._fallback_limiter = InMemoryRateLimiter()

    def _get_client(self):
        if self._redis_client is None and self.redis_url:
            try:
                import redis
                self._redis_client = redis.from_url(self.redis_url, decode_responses=True)
            except Exception as e:
                logger.warning(f"Could not connect to Redis at {self.redis_url}: {e}. Fallback active.")
        return self._redis_client

    def check_rate_limit(self, key: str, max_requests: int, window_seconds: int = 60):
        client = self._get_client()
        now = time.time()
        window_start = now - window_seconds
        redis_key = f"ratelimit:{key}"

        if client is not None:
            try:
                pipeline = client.pipeline()
                # 1. Remove entries older than window_start
                pipeline.zremrangebyscore(redis_key, 0, window_start)
                # 2. Add current timestamp
                pipeline.zadd(redis_key, {str(now): now})
                # 3. Count elements in current window
                pipeline.zcard(redis_key)
                # 4. Set TTL
                pipeline.expire(redis_key, window_seconds + 5)
                results = pipeline.execute()

                current_count = results[2]
                if current_count > max_requests:
                    raise RateLimitError(
                        f"Rate limit exceeded ({max_requests} requests per {window_seconds}s). Please wait before retrying."
                    )
                return
            except RateLimitError:
                raise
            except Exception as e:
                env = os.getenv("ENVIRONMENT", "development")
                if env in ["production", "staging"]:
                    logger.error(f"Redis rate limit error in {env}: {e}")
                # Fallback to in-memory on non-rate-limit operational errors in dev
                self._fallback_limiter.check_rate_limit(key, max_requests, window_seconds)
        else:
            self._fallback_limiter.check_rate_limit(key, max_requests, window_seconds)


# Primary Rate Limiter Instance
rate_limiter = DistributedRedisRateLimiter()
