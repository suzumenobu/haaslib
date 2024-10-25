from typing import List, Optional, Dict
from datetime import datetime
from ..executor import RequestsExecutor, Authenticated
from ..models.market import (
    Market,
    CloudMarket,
    MarketListResponse,
    PriceSource,
    OrderBook,
    Trade,
    Tick
)
from ..models.price_source import (
    PriceSourceDetail,
    PriceSourceDetailResponse
)
from ..models.market_data import (
    MarketPrice,
    MarketPriceResponse,
    CloudLastTrade,
    CloudTradeContract,
    # PriceSnapshot  # Add this if it exists
)
from ..models.base import ApiResponse
from ..exceptions import HaasApiError

# Public endpoints - no authentication required
def get_server_time(executor: RequestsExecutor) -> int:
    """Returns the server time (UNIX-UTC)"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[int],
        query_params={"channel": "TIME"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get server time")
    return response.Data or 0

def get_all_pricesources_simple(executor: RequestsExecutor) -> List[str]:
    """Returns a simple list of all supported pricesources"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[str]],
        query_params={"channel": "ALL_PRICESOURCES"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get price sources")
    return response.Data or []

def get_pricesources_detailed(executor: RequestsExecutor) -> List[PriceSourceDetail]:
    """Returns detailed information about all supported price sources"""
    response = executor.execute(
        endpoint="Price",
        response_type=PriceSourceDetailResponse,
        query_params={"channel": "ALL_PRICESOURCES"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get detailed price sources")
    return response.Data or []

def get_all_markets(executor: RequestsExecutor) -> List[CloudMarket]:
    """Returns a list of all supported markets"""
    executor.set_debug(False)  # Disable debug by default for this noisy endpoint
    
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={"channel": "MARKETLIST"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get markets")
    return response.Data or []

def get_all_markets_by_source(executor: RequestsExecutor, price_source: str) -> Dict[str, List[CloudMarket]]:
    """Returns a dictionary of supported price sources and their markets"""
    executor.set_debug(False)  # Disable debug by default for this noisy endpoint
    
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[Dict[str, List[CloudMarket]]],
        query_params={"channel": "ALL_MARKETS"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get markets by source")
    return response.Data or {}

def get_unique_markets(executor: RequestsExecutor) -> List[CloudMarket]:
    """Returns a list of all unique markets"""
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={"channel": "UNIQUE_MARKETLIST"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get unique markets")
    return response.Data or []

def get_markets_by_source(executor: RequestsExecutor, price_source: str) -> List[CloudMarket]:
    """Returns markets for a specific price source"""
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={
            "channel": "MARKETS",
            "pricesource": price_source
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get markets for {price_source}")
    return response.Data or []

def get_trade_markets(executor: RequestsExecutor, price_source: str) -> List[CloudMarket]:
    """Returns trade markets for a specific price source"""
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={
            "channel": "TRADE_MARKETS",
            "pricesource": price_source
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get trade markets for {price_source}")
    return response.Data or []

def get_coin_list(executor: RequestsExecutor) -> List[str]:
    """Returns a list of all supported coins"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[str]],
        query_params={"channel": "COINLIST"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get coin list")
    return response.Data or []

def get_price(executor: RequestsExecutor, market_tag: str) -> MarketPrice:
    """
    Get current price information for a market
    
    Args:
        executor: The RequestsExecutor instance
        market_tag: Market identifier (e.g., 'BINANCE_BTC_USDT_')
        
    Returns:
        MarketPrice object containing current price data
        
    Raises:
        HaasApiError: If the API request fails
    """
    response = executor.execute(
        endpoint="Price",
        response_type=MarketPriceResponse,
        query_params={
            "channel": f"PRICE_{market_tag}"
        }
    )
    
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get price for {market_tag}")
    
    return response.Data

def get_orderbook(executor: RequestsExecutor, market: str) -> OrderBook:
    """Returns the orderbook for a market"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[OrderBook],
        query_params={
            "channel": "ORDERBOOK",
            "market": market
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get orderbook for {market}")
    return response.Data

def get_last_trades(executor: RequestsExecutor, market: str) -> List[Trade]:
    """Returns the last trades for a market"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[Trade]],
        query_params={
            "channel": "LASTTRADES",
            "market": market
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get last trades for {market}")
    return response.Data or []

def get_sync_ticks(executor: RequestsExecutor, market: str) -> List[Tick]:
    """Returns the 10 very last minutes of ticks"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[Tick]],
        query_params={
            "channel": "SYNCTICKS",
            "market": market
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get sync ticks for {market}")
    return response.Data or []

def get_last_ticks(executor: RequestsExecutor, market: str, interval: int) -> List[Tick]:
    """Returns between 500 and 1440 ticks"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[Tick]],
        query_params={
            "channel": "LASTTICKS",
            "market": market,
            "interval": interval
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get last ticks for {market}")
    return response.Data or []

def get_deep_ticks(executor: RequestsExecutor, market: str) -> List[Tick]:
    """Returns about 40,000 ticks of the last minutes"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[Tick]],
        query_params={
            "channel": "DEEPTICKS",
            "market": market
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get deep ticks for {market}")
    return response.Data or []

def get_price_snapshot(executor: RequestsExecutor, price_source: str) -> List:
    """Returns a snapshot of the very last prices"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[PriceSnapshot]],
        query_params={
            "channel": "SNAPSHOT",
            "pricesource": price_source
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get price snapshot for {price_source}")
    return response.Data or []

# Private endpoints - require authentication
def get_fiat_conversions(executor: RequestsExecutor[Authenticated]) -> Dict[str, float]:
    """Returns the fiat conversion rates"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[Dict[str, float]],
        query_params={"channel": "FIAT_CONVERSIONS"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get fiat conversions")
    return response.Data or {}

def get_used_margin(executor: RequestsExecutor[Authenticated]) -> float:
    """Returns the currently used margin"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[float],
        query_params={"channel": "USED_MARGIN"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get used margin")
    return response.Data or 0.0

def get_custom_snapshot_minute_tick(executor: RequestsExecutor, markets: List[str]) -> List:
    """
    Fetches a custom snapshot of minute ticks for specified markets.
    
    Args:
        executor: The RequestsExecutor instance
        markets: List of market strings (e.g., ['BINANCEQUARTERLY_SOL_USD_QUARTERLY', ...])
        
    Returns:
        List of snapshot data for the specified markets
        
    Raises:
        HaasApiError: If the API request fails
    """
    # Join the markets into a single string separated by commas
    markets_string = ','.join(markets)
    
    # Execute the request
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List],
        query_params={
            "channel": "CUSTOM_SNAPSHOT_MINUTE_TICK",
            "marketsString": markets_string
        }
    )
    
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get custom snapshot minute tick")
    
    return response.Data or []
