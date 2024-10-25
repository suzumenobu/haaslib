import dataclasses
from typing import Any, List

@dataclasses.dataclass
class RuntimeOrdersReport:
    Filled: int
    PartiallyFilled: int
    Cancelled: int
    Failed: int
    Total: int
    AverageOpenTime: int
    LastCompletedOrder: Any
    ProfitableTrades: int
    LoosingTrades: int
    BiggestWin: float
    BiggestLoss: float
