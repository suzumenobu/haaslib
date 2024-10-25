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
from .models.market import Market, MarketListResponse

log = logging.getLogger(__name__)

def get_all_markets(executor: RequestsExecutor) -> List[Market]:
    """Get all available markets"""
    response = executor.execute(
        endpoint="Price",
        response_type=MarketListResponse,
        query_params={"channel": "MARKETLIST"}
    )
    
    if not response.Success:
        raise HaasApiError(response.Error or "Failed to get markets")
    return response.Data or []

def get_all_markets_by_pricesource(executor: RequestsExecutor, price_source: str) -> List[CloudMarket]:
    """Get markets filtered by price source"""
    markets = get_all_markets(executor)
    
    # Validate the markets data
    if not isinstance(markets, MarketList):
        raise HaasApiError(f"Unexpected markets format: {markets}")
    
    return [
        market for market in markets.root 
        if market.price_source.lower() == price_source.lower()
    ]

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
