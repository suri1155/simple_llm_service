"""Query log database model."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from . import Base


class QueryLog(Base):
    """Query log model for tracking user queries."""

    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    llm_model_used = Column(String(255), nullable=False)
    tokens_used = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<QueryLog(id={self.id}, user_id={self.user_id}, model={self.llm_model_used})>"
