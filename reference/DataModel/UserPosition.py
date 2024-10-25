import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserPosition:
    PositionId: str
    Direction: str
    CloudMarket: str
    Leverage: float
    MarginMode: str
    Price: float
    Amount: float
    Margin: float
    ProfitLoss: float
    ProfitLossRatio: float
    LiquidationPrice: float
