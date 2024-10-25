import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasCommandBase:
    CommandName: str
    Command: str
    CommandType: str
    Category: str
    Description: str
    ReturnDescription: str
    Parameters: List[Any]
    OutputIndex: int
    IsConstant: bool
    IsPrimary: bool
    RequiresCall: bool
    Resizable: bool
    OutputHidden: bool
    OutputType: str
    OutputSuggestions: List[Any]
    ChangeTypes: List[Any]
    ExecutionTimes: List[int]
