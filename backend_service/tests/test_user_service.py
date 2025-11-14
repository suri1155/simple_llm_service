"""Tests for user service."""

import pytest

from src.services import UserService
from src.core.auth import verify_password


def test_create_user(db_session):
    """Test user creation."""
    user = UserService.create_user(
        db_session,
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert verify_password("testpassword123", user.hashed_password)


def test_create_user_duplicate_username(db_session):
    """Test duplicate username rejection."""
    UserService.create_user(
        db_session,
        username="testuser",
        email="test1@example.com",
        password="testpassword123",
    )

    with pytest.raises(ValueError, match="already exists"):
        UserService.create_user(
            db_session,
            username="testuser",
            email="test2@example.com",
            password="testpassword123",
        )


def test_get_user_by_username(db_session):
    """Test getting user by username."""
    created_user = UserService.create_user(
        db_session,
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )

    user = UserService.get_user_by_username(db_session, "testuser")
    assert user.id == created_user.id


def test_authenticate_user(db_session):
    """Test user authentication."""
    UserService.create_user(
        db_session,
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )

    user = UserService.authenticate_user(db_session, "testuser", "testpassword123")
    assert user is not None
    assert user.username == "testuser"


def test_authenticate_user_wrong_password(db_session):
    """Test authentication with wrong password."""
    UserService.create_user(
        db_session,
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )

    user = UserService.authenticate_user(db_session, "testuser", "wrongpassword")
    assert user is None
