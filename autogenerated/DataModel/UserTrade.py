import dataclasses

@dataclasses.dataclass
class UserTrade:
    UserId: str
    AccountId: str
    TradeId: str
    OrderId: str
    Unix: int
    Type: str
    Market: str
    Direction: str
    TradePrice: float
    TradeAmount: float
    FeeCosts: float
    FeeCurrency: str
    Notes: str
    SearchTag: str
