import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasChartContainer:
    Guid: str
    Interval: str
    Status: str
    Charts: List[Any]
    Colors: Any
