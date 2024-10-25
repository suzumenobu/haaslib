import dataclasses
from typing import Any

@dataclasses.dataclass
class AppLoginResult:
    IsSuccess: bool
    Error: str
    Details: Any
