import dataclasses
from typing import List, Any

@dataclasses.dataclass
class UserOrderExecutionRequest:
    RequestId: str
    UserId: str
    AccountId: str
    BotId: str
    CloudMarket: str
    Type: str
    Direction: str
    OrderPrice: float
    TriggerPrice: float
    TriggerPriceType: str
    Amount: float
    PostOnly: bool
    ReduceOnly: bool
    HiddenOrder: bool
    TimeInForce: str
    Notes: str
    IsMarketOrder: bool
