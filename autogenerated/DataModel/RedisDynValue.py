import dataclasses
from typing import Any

@dataclasses.dataclass
class RedisDynValue:
    UserDataType: str
    Data: Any
    Unix: int
