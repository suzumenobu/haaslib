from typing import Dict, Any
from ..executor import RequestsExecutor
from ..models.interface import MarketInfo, MarketPriceInfo, MarketTechnicalInfo

def get_market_info(
    executor: RequestsExecutor,
    market: str
) -> MarketInfo:
    """Returns the market information page"""
    response = executor.execute(
        endpoint="InterfaceAPI",
        command="MARKET_INFO",
        params={"market": market}
    )
    return MarketInfo(**response.data)

def get_market_price_info(
    executor: RequestsExecutor,
    market: str
) -> MarketPriceInfo:
    """Returns the market price information page"""
    response = executor.execute(
        endpoint="InterfaceAPI",
        command="MARKET_PRICE_INFO",
        params={"market": market}
    )
    return MarketPriceInfo(**response.data)

def get_market_ta_info(
    executor: RequestsExecutor,
    market: str
) -> MarketTechnicalInfo:
    """Returns the market price technical analysis page"""
    response = executor.execute(
        endpoint="InterfaceAPI",
        command="MARKET_TA_INFO",
        params={"market": market}
    )
    return MarketTechnicalInfo(**response.data)
