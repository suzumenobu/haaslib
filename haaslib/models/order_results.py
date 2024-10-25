from typing import List, Dict
from typing_extensions import Any, Optional
from pydantic import BaseModel, Field

class UserOrderCancelResult(BaseModel):
    """Result of order cancellation attempt"""
    is_cancelled: bool = Field(alias="IsCancelled")
    is_not_open: bool = Field(alias="IsNotOpen")
    cancel_failed: bool = Field(alias="CancelFailed")

    class Config:
        populate_by_name = True

class UserOrderExecutionResult(BaseModel):
    """Result of order execution attempt"""
    success: bool = Field(alias="Success")
    order_id: str = Field(alias="OrderId")
    order: Any = Field(alias="Order")
    result: Any = Field(alias="Result")
    error_message: Optional[str] = Field(alias="ErrorMessage")
    error_code: Optional[str] = Field(alias="ErrorCode")

    class Config:
        populate_by_name = True

class UserOrder(BaseModel):
    """User order information"""
    unix: int = Field(alias="Unix")
    order_id: str = Field(alias="OrderId")
    stop_order_id: str = Field(alias="StopOrderId")
    market: str = Field(alias="Market")
    direction: str = Field(alias="Direction")
    type: str = Field(alias="Type")
    order_price: float = Field(alias="OrderPrice")
    trigger_price: float = Field(alias="TriggerPrice")
    order_amount: float = Field(alias="OrderAmount")
    trade_amount: float = Field(alias="TradeAmount")
    status: str = Field(alias="Status")
    bot_id: str = Field(alias="BotId")
    notes: str = Field(alias="Notes")

    class Config:
        populate_by_name = True
