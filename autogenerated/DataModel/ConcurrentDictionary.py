import dataclasses
from typing import Any, List

@dataclasses.dataclass
class ConcurrentDictionary:
    Item: Any
    IsEmpty: bool
    Keys: List[Any]
    Values: List[Any]
