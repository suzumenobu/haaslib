import dataclasses
from typing import Any

@dataclasses.dataclass
class MarketPriceInformation:
    Timestamp: int
    CloudMarket: str
    Statistics: Any
