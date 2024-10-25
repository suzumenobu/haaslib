from typing import List
from ..executor import RequestsExecutor, Authenticated
from ..models.market import Market, MarketListResponse
from ..exceptions import HaasApiError as HaasApiError
from ..exceptions import MarketError as MarketError


def get_all_markets(executor: RequestsExecutor) -> List[Market]:
    """Get all available markets"""
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={"channel": "GET_MARKET_LIST"}
    )
    
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get markets")
        
    if not response.Data:
        return []
        
    return response.Data

def get_all_markets_by_pricesource(
    executor: RequestsExecutor,
    price_source: str
) -> List[Market]:
    """Get markets filtered by price source"""
    markets = get_all_markets(executor)
    return [
        market for market in markets
        if market.price_source.lower() == price_source.lower()
    ]

def get_market_price(
    executor: RequestsExecutor,
    market_tag: str
) -> float:
    """Get current price for a market"""
    response = executor.execute(
        endpoint="Price",
        response_type=dict,
        query_params={
            "channel": "GET_PRICE",
            "marketTag": market_tag
        }
    )
    
    if not response.Success:
        raise MarketError(f"Failed to get price for {market_tag}: {response.Error}")
    
    return float(response.Data.get("price", 0))
