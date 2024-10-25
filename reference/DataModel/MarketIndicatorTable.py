import dataclasses
from typing import Any, List

@dataclasses.dataclass
class MarketIndicatorTable:
    IndicatorName: str
    Intervals: List[str]
    Rows: List[Any]
