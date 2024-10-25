import dataclasses

@dataclasses.dataclass
class HaasScriptItem:
    UserId: str
    ScriptId: str
    ScriptName: str
    ScriptDescription: str
    ScriptType: str
    ScriptStatus: str
    CommandName: str
    IsCommand: bool
    IsValid: bool
    CreatedUnix: int
    UpdatedUnix: int
