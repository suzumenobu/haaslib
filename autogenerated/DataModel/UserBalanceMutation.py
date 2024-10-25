import dataclasses

@dataclasses.dataclass
class UserBalanceMutation:
    Id: str
    UserId: str
    AccountId: str
    MutationId: str
    WalletId: str
    Currency: str
    Timestamp: int
    Type: str
    Amount: float
