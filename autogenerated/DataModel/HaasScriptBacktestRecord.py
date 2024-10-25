import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasScriptBacktestRecord:
    RecordId: str
    Unix: int
    UserId: str
    BacktestId: str
    BacktestStart: int
    BacktestEnd: int
    BacktestTag: str
    ExecutionStart: int
    ExecutionEnd: int
    ScriptTag: str
    AccountTag: str
    MarketTag: str
    ProfitTags: List[Any]
    ROITags: List[Any]
    IsArchived: bool
    Runtime: Any
    Chart: Any
    Logs: List[Any]
