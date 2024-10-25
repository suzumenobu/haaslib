from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from .base import ApiResponse
from datetime import datetime

class PriceSource(str, Enum):
    """Supported price sources"""
    BINANCE = "BINANCE"
    BINANCE_FUTURES = "BINANCE_FUTURES"
    BINANCE_US = "BINANCE_US"
    BITFINEX = "BITFINEX"
    BITMEX = "BITMEX"
    BYBIT = "BYBIT"
    COINBASE = "COINBASE"
    HUOBI = "HUOBI"
    KRAKEN = "KRAKEN"
    KUCOIN = "KUCOIN"
    OKEX = "OKEX"

class OrderBookEntry(BaseModel):
    """Single order book entry with price and amount"""
    price: float
    amount: float

class OrderBook(BaseModel):
    """Order book with bids and asks"""
    bids: List[OrderBookEntry]
    asks: List[OrderBookEntry]
    timestamp: Optional[int] = None

    class Config:
        populate_by_name = True

class MarketPriceSummary(BaseModel):
    """CloudMarket price summary statistics"""
    change: float = Field(..., alias="Change")
    open: float = Field(..., alias="Open")
    high: float = Field(..., alias="High")
    low: float = Field(..., alias="Low")
    close: float = Field(..., alias="Close")
    volume: float = Field(..., alias="Volume")

    class Config:
        populate_by_name = True

class Market(BaseModel):
    """Basic market information"""
    price_source: str
    base_currency: str
    quote_currency: str
    enabled: bool = True

class CloudMarket(Market):
    """Extended market information from cloud API"""
    market_id: str
    market_name: str
    market_type: str
    price_precision: int
    volume_precision: int
    min_volume: float
    max_volume: float
    min_price: float
    max_price: float
    maker_fee: float
    taker_fee: float
    is_spot: bool = True
    is_margin: bool = False
    is_futures: bool = False

class MarketListResponse(ApiResponse):
    """Response wrapper for market list"""
    Data: Optional[List[CloudMarket]] = None

# Trade-specific models
class LastTrade(BaseModel):
    """Last trade information"""
    timestamp: int = Field(alias="Timestamp")
    is_buy_order: bool = Field(alias="IsBuyOrder")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")

    class Config:
        populate_by_name = True

class TradeContract(BaseModel):
    """Trade contract information"""
    type: str = Field(alias="Type")
    margin_currency: str = Field(alias="MarginCurrency")
    display_name: str = Field(alias="DisplayName")
    amount_label: str = Field(alias="AmountLabel")
    profit_label: str = Field(alias="ProfitLabel")
    contract_value: float = Field(alias="ContractValue")
    contract_value_currency: str = Field(alias="ContractValueCurrency")
    settlement_date: int = Field(alias="SettlementDate")
    lowest_leverage: float = Field(alias="LowestLeverage")
    highest_leverage: float = Field(alias="HighestLeverage")

    class Config:
        populate_by_name = True

class Trade(BaseModel):
    """Trade information"""
    trade_id: str = Field(alias="TradeId")
    order_id: str = Field(alias="OrderId")
    timestamp: int = Field(alias="Timestamp")
    type: str = Field(alias="Type")
    market: str = Field(alias="CloudMarket")
    direction: str = Field(alias="Direction")
    trade_price: float = Field(alias="TradePrice")
    trade_amount: float = Field(alias="TradeAmount")
    fee_costs: float = Field(alias="FeeCosts")
    fee_currency: str = Field(alias="FeeCurrency")
    notes: Optional[str] = Field(alias="Notes", default="")
    search_tag: Optional[str] = Field(alias="SearchTag", default="")

    class Config:
        populate_by_name = True

class Tick(BaseModel):
    """CloudMarket tick data"""
    timestamp: int = Field(alias="Timestamp")
    open: float = Field(alias="Open")
    high: float = Field(alias="High")
    low: float = Field(alias="Low")
    close: float = Field(alias="Close")
    volume: float = Field(alias="Volume")
    buy_price: float = Field(alias="BuyPrice")
    sell_price: float = Field(alias="SellPrice")

    class Config:
        populate_by_name = True

class PriceSourceDetail(BaseModel):
    """Detailed price source information"""
    full_name: str = Field(..., alias="F")
    friendly_name: str = Field(..., alias="FN")
    description: Optional[str] = Field(None, alias="D")
    enabled: bool = Field(..., alias="E")
    login_required: bool = Field(False, alias="LR")
    is_beta: bool = Field(False, alias="IBD")

    class Config:
        populate_by_name = True

class PriceSourceDetailResponse(ApiResponse):
    """Response wrapper for price source details"""
    Data: Optional[List[PriceSourceDetail]] = None
