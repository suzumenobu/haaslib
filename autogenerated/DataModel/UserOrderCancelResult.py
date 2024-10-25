import dataclasses

@dataclasses.dataclass
class UserOrderCancelResult:
    IsCancelled: bool
    IsNotOpen: bool
    CancelFailed: bool
