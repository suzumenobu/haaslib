import dataclasses
from typing import Any, List

@dataclasses.dataclass
class RuntimeCustomReport:
    Comparer: Any
    Keys: List[Any]
    Values: List[Any]
    Item: Any
