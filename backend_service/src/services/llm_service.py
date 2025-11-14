"""LLM service using LangChain."""

from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.query_log import QueryLog
from src.utils.logger import get_logger
from config.settings import get_settings

from langchain_openai import ChatOpenAI

logger = get_logger(__name__)
settings = get_settings()


class LLMService:
    """LLM service for query processing."""

    def __init__(self):
        """Initialize LLM service."""
        # Initialize LangChain components
        try:
            self.llm = ChatOpenAI(
                temperature=0.7,
                model_name=settings.llm_model,
                openai_api_key=settings.openai_api_key,
            )
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.initialized = False

    async def process_query(self, user_id: int, query: str, db: Session) -> dict:
        """Process user query with LLM.

        Args:
            user_id: User ID.
            query: User query.
            db: Database session.

        Returns:
            Dictionary with response and metadata.
        """
        if not self.initialized:
            raise RuntimeError("LLM service not initialized")

        try:
            # Process query with LLM
            response = self.llm.invoke(query)

            # Log query
            query_log = QueryLog(
                user_id=user_id,
                query=query,
                response=str(response.content),
                llm_model_used=settings.llm_model,
                created_at=datetime.now(timezone.utc),
            )
            db.add(query_log)
            db.commit()

            logger.info(f"Query processed for user {user_id}")

            return {
                "response": str(response.content),
                "llm_model_used": settings.llm_model,
                "created_at": query_log.created_at,
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    @staticmethod
    def get_query_history(db: Session, user_id: int, limit: int = 10) -> list:
        """Get query history for user.

        Args:
            db: Database session.
            user_id: User ID.
            limit: Maximum number of records.

        Returns:
            List of query logs.
        """
        return (
            db.query(QueryLog)
            .filter(QueryLog.user_id == user_id)
            .order_by(QueryLog.created_at.desc())
            .limit(limit)
            .all()
        )
