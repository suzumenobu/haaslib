import dataclasses
from typing import Any

@dataclasses.dataclass
class CloudOrderbook:
    Ask: Any
    Bid: Any
