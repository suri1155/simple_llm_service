"""Query endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import get_db
from src.core import QueryRequest, QueryResponse
from src.core.rate_limiter import RateLimiter
from src.services import LLMService
from src.api.dependencies import get_current_user
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/queries", tags=["queries"])
rate_limiter = RateLimiter()
llm_service = LLMService()


@router.post("/", response_model=QueryResponse)
async def create_query(
    query_data: QueryRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Process a user query with LLM.

    Args:
        query_data: Query request data.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        Query response from LLM.

    Raises:
        HTTPException: If rate limited or processing fails.
    """
    # Check rate limit
    if rate_limiter.is_rate_limited(current_user.id):
        remaining = rate_limiter.get_remaining_queries(current_user.id)
        reset_time = rate_limiter.get_reset_time(current_user.id)
        logger.warning(f"Rate limit exceeded for user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Query limit exceeded. Remaining: {remaining}. Resets at {reset_time}",
        )

    try:
        # Process query
        response = await llm_service.process_query(
            current_user.id,
            query_data.query,
            db,
        )

        # Increment counter
        rate_limiter.increment_query_count(current_user.id)

        logger.info(f"Query processed for user {current_user.id}")

        return QueryResponse(**response)

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process query",
        )


@router.get("/history")
async def get_query_history(
    limit: int = 10,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get query history for current user.

    Args:
        limit: Maximum number of records.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        List of query history.
    """
    history = LLMService.get_query_history(db, current_user.id, limit)
    return {"queries": history, "count": len(history)}


@router.get("/stats")
async def get_query_stats(
    current_user=Depends(get_current_user),
):
    """Get query statistics for current user.

    Args:
        current_user: Current authenticated user.

    Returns:
        Query statistics.
    """
    used = rate_limiter.get_user_query_count(current_user.id)
    remaining = rate_limiter.get_remaining_queries(current_user.id)
    reset_time = rate_limiter.get_reset_time(current_user.id)

    return {
        "queries_used_today": used,
        "queries_remaining": remaining,
        "reset_at": reset_time,
    }
