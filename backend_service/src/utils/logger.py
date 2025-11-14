"""Utility functions."""

import logging
from config.settings import get_settings

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)
