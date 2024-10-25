import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasChartTradeMarket:
    Unix: int
    Price: float
    Color: Any
    Text: str
