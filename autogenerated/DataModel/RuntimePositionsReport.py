import dataclasses
from typing import Any, List

@dataclasses.dataclass
class RuntimePositionsReport:
    ClosedPositions: int
    WinningPositions: int
    AverageProfits: float
    AveragePositionSize: float
    AveragePositionMargin: float
    TotalEnterMargin: float
    AverageWin: float
    BiggestWin: float
    TotalWin: float
    AverageLoss: float
    BiggestLoss: float
    TotalLoss: float
    ProfitHistory: List[Any]
