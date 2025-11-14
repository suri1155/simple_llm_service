"""Tests for rate limiter."""

import pytest

from src.core.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    """Create rate limiter instance."""
    # Use in-memory Redis for testing
    return RateLimiter("redis://localhost:6379/1")


def test_increment_query_count(rate_limiter):
    """Test incrementing query count."""
    count = rate_limiter.increment_query_count(user_id=1)
    assert count == 1

    count = rate_limiter.increment_query_count(user_id=1)
    assert count == 2


def test_is_rate_limited(rate_limiter, settings):
    """Test rate limit check."""
    # Increment to limit
    for i in range(settings.max_queries_per_day):
        rate_limiter.increment_query_count(user_id=2)

    assert rate_limiter.is_rate_limited(user_id=2)


def test_get_remaining_queries(rate_limiter, settings):
    """Test remaining queries calculation."""
    rate_limiter.increment_query_count(user_id=3)
    remaining = rate_limiter.get_remaining_queries(user_id=3)
    assert remaining == settings.max_queries_per_day - 1
