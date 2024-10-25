import dataclasses
from typing import List, Any

@dataclasses.dataclass
class HaasChartAnnotations:
    Name: str
    Type: str
    Decoration: str
    Side: str
    Colors: List[Any]
    Values: List[Any]
    Timestamps: List[int]
