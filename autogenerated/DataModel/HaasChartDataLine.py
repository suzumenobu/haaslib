import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasChartDataLine:
    Guid: str
    Name: str
    Interval: str
    Visible: bool
    Behind: bool
    IgnoreOnAxis: bool
    Color: Any
    Width: int
    Type: str
    Style: str
    Decoration: str
    Side: str
    FixedValue: float
    DataPoints: List[Any]
    DataSets: List[Any]
    ConnectedLines: bool
