import logging
import sys
import os
import time
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
haaslib_logger = logging.getLogger('haaslib')

haaslib_logger.info("Starting import in __init__.py")
haaslib_logger.info(f"Python version: {sys.version}")
haaslib_logger.info(f"Python path: {sys.path}")

# Import from executor instead of api
from .executor import RequestsExecutor, Guest, Authenticated, HaasApiError
from .model import (
    CloudMarket,
    ApiResponse,
    MarketList,
    AccountList,
    UserLabDetails,
    UserLabBacktestResult,
)
from .api import (
    get_all_markets,
    get_all_markets_by_pricesource,
    get_lab_details,
    update_lab_details,
    get_backtest_result,
    get_all_labs,
    delete_lab,
)

haaslib_logger.info("Finished imports in __init__.py")

# Make logger available for other modules
__all__ = [
    'haaslib_logger',
    'RequestsExecutor',
    'Guest',
    'Authenticated',
    'HaasApiError',
    'CloudMarket',
    'ApiResponse',
    'MarketList',
    'AccountList',
    'UserLabDetails',
    'UserLabBacktestResult',
    'get_all_markets',
    'get_all_markets_by_pricesource',
    'get_lab_details',
    'update_lab_details',
    'get_backtest_result',
    'get_all_labs',
    'delete_lab',
]
