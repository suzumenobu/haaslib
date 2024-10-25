import dataclasses

@dataclasses.dataclass
class RuntimePerformanceReport:
    SharpeRatio: float
    SortinoRatio: float
    WinPercentage: float
    WinLossPercentage: float
    ProfitFactor: float
    CPCIndex: float
    TailRatio: float
    CommonSenseRatio: float
    OutlierWinRatio: float
    OutlierLossRatio: float
    ProfitMarginRatio: float
    BiggestWin: float
    BiggestLoss: float
    HighestPointInProfit: float
    LowestPointInProfit: float
    TotalMarginUsed: float
    IsSet: bool
    Peak: float
    Trough: float
    MaxDrawDown: float
