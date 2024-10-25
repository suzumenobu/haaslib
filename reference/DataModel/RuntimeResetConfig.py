import dataclasses

@dataclasses.dataclass
class RuntimeResetConfig:
    ResetLogs: bool
    ResetReports: bool
    ResetPositions: bool
    ResetChart: bool
