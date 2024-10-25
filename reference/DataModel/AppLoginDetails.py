import dataclasses
from typing import Any

@dataclasses.dataclass
class AppLoginDetails:
    UserId: str
    InterfaceSecret: str
    LicenseDetails: Any
