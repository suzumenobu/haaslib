import dataclasses

@dataclasses.dataclass
class UserOrder:
    Unix: int
    OrderId: str
    StopOrderId: str
    Market: str
    Direction: str
    Type: str
    OrderPrice: float
    TriggerPrice: float
    OrderAmount: float
    TradeAmount: float
    Status: str
    BotId: str
    Notes: str
