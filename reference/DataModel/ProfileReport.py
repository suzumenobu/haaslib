import dataclasses
from typing import Any

@dataclasses.dataclass
class ProfileReport:
    MergeCounter: int
    Properties: Any
    Settings: Any
    Profits: Any
    Orders: Any
    Performance: Any
    PerformancePerMarket: Any
