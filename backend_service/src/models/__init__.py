"""Database models and shared Base."""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .query_log import QueryLog

__all__ = ["Base", "User", "QueryLog"]
