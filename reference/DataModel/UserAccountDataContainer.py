import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserAccountDataContainer:
    Balances: List[Any]
    Orders: List[Any]
    Positions: List[Any]
