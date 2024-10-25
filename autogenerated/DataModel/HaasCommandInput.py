import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasCommandInput:
    Index: int
    Name: str
    Type: str
    IsRequired: bool
    IsHidden: bool
    IsField: bool
    AllowNull: bool
    Description: str
    DefaultStorage: Any
    Suggestion: Any
