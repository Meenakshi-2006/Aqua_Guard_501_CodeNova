
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def log_execution(func):
    """Log the execution of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Executing %s", func.__name__)

        try:
            result = func(*args, **kwargs)
            logger.info("%s completed successfully", func.__name__)
            return result
        except Exception:
            logger.exception("%s failed", func.__name__)
            raise

    return wrapper


def handle_errors(func):
    """Handle unexpected errors in a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            logger.exception("Error in %s", func.__name__)

            return {
                "success": False,
                "message": "An unexpected error occurred",
                "error": str(error)
            }

    return wrapper
