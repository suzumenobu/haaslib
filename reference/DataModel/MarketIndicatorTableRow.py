import dataclasses
from typing import Any, List

@dataclasses.dataclass
class MarketIndicatorTableRow:
    Settings: Any
    Values: List[Any]
