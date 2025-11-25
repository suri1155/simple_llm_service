"""Database models and shared Base."""

from .user import User
from .query_log import QueryLog
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


__all__ = ["Base", "User", "QueryLog"]
