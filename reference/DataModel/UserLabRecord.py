import dataclasses

@dataclasses.dataclass
class UserLabRecord:
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
