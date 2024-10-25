import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasChartShapes:
    Type: str
    AboveCandle: bool
    TextColor: Any
    Color: Any
    Text: str
    Size: int
