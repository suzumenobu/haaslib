import dataclasses

@dataclasses.dataclass
class HaasScriptOlderVersion:
    Id: str
    ScriptId: str
    Version: str
    Created: int
    SourceCode: str
