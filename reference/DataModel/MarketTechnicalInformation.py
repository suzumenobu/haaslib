import dataclasses
from typing import Any, List

@dataclasses.dataclass
class MarketTechnicalInformation:
    Timestamp: int
    CloudMarket: str
    TrendIndicators: List[Any]
    SideWaysIndicators: List[Any]
