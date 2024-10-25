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

# Export models
from .models.market import (
    Market,
    MarketListResponse,
    PriceSource,
    OrderBook,
    Trade,
    Tick,
    PriceSnapshot,
    FiatConversion
)
from .models.auth import AuthResponse
from .models.trading import (
    Order,
    MarginSettings
)
from .exceptions import AuthenticationError, HaasApiError
from .executor import RequestsExecutor, Authenticated, Guest
from .api.market import get_all_markets, get_all_markets_by_pricesource
from .api.price import (
    get_server_time,
    get_all_pricesources_simple,
    get_pricesources_detailed,
    get_all_markets_by_source,
    get_all_markets,
    get_unique_markets,
    get_markets_by_source,
    get_trade_markets,
    get_coin_list,
    get_price,
    get_orderbook,
    get_last_trades,
    get_sync_ticks,
    get_last_ticks,
    get_deep_ticks,
    get_price_snapshot,
    get_fiat_conversions
)
from .api.trading import (
    place_order,
    cancel_order,
    get_used_margin
)

__all__ = [
    'Market',
    'MarketListResponse',
    'PriceSource',
    'OrderBook',
    'Trade',
    'Tick',
    'PriceSnapshot',
    'FiatConversion',
    'AuthResponse',
    'AuthenticationError',
    'HaasApiError',
    'RequestsExecutor',
    'Authenticated',
    'Guest',
    'get_all_markets',
    'get_all_markets_by_pricesource',
    'get_server_time',
    'get_all_pricesources_simple',
    'get_pricesources_detailed',
    'get_all_markets_by_source',
    'get_all_markets',
    'get_unique_markets',
    'get_markets_by_source',
    'get_trade_markets',
    'get_coin_list',
    'get_price',
    'get_orderbook',
    'get_last_trades',
    'get_sync_ticks',
    'get_last_ticks',
    'get_deep_ticks',
    'get_price_snapshot',
    'get_fiat_conversions',
    'Order',
    'MarginSettings',
    'place_order',
    'cancel_order',
    'get_used_margin'
]

logger.info("Finished imports in __init__.py")
