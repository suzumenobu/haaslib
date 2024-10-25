from typing import List, Optional, Any
from typing_extensions import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .base import ApiResponse
from .market import MarketPriceSummary  # Move this class to market.py if it's used there

class CloudLastTrade(BaseModel):
    """Last trade information"""
    timestamp: int = Field(alias="Timestamp")
    is_buy_order: bool = Field(alias="IsBuyOrder")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")

    class Config:
        populate_by_name = True

class CloudTradeContract(BaseModel):
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

class MarketPriceInformation(BaseModel):
    """CloudMarket price information with timestamp"""
    timestamp: int = Field(..., alias="Timestamp")
    market: str = Field(..., alias="CloudMarket")
    statistics: MarketPriceSummary = Field(..., alias="Statistics")

    class Config:
        populate_by_name = True

class MarketInformation(BaseModel):
    """Detailed market information"""
    price_source: Optional[str] = Field(None, alias="PriceSource")
    base_currency: Optional[str] = Field(None, alias="BaseCurrency")
    quote_currency: Optional[str] = Field(None, alias="QuoteCurrency")
    contract_name: Optional[str] = Field(None, alias="ContractName")
    enabled: Optional[bool] = Field(None, alias="Enabled")
    last_price: Optional[float] = Field(None, alias="LastPrice")
    volume_24h: Optional[float] = Field(None, alias="Volume24H")
    price_summary: Optional[MarketPriceSummary] = Field(None, alias="PriceSummary")

    class Config:
        populate_by_name = True

class MarketPrice(BaseModel):
    """Market price data"""
    timestamp: int = Field(..., alias="T")
    open: float = Field(..., alias="O")
    high: float = Field(..., alias="H")
    low: float = Field(..., alias="L")
    close: float = Field(..., alias="C")
    volume: float = Field(..., alias="V")
    bid: float = Field(..., alias="B")
    ask: float = Field(..., alias="A")
    spread: float = Field(..., alias="S")

    class Config:
        populate_by_name = True

class CloudMarket(BaseModel):
    """CloudMarket data model with field aliases for shortened API response"""
    price_source: str = Field(alias='PS')
    base_currency: str = Field(alias='P')
    quote_currency: str = Field(alias='S')
    contract_name: Optional[str] = Field(alias='C', default='')
    enabled: bool = Field(default=True)
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class MarketListResponse(BaseModel):
    """Wrapper for list of markets response"""
    Success: bool
    Error: Optional[str] = None
    Data: Optional[List[CloudMarket]] = None

    class Config:
        populate_by_name = True

class MarketPriceResponse(ApiResponse):
    """Response wrapper for market price data"""
    Data: Optional[MarketPrice] = None
    Success: bool
    Error: Optional[str] = None

    class Config:
        populate_by_name = True

class CloudTradeMarket(BaseModel):
    """Trade market details from the API"""
    normalized_primary: str = Field(..., alias="NormalizedPrimary")
    normalized_secondary: str = Field(..., alias="NormalizedSecondary")
    normalized_margin_currency: str = Field(..., alias="NormalizedMarginCurrency")
    exchange_symbol: str = Field(..., alias="ExchangeSymbol")
    websocket_symbol: str = Field(..., alias="WebSocketSymbol")
    exchange_value: float = Field(..., alias="ExchangeValue")
    exchange_values: List[float] = Field(..., alias="ExchangeValues")
    price_step: float = Field(..., alias="PriceStep")
    price_decimals: int = Field(..., alias="PriceDecimals")
    amount_step: float = Field(..., alias="AmountStep")
    amount_decimals: int = Field(..., alias="AmountDecimals")
    price_decimal_type: str = Field(..., alias="PriceDecimalType")
    amount_decimal_type: str = Field(..., alias="AmountDecimalType")
    makers_fee: float = Field(..., alias="MakersFee")
    takers_fee: float = Field(..., alias="TakersFee")
    minimum_trade_amount: float = Field(..., alias="MinimumTradeAmount")
    minimum_trade_volume: float = Field(..., alias="MinimumTradeVolume")
    is_open: bool = Field(..., alias="IsOpen")
    is_margin: bool = Field(..., alias="IsMargin")
    contract_details: Optional[CloudTradeContract] = Field(None, alias="ContractDetails")
    margin_currency: str = Field(..., alias="MarginCurrency")
    amount_label: str = Field(..., alias="AmountLabel")
    profit_label: str = Field(..., alias="ProfitLabel")
    price_source: str = Field(..., alias="PriceSource")
    primary: str = Field(..., alias="Primary")
    secondary: str = Field(..., alias="Secondary")
    contract_name: str = Field(..., alias="ContractName")
    short_name: str = Field(..., alias="ShortName")
    wallet_tag: str = Field(..., alias="WalletTag")

    class Config:
        populate_by_name = True

class CloudTradeMarketResponse(ApiResponse):
    """Response wrapper for trade market data"""
    Data: Optional[List[CloudTradeMarket]] = None
    Success: bool
    Error: Optional[str] = None

    class Config:
        populate_by_name = True
