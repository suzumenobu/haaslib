from typing import List, Optional, Any, Dict
from typing_extensions import Any
from pydantic import BaseModel, Field

class MarketPriceSummary(BaseModel):
    """Market price summary information"""
    change: float = Field(alias="Change")
    open: float = Field(alias="Open")
    high: float = Field(alias="High")
    low: float = Field(alias="Low")
    close: float = Field(alias="Close")
    volume: float = Field(alias="Volume")

    class Config:
        populate_by_name = True

class HaasChartTradeMarket(BaseModel):
    """Chart trade market information"""
    Unix: int
    Price: float
    Color: Any
    Text: str

class CloudMarket(BaseModel):
    """Cloud market information"""
    id: str = Field(alias="Id")
    name: str = Field(alias="Name")
    price_source: str = Field(alias="PriceSource")
    base_currency: str = Field(alias="BaseCurrency")
    quote_currency: str = Field(alias="QuoteCurrency")
    enabled: bool = Field(alias="Enabled")
    description: Optional[str] = Field(alias="Description", default=None)
    primary: str = Field(alias="Primary")
    secondary: str = Field(alias="Secondary")
    contract_name: str = Field(alias="ContractName")
    short_name: str = Field(alias="ShortName")
    wallet_tag: str = Field(alias="WalletTag")

    def as_market_tag(self) -> str:
        """Convert to market tag format"""
        return f"{self.price_source}_{self.base_currency}_{self.quote_currency}_SPOT"

    class Config:
        populate_by_name = True

# Add alias for backward compatibility
Market = CloudMarket  # This makes `Market` available when importing from this module

class MarketList(BaseModel):
    """Wrapper for list of markets response"""
    Success: bool
    Error: str
    Data: List[Market]

    class Config:
        populate_by_name = True

class CloudTick(BaseModel):
    """Market tick data"""
    Timestamp: int
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float
    BuyPrice: float
    SellPrice: float

    class Config:
        from_attributes = True

class CloudTradeMarket(BaseModel):
    """Market trading information"""
    normalized_primary: str = Field(alias="NormalizedPrimary")
    normalized_secondary: str = Field(alias="NormalizedSecondary")
    normalized_margin_currency: str = Field(alias="NormalizedMarginCurrency")
    exchange_symbol: str = Field(alias="ExchangeSymbol")
    websocket_symbol: str = Field(alias="WebSocketSymbol")
    exchange_value: float = Field(alias="ExchangeValue")
    exchange_values: List[float] = Field(alias="ExchangeValues")
    price_step: float = Field(alias="PriceStep")
    price_decimals: int = Field(alias="PriceDecimals")
    amount_step: float = Field(alias="AmountStep")
    amount_decimals: int = Field(alias="AmountDecimals")
    price_decimal_type: str = Field(alias="PriceDecimalType")
    amount_decimal_type: str = Field(alias="AmountDecimalType")
    makers_fee: float = Field(alias="MakersFee")
    takers_fee: float = Field(alias="TakersFee")
    minimum_trade_amount: float = Field(alias="MinimumTradeAmount")
    minimum_trade_volume: float = Field(alias="MinimumTradeVolume")
    is_open: bool = Field(alias="IsOpen")
    is_margin: bool = Field(alias="IsMargin")
    contract_details: Optional[Any] = Field(alias="ContractDetails")
    margin_currency: str = Field(alias="MarginCurrency")
    amount_label: str = Field(alias="AmountLabel")
    profit_label: str = Field(alias="ProfitLabel")

    class Config:
        populate_by_name = True

class CloudLastTrade(BaseModel):
    """Last trade information"""
    Timestamp: int
    IsBuyOrder: bool
    Price: float
    Amount: float

class CloudTradeContract(BaseModel):
    """Trade contract information"""
    Type: str
    MarginCurrency: str
    DisplayName: str
    AmountLabel: str
    ProfitLabel: str
    ContractValue: float
    ContractValueCurrency: str
    SettlementDate: int
    LowestLeverage: float
    HighestLeverage: float

class MarketPriceInformation(BaseModel):
    """Market price information"""
    Timestamp: int
    Market: str
    Statistics: Any

class MarketTechnicalInformation(BaseModel):
    """Market technical information"""
    Timestamp: int
    Market: str
    TrendIndicators: List[Any]
    SideWaysIndicators: List[Any]

class HaasChartPricePlot(BaseModel):
    """Chart price plot information"""
    Market: str
    Interval: str
    Candles: List[Any]
    Colors: Any
    Style: str
    Side: str

class MarketIndicatorTable(BaseModel):
    """Market indicator information"""
    indicator_name: str = Field(alias="IndicatorName")
    intervals: List[str] = Field(alias="Intervals")
    rows: List[Any] = Field(alias="Rows")

    class Config:
        populate_by_name = True

class MarketListResponse(BaseModel):
    """Wrapper for list of markets response"""
    Success: bool
    Error: Optional[str] = None
    Data: Optional[List[Market]] = None

    class Config:
        populate_by_name = True

class Market(BaseModel):
    """Market data model with field aliases for shortened API response"""
    Id: str = Field(alias='I')
    Name: str = Field(alias='N')
    PriceSource: str = Field(alias='PS')
    BaseCurrency: str = Field(alias='P')
    QuoteCurrency: str = Field(alias='S')
    Enabled: bool = Field(alias='E', default=True)
    Connected: Optional[bool] = Field(alias='C', default=None)

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class PriceSource(BaseModel):
    name: str = Field(alias="Name")
    enabled: bool = Field(alias="Enabled")
    
    class Config:
        populate_by_name = True

class OrderBook(BaseModel):
    bids: List[Dict[str, float]] = Field(alias="Bids")
    asks: List[Dict[str, float]] = Field(alias="Asks")

    class Config:
        populate_by_name = True

class Trade(BaseModel):
    timestamp: int = Field(alias="Timestamp")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")
    type: str = Field(alias="Type")  # "BUY" or "SELL"

    class Config:
        populate_by_name = True

class Tick(BaseModel):
    timestamp: int = Field(alias="Timestamp")
    open: float = Field(alias="Open")
    high: float = Field(alias="High")
    low: float = Field(alias="Low")
    close: float = Field(alias="Close")
    volume: float = Field(alias="Volume")

    class Config:
        populate_by_name = True

class PriceSnapshot(BaseModel):
    market: str = Field(alias="Market")
    price: float = Field(alias="Price")
    timestamp: int = Field(alias="Timestamp")

    class Config:
        populate_by_name = True

class FiatConversion(BaseModel):
    """Dictionary of fiat currency conversion rates"""
    data: Dict[str, float] = Field(alias="Data")

    class Config:
        populate_by_name = True
