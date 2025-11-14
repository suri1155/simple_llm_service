"""Authentication dependencies."""

from fastapi import Depends, HTTPException, status

# from fastapi.security import HTTPBearer, HTTPAuthCredentials
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.db import get_db
from src.core import decode_access_token
from src.services import UserService
from src.utils.logger import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """Get current authenticated user.

    Args:
        credentials: HTTP bearer credentials.
        db: Database session.

    Returns:
        Authenticated user.

    Raises:
        HTTPException: If authentication fails.
    """
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = UserService.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
