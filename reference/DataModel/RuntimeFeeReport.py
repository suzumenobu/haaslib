import dataclasses
from typing import Any, Dict

@dataclasses.dataclass
class RuntimeFeeReport:
    FeeCost: float
    FeeRebate: float
    TotalFeeCosts: float
    FeesPerCurrency: Dict[str, float]
