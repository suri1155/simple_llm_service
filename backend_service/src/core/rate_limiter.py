"""Rate limiting utilities."""

import redis
from datetime import datetime, timedelta, timezone
from typing import Optional

from config.settings import get_settings

settings = get_settings()


class RateLimiter:
    """Rate limiter using Redis."""

    def __init__(self, redis_url: str = settings.redis_url):
        """Initialize rate limiter.

        Args:
            redis_url: Redis connection URL.
        """
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

    def get_user_query_count(self, user_id: int) -> int:
        """Get today's query count for a user.

        Args:
            user_id: User ID.

        Returns:
            Number of queries made today.
        """
        key = self._get_key(user_id)
        count = self.redis_client.get(key)
        return int(count) if count else 0

    def increment_query_count(self, user_id: int) -> int:
        """Increment query count for a user.

        Args:
            user_id: User ID.

        Returns:
            Updated query count.
        """
        key = self._get_key(user_id)
        count = self.redis_client.incr(key)

        # Set expiration on first increment
        if count == 1:
            expire_at = self._get_reset_time()
            ttl = int((expire_at - datetime.now(timezone.utc)).total_seconds())
            self.redis_client.expire(key, ttl)

        return count

    def is_rate_limited(self, user_id: int) -> bool:
        """Check if user has exceeded rate limit.

        Args:
            user_id: User ID.

        Returns:
            True if rate limited, False otherwise.
        """
        count = self.get_user_query_count(user_id)
        return count >= settings.max_queries_per_day

    def get_remaining_queries(self, user_id: int) -> int:
        """Get remaining queries for today.

        Args:
            user_id: User ID.

        Returns:
            Number of remaining queries.
        """
        count = self.get_user_query_count(user_id)
        return max(0, settings.max_queries_per_day - count)

    def get_reset_time(self, user_id: int) -> Optional[datetime]:
        """Get query count reset time for a user.

        Args:
            user_id: User ID.

        Returns:
            Reset time or None if no queries made today.
        """
        key = self._get_key(user_id)
        ttl = self.redis_client.ttl(key)
        if ttl == -1 or ttl == -2:
            return None
        return datetime.now(timezone.utc) + timedelta(seconds=ttl)

    @staticmethod
    def _get_key(user_id: int) -> str:
        """Get Redis key for user's query count.

        Args:
            user_id: User ID.

        Returns:
            Redis key.
        """
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return f"query_count:{user_id}:{today}"

    @staticmethod
    def _get_reset_time() -> datetime:
        """Get next reset time based on configuration.

        Returns:
            Next reset time.
        """
        now = datetime.now(timezone.utc)
        reset_hour = settings.query_reset_hour

        # If reset time hasn't passed today, schedule for today
        reset_time = now.replace(hour=reset_hour, minute=0, second=0, microsecond=0)
        if reset_time > now:
            return reset_time

        # Otherwise, schedule for tomorrow
        return reset_time + timedelta(days=1)
