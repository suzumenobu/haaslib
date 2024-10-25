import dataclasses
from typing import Any

@dataclasses.dataclass
class RuntimeReport:
    AccountId: str
    Market: str
    AmountLabel: str
    MarginLabel: str
    ProfitLabel: str
    Fees: Any
    Profits: Any
    Orders: Any
    Positions: Any
    Performance: Any
