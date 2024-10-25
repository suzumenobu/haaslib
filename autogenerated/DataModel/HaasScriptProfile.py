import dataclasses
from typing import Any

@dataclasses.dataclass
class HaasScriptProfile:
    ScriptId: str
    PublicRating: float
    Details: Any
    ScriptName: str
    ScriptDescription: str
    UserId: str
    UserName: str
    ScriptStatus: str
