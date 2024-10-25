import dataclasses
from typing import Any

@dataclasses.dataclass
class CloudTradeContract:
    Type: str
    MarginCurrency: str
    DisplayName: str
    AmountLabel: str
    ProfitLabel: str
    ContractValue: float
    ContractValueCurrency: str
    SettlementDate: int
    LowestLeverage: float
    HighestLeverage: float
