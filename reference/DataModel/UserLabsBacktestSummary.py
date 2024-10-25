import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserLabsBacktestSummary:
    Orders: Any
    Trades: Any
    Positions: Any
    FeeCosts: float
    RealizedProfits: float
    ReturnOnInvestment: float
    CustomReport: Any
