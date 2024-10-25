import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserLabsBacktestResult:
    RecordId: str
    UserId: str
    LabId: str
    BacktestId: str
    NoGeneration: int
    NoPopulation: int
    Status: str
    Settings: Any
    Parameters: Any
    Runtime: Any
    Chart: Any
    Logs: List[Any]
    Summary: Any
    ServiceId: str
    IsElite: bool
