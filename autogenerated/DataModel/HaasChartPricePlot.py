import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasChartPricePlot:
    Market: str
    Interval: str
    Candles: List[Any]
    Colors: Any
    Style: str
    Side: str
