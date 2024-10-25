import dataclasses
from typing import Any, Dict

@dataclasses.dataclass
class UserLabDetails:
    Config: Any
    Settings: Any
    Parameters: Dict[str, Any]
    UserId: str
    LabId: str
    ScriptId: str
    Name: str
    Type: str
    Status: str
    ScheduledBacktests: int
    CompletedBacktests: int
    CreatedAt: int
    UpdatedAt: int
    StartedAt: int
    RunningSince: int
    StartUnix: int
    EndUnix: int
