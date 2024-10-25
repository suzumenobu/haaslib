import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasBot:
    UserId: str
    BotId: str
    BotName: str
    ScriptId: str
    ScriptVersion: str
    AccountId: str
    CloudMarket: str
    ExecutionId: str
    IsActivated: bool
    IsPaused: bool
    IsFavorite: bool
    Notes: str
    ScriptNote: str
    NotesTimestamp: int
    RealizedProfit: float
    UnrealizedProfit: float
    ReturnOnInvestment: float
    TradeAmountError: str
    AccountError: str
    ScriptError: str
    UpdateCounter: int
    ChartInterval: str
    ChartStyle: str
    ChartVolume: bool
    Runtime: Any
    ScriptPackage: Any
