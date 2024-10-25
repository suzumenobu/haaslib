import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasScriptItemWithDependencies:
    Dependencies: List[str]
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
