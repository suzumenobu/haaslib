import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasScriptRecord:
    SourceCode: str
    CompileResult: Any
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
