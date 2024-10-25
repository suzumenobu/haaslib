import dataclasses

@dataclasses.dataclass
class MarketPriceSummary:
    Change: float
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float
