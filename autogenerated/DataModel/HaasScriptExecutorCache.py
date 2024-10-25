import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasScriptExecutorCache:
    Unix: int
    Interval: str
    Value: Any
