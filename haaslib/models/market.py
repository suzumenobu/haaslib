from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field

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

class Market(BaseModel):
    """Market data model with field aliases for shortened API response"""
    price_source: str = Field(alias='PS')
    base_currency: str = Field(alias='P')
    quote_currency: str = Field(alias='S')
    contract_name: Optional[str] = Field(alias='C', default='')
    enabled: bool = Field(default=True)
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    @property
    def market_name(self) -> str:
        """Generate market name in format: PRICESOURCE_BASE_QUOTE"""
        return f"{self.price_source}_{self.base_currency}_{self.quote_currency}"

class MarketListResponse(BaseModel):
    """Wrapper for list of markets response"""
    Success: bool
    Error: Optional[str] = None
    Data: Optional[List[Market]] = None

    class Config:
        populate_by_name = True

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
    market: str = Field(alias="Market")
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
    """Market tick data"""
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
