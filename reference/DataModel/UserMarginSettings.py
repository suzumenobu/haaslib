import dataclasses

@dataclasses.dataclass
class UserMarginSettings:
    LongLeverage: float
    ShortLeverage: float
    MarginMode: str
