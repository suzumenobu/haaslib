from typing import List
from ..executor import RequestsExecutor
from ..models import CloudMarket, MarketList
from .. import logger

def get_all_markets(executor: RequestsExecutor) -> MarketList:
    """Get all available markets"""
    logger.debug("Fetching all markets")
    response = executor.execute(
        endpoint="Price",
        response_type=dict,
        query_params={"channel": "MARKETLIST"}
    )
    
    logger.debug(f"Raw market response: {response}")
    
    if not response.Success:
        raise HaasApiError(f"Failed to fetch markets: {response.Error}")
    
    # Handle empty response
    if not response.Data:
        return MarketList(root=[])
    
    # If response.Data is already a list
    if isinstance(response.Data, list):
        return MarketList(root=response.Data)
    
    # If response.Data is a dict with a 'root' key
    if isinstance(response.Data, dict) and 'root' in response.Data:
        return MarketList(**response.Data)
    
    # If response.Data is a dict but needs to be wrapped
    if isinstance(response.Data, dict):
        return MarketList(root=[response.Data])
    
    raise HaasApiError(f"Unexpected market data format: {response.Data}")

def get_all_markets_by_pricesource(
    executor: RequestsExecutor,
    price_source: str
) -> List[CloudMarket]:
    """Get markets filtered by price source"""
    markets = get_all_markets(executor)
    return [
        market for market in markets.root
        if market.price_source.lower() == price_source.lower()
    ]
