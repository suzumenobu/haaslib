import dataclasses

@dataclasses.dataclass
class UserBalanceItem:
    Currency: str
    WalletId: str
    Available: float
    Total: float
