import dataclasses
from typing import Any

@dataclasses.dataclass
class RuntimeReport:
    AccountId: str
    CloudMarket: str
    AmountLabel: str
    MarginLabel: str
    ProfitLabel: str
    Fees: Any
    Profits: Any
    Orders: Any
    Positions: Any
    Performance: Any
