import dataclasses

@dataclasses.dataclass
class RuntimeProfitReport:
    StartPrice: float
    StartBalance: float
    PriceChange: float
    BalanceChange: float
    GrossProfits: float
    RealizedProfits: float
    UnrealizedProfits: float
    ReturnOnInvestment: float
    RoiMargin: float
    CustomRoiMargin: float
