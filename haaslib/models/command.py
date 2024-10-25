from typing import Any, List
from pydantic import BaseModel

class HaasCommandBase(BaseModel):
    """Base command model for Haas commands"""
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

    class Config:
        from_attributes = True

class HaasScriptCommandRecord(BaseModel):
    """Script command record"""
    CommandName: str
    CommandDescription: str
    IsManagedTrading: bool
    IsUnmanagedSpot: bool
    IsUnmanagedLeverage: bool
    HasOrderHandling: bool
    Parameters: List[Any]
    Output: Any
    OutputIndex: int
