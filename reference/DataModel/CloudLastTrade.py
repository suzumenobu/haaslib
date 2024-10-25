import dataclasses

@dataclasses.dataclass
class CloudLastTrade:
    Timestamp: int
    IsBuyOrder: bool
    Price: float
    Amount: float
