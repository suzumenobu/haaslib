from typing import List, Dict, Optional
from datetime import datetime
from ..executor import RequestsExecutor, Authenticated
from ..models.market import (
    Market,
    MarketListResponse,
    PriceSource,
    OrderBook,
    Trade,
    Tick,
    # PriceSnapshot,
    # FiatConversion
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

def get_pricesources_detailed(executor: RequestsExecutor) -> List[PriceSource]:
    """Returns a detailed list of all supported pricesources"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[List[PriceSource]],
        query_params={"channel": "PRICESOURCES"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get detailed price sources")
    return response.Data or []

def get_all_markets(executor: RequestsExecutor) -> List[Market]:
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

def get_all_markets_by_source(executor: RequestsExecutor, price_source: str) -> Dict[str, List[Market]]:
    """Returns a dictionary of supported price sources and their markets"""
    executor.set_debug(False)  # Disable debug by default for this noisy endpoint
    
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[Dict[str, List[Market]]],
        query_params={"channel": "ALL_MARKETS"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get markets by source")
    return response.Data or {}

def get_unique_markets(executor: RequestsExecutor) -> List[Market]:
    """Returns a list of all unique markets"""
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={"channel": "UNIQUE_MARKETLIST"}
    )
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get unique markets")
    return response.Data or []

def get_markets_by_source(executor: RequestsExecutor, price_source: str) -> List[Market]:
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

def get_trade_markets(executor: RequestsExecutor, price_source: str) -> List[Market]:
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

def get_price(executor: RequestsExecutor, market: str) -> float:
    """Returns the last price for a market"""
    response = executor.execute(
        endpoint="Price",
        response_type=ApiResponse[float],
        query_params={
            "channel": "PRICE",
            "market": market
        }
    )
    if not response.Success:
        raise HaasApiError(response.Error or f"Failed to get price for {market}")
    return response.Data or 0.0

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
