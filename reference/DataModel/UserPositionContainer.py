import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserPositionContainer:
    AccountId: str
    Items: List[Any]
