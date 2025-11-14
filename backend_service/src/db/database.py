"""Database connection and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.settings import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session.

    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
