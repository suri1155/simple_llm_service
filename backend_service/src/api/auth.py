"""Auth endpoints."""

from datetime import timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import get_db
from src.core import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserResponse,
    create_access_token,
)
from src.services import UserService
from src.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """Register a new user.

    Args:
        user_data: User registration data.
        db: Database session.

    Returns:
        Created user.

    Raises:
        HTTPException: If registration fails.
    """
    try:
        user = UserService.create_user(
            db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )
        return user
    except ValueError as e:
        logger.warning(f"Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """Authenticate user and return access token.

    Args:
        credentials: User login credentials.
        db: Database session.

    Returns:
        Access token.

    Raises:
        HTTPException: If authentication fails.
    """
    user = UserService.authenticate_user(
        db,
        username=credentials.username,
        password=credentials.password,
    )

    if not user:
        logger.warning(f"Login failed for user: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    logger.info(f"User logged in: {user.username}")

    return TokenResponse(access_token=access_token)
