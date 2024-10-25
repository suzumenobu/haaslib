import dataclasses

@dataclasses.dataclass
class ProfilePerformanceReport:
    SharpeRatio: float
    SortinoRatio: float
    WinPercentage: float
    ProfitFactor: float
    CPCIndex: float
    TailRatio: float
    CommonSenseRatio: float
    ProfitMarginRatio: float
