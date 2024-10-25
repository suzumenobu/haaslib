import dataclasses
from typing import Any, List

@dataclasses.dataclass
class RuntimePosition:
    PositionGuid: str
    PositionId: str
    AccountId: str
    Market: str
    Leverage: float
    Direction: str
    MarketType: str
    ProfitLabel: str
    AmountLabel: str
    PriceDecimals: int
    AmountDecimals: int
    OpenTime: int
    CloseTime: int
    IsClosed: bool
    AveragePrice: float
    Total: float
    Available: float
    InOrder: float
    EnterOrders: List[Any]
    ExitOrders: List[Any]
    CurrentPrice: float
    FeeCosts: float
    RealizedProfits: float
    UnrealizedProfits: float
    ROI: float
    HighestPointInProfit: float
    LowestPointInProfit: float
    IsSet: bool
    Peak: float
    Trough: float
    MaxDrawDown: float
