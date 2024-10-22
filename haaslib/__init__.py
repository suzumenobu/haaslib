from .logging_config import setup_logging, logger

setup_logging()

logger.info("Starting import in __init__.py")

from .api import RequestsExecutor, HaasApiError

__all__ = ['RequestsExecutor', 'HaasApiError']

logger.info("Finished imports in __init__.py")
