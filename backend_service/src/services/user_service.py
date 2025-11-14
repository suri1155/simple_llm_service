"""User service."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.user import User
from src.core.auth import hash_password, verify_password
from src.utils.logger import get_logger

logger = get_logger(__name__)


class UserService:
    """User service for database operations."""

    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str) -> User:
        """Create a new user.

        Args:
            db: Database session.
            username: Username.
            email: User email.
            password: Plain text password.

        Returns:
            Created user.

        Raises:
            ValueError: If username or email already exists.
        """
        hashed_password = hash_password(password)
        user = User(username=username, email=email, hashed_password=hashed_password)

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"User created: {username}")
            return user
        except IntegrityError:
            db.rollback()
            logger.error(f"Failed to create user: {username} (duplicate)")
            raise ValueError("Username or email already exists")

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        """Get user by username.

        Args:
            db: Database session.
            username: Username.

        Returns:
            User object or None.
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Get user by ID.

        Args:
            db: Database session.
            user_id: User ID.

        Returns:
            User object or None.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User | None:
        """Authenticate user.

        Args:
            db: Database session.
            username: Username.
            password: Plain text password.

        Returns:
            User object if authentication successful, None otherwise.
        """
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
