import dataclasses
from typing import List, Any

@dataclasses.dataclass
class HaasChartAxis:
    Type: str
    Side: str
    IsVisible: bool
    Labels: List[Any]
