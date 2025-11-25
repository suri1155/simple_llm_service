"""Database models and shared Base.

Centralize the SQLAlchemy `Base` from the DB module to avoid multiple
declaration sites and circular imports. Import `Base` first so model
modules can safely import `from . import Base` without triggering a
partially-initialized package error.
"""

from src.db.database import Base

from .user import User
from .query_log import QueryLog

__all__ = ["Base", "User", "QueryLog"]
