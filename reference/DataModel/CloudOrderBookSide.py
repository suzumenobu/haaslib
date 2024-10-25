import dataclasses

@dataclasses.dataclass
class CloudOrderBookSide:
    Price: float
    Amount: float
