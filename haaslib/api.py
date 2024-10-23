from __future__ import annotations
import logging
from typing import List, Dict, Any, Optional

from .executor import RequestsExecutor, Authenticated, Guest, HaasApiError
from .model import (
    CloudMarket,
    AccountList,
    MarketList,
    UserLabDetails,
    GetBacktestResultRequest,
    UserLabBacktestResult,
    CreateLabRequest,
    StartLabExecutionRequest,
    HaasScriptItemWithDependencies,
    ApiResponse,
)

log = logging.getLogger(__name__)

def get_all_markets(executor: RequestsExecutor[Authenticated]) -> MarketList:
    """Get all available markets"""
    log.info("Fetching all markets")
    response = executor.execute(
        endpoint="Price",
        response_type=dict,  # Change to dict temporarily for debugging
        query_params={"channel": "MARKETLIST"}
    )
    log.debug(f"Raw response: {response}")
    
    if not response.Success:
        raise HaasApiError(f"Failed to fetch markets: {response}")
    
    # Convert the response to MarketList
    try:
        if isinstance(response.Data, dict):
            return MarketList(**response.Data)
        elif isinstance(response.Data, list):
            return MarketList(root=response.Data)
        else:
            raise HaasApiError(f"Unexpected response format: {response.Data}")
    except Exception as e:
        log.error(f"Error parsing market data: {e}")
        raise HaasApiError(f"Failed to parse market data: {e}")

def get_all_markets_by_pricesource(
    executor: RequestsExecutor[Authenticated],
    price_source: str
) -> List[CloudMarket]:
    """Get markets filtered by price source"""
    log.info(f"Fetching markets for price source: {price_source}")
    response = executor.execute(
        endpoint="Price",
        response_type=dict,  # Change to dict temporarily for debugging
        query_params={"channel": "MARKETLIST", "pricesource": price_source}
    )
    log.debug(f"Raw response: {response}")
    
    if not response.Success:
        raise HaasApiError(f"Failed to fetch markets: {response}")
    
    try:
        if isinstance(response.Data, dict):
            markets = MarketList(**response.Data)
        elif isinstance(response.Data, list):
            markets = MarketList(root=response.Data)
        else:
            raise HaasApiError(f"Unexpected response format: {response.Data}")
        
        return [
            market for market in markets.root 
            if market.price_source.lower() == price_source.lower()
        ]
    except Exception as e:
        log.error(f"Error parsing market data: {e}")
        raise HaasApiError(f"Failed to parse market data: {e}")

def get_lab_details(executor: RequestsExecutor[Authenticated], lab_id: str) -> UserLabDetails:
    response = executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={"channel": "GET_LAB_DETAILS", "labId": lab_id},
    )
    return response.Data

def update_lab_details(executor: RequestsExecutor[Authenticated], lab_id: str, details: UserLabDetails) -> None:
    response = executor.execute(
        endpoint="Labs",
        response_type=None,
        query_params={"channel": "UPDATE_LAB_DETAILS", "labId": lab_id, "details": details.model_dump()},
    )
    if not response.Success:
        raise HaasApiError(f"Failed to update lab details: {response.Error}")

def get_backtest_result(
    executor: RequestsExecutor[Authenticated], 
    request: GetBacktestResultRequest
) -> UserLabBacktestResult:
    response = executor.execute(
        endpoint="Labs",
        response_type=UserLabBacktestResult,
        query_params={"channel": "GET_BACKTEST_RESULT", "request": request.model_dump()},
    )
    return response.Data

def get_all_labs(executor: RequestsExecutor[Authenticated]) -> List[UserLabDetails]:
    response = executor.execute(
        endpoint="Labs",
        response_type=List[UserLabDetails],
        query_params={"channel": "GET_ALL_LABS"},
    )
    return response.Data

def delete_lab(executor: RequestsExecutor[Authenticated], lab_id: str) -> None:
    response = executor.execute(
        endpoint="Labs",
        response_type=None,
        query_params={"channel": "DELETE_LAB", "labId": lab_id},
    )
    if not response.Success:
        raise HaasApiError(f"Failed to delete lab: {response.Error}")

# Move other functions from api_functions.py here
