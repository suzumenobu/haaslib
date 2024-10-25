from typing import Optional
from ..executor import RequestsExecutor
from ..models.base import ApiResponse
from ..models.trading import (
    Order, 
    MarginSettings,
    MaxAmountRequest,
    MaxAmountResponse,
    CancelOrdersRequest
)
from ..exceptions import HaasApiError

def place_order(
    executor: RequestsExecutor,
    order: Order
) -> bool:
    """Places an order"""
    response = executor.execute(
        endpoint="TradingAPI",
        command="PLACE_ORDER",
        params={"order": order.model_dump()}
    )
    return response.success

def cancel_order(
    executor: RequestsExecutor,
    account_id: str,
    order_id: str
) -> bool:
    """Cancels an open order"""
    response = executor.execute(
        endpoint="TradingAPI",
        command="CANCEL_ORDER",
        params={
            "accountid": account_id,
            "orderid": order_id
        }
    )
    return response.success

def get_used_margin(
    executor: RequestsExecutor,
    settings: MarginSettings
) -> float:
    """Returns what the used margin is"""
    response = executor.execute(
        endpoint="TradingAPI",
        command="USED_MARGIN",
        params=settings.model_dump()
    )
    return response.data

def get_max_amount(
    executor: RequestsExecutor,
    request: MaxAmountRequest
) -> MaxAmountResponse:
    """Calculates the maximum trade amount, price and margin"""
    response = executor.execute(
        endpoint="TradingAPI",
        command="MAX_AMOUNT",
        params=request.model_dump()
    )
    return MaxAmountResponse(**response.data)

def cancel_all_orders(
    executor: RequestsExecutor,
    request: CancelOrdersRequest
) -> bool:
    """Cancels all open orders, accountid and market as optional"""
    response = executor.execute(
        endpoint="TradingAPI",
        command="CANCEL_ALL_OPEN_ORDERS",
        params=request.model_dump(exclude_none=True)
    )
    return response.success
