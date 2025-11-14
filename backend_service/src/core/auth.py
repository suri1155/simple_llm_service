"""Authentication utilities."""

import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from typing import Optional

from config.settings import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password.

    Returns:
        Hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password.
        hashed_password: Hashed password.

    Returns:
        True if password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token.

    Args:
        data: Data to encode in token.
        expires_delta: Token expiration time delta.

    Returns:
        JWT token string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc)+ timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode a JWT access token.

    Args:
        token: JWT token string.

    Returns:
        Decoded token data.

    Raises:
        jwt.InvalidTokenError: If token is invalid.
    """
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload
