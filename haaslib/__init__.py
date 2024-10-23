from __future__ import annotations

import logging
import sys

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Log initial information
logger.info("Starting import in __init__.py")
logger.info(f"Python version: {sys.version}")
logger.info(f"Python path: {sys.path}")

# Import and export components
from .executor import RequestsExecutor, Guest, Authenticated, HaasApiError
from .models import ApiResponse, ModelApiResponse, CloudMarket, MarketList
from .api import get_all_markets, get_all_markets_by_pricesource

logger.info("Finished imports in __init__.py")

__all__ = [
    'RequestsExecutor',
    'Guest',
    'Authenticated',
    'HaasApiError',
    'ApiResponse',
    'ModelApiResponse',
    'CloudMarket',
    'MarketList',
    'get_all_markets',
    'get_all_markets_by_pricesource',
    'logger',
]
