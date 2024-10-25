import dataclasses
from typing import Any, List

@dataclasses.dataclass
class UserLabParameter:
    Key: str
    Type: str
    Options: List[Any]
    IsEnabled: bool
    IsSpecific: bool
