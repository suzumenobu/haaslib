import dataclasses

@dataclasses.dataclass
class VisualScriptCompileError:
    CommandGuid: str
    InputGuid: str
