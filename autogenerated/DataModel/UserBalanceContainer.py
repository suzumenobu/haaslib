import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserBalanceContainer:
    AccountId: str
    Items: List[Any]
