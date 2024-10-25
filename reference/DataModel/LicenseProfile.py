import dataclasses
from typing import List, Any

@dataclasses.dataclass
class LicenseProfile:
    LicenseName: str
    ValidUntill: int
    Rights: List[Any]
    Enterprise: bool
    AllowedExchanges: List[Any]
    MaxBots: int
    MaxSimulatedAccounts: int
    MaxRealAccounts: int
    MaxDashboards: int
    MaxBacktestMonths: int
    RentedSignals: List[Any]
    RentedStrategies: List[Any]
    HireSignalsEnabled: bool
    HireStrategiesEnabled: bool
    HaasLabsEnabled: bool
    ResellSignalsEnabled: bool
    MarketDetailsEnabled: bool
    LocalAPIEnabled: bool
    ScriptedExchangesEnabled: bool
    MachinelearningEnabled: bool
