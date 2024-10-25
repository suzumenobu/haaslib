import dataclasses
from typing import Any, List

@dataclasses.dataclass
class HaasScriptExecutionPackage:
    ScriptId: str
    ScriptName: str
    ScriptType: str
    IsCommand: bool
    CommandName: str
    SourceCode: str
    Commands: List[Any]
