import dataclasses
from typing import Any

@dataclasses.dataclass
class UserAccount:
    UserId: str
    AccountId: str
    Name: str
    ExchangeCode: str
    ExchangeType: str
    Status: str
    IsSimulated: bool
    IsTestNet: bool
    IsPublic: bool
    PositionMode: str
    MarginSettings: Any
