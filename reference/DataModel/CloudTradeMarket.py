import dataclasses
from typing import Any, List

@dataclasses.dataclass
class CloudTradeMarket:
    NormalizedPrimary: str
    NormalizedSecondary: str
    NormalizedMarginCurrency: str
    ExchangeSymbol: str
    WebSocketSymbol: str
    ExchangeValue: float
    ExchangeValues: List[float]
    PriceStep: float
    PriceDecimals: int
    AmountStep: float
    AmountDecimals: int
    PriceDecimalType: str
    AmountDecimalType: str
    MakersFee: float
    TakersFee: float
    MinimumTradeAmount: float
    MinimumTradeVolume: float
    IsOpen: bool
    IsMargin: bool
    ContractDetails: Any
    MarginCurrency: str
    AmountLabel: str
    ProfitLabel: str
    PriceSource: str
    Primary: str
    Secondary: str
    ContractName: str
    ShortName: str
    WalletTag: str
