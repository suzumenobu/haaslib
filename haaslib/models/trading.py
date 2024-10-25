from typing import Optional, List
from pydantic import Field
from .base import BaseModel

class Order(BaseModel):
    account_id: str = Field(alias="AccountId")
    order_id: Optional[str] = Field(alias="OrderId", default=None)
    market: str = Field(alias="Market")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")
    type: str = Field(alias="Type")  # "BUY" or "SELL"
    status: Optional[str] = Field(alias="Status", default=None)
    timestamp: Optional[int] = Field(alias="Timestamp", default=None)
    
    class Config:
        populate_by_name = True

class Position(BaseModel):
    account_id: str = Field(alias="AccountId")
    position_id: str = Field(alias="PositionId")
    market: str = Field(alias="Market")
    entry_price: float = Field(alias="EntryPrice")
    current_price: float = Field(alias="CurrentPrice")
    amount: float = Field(alias="Amount")
    leverage: float = Field(alias="Leverage")
    liquidation_price: Optional[float] = Field(alias="LiquidationPrice")
    unrealized_pnl: float = Field(alias="UnrealizedPnl")
    
    class Config:
        populate_by_name = True

class MarginSettings(BaseModel):
    driver_name: str = Field(alias="DriverName")
    driver_type: str = Field(alias="DriverType")
    market: str = Field(alias="Market")
    leverage: float = Field(alias="Leverage")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")
    
    class Config:
        populate_by_name = True

class MaxAmountRequest(BaseModel):
    account_id: str = Field(alias="AccountId")
    market: str = Field(alias="Market")
    price: float = Field(alias="Price")
    used_amount: float = Field(alias="UsedAmount")
    amount_percentage: float = Field(alias="AmountPercentage")
    is_buy: bool = Field(alias="IsBuy")
    
    class Config:
        populate_by_name = True

class MaxAmountResponse(BaseModel):
    max_amount: float = Field(alias="MaxAmount")
    max_price: float = Field(alias="MaxPrice")
    used_margin: float = Field(alias="UsedMargin")
    
    class Config:
        populate_by_name = True

class CancelOrdersRequest(BaseModel):
    account_id: Optional[str] = Field(alias="AccountId", default=None)
    market: Optional[str] = Field(alias="Market", default=None)
    
    class Config:
        populate_by_name = True

class Trade(BaseModel):
    account_id: str = Field(alias="AccountId")
    trade_id: str = Field(alias="TradeId")
    market: str = Field(alias="Market")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")
    type: str = Field(alias="Type")  # "BUY" or "SELL"
    timestamp: int = Field(alias="Timestamp")
    fee: Optional[float] = Field(alias="Fee")
    fee_currency: Optional[str] = Field(alias="FeeCurrency")
    
    class Config:
        populate_by_name = True
