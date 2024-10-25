import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasScriptCommandRecord:
    CommandName: str
    CommandDescription: str
    IsManagedTrading: bool
    IsUnmanagedSpot: bool
    IsUnmanagedLeverage: bool
    HasOrderHandling: bool
    Parameters: List[Any]
    Output: Any
    OutputIndex: int
