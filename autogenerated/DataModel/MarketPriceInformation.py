import dataclasses
from typing import Any

@dataclasses.dataclass
class MarketPriceInformation:
    Timestamp: int
    Market: str
    Statistics: Any
