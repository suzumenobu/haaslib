import dataclasses
from typing import Any

@dataclasses.dataclass
class CloudPriceSource:
    ExchangeFamily: str
    ExchangeName: str
    ExchangeCode: str
    IsTestNet: bool
    SpotTrading: bool
    MarginTrading: bool
    LeverageTrading: bool
    HasTestNetSupport: bool
    PublicKeyLabel: str
    SecretKeyLabel: str
    AdditionalFieldLabel: str
    Location: str
    FoundedYear: int
    AffiliationLink: str
    Website: str
    Email: str
    Twitter: str
    Telegram: str
    Facebook: str
    Discord: str
    GitBookApi: str
    Rating: float
    IsForexDriver: bool
    IsLoginRequired: bool
    IsBetaDriver: bool
