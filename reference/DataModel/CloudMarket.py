import dataclasses

@dataclasses.dataclass
class CloudMarket:
    PriceSource: str
    Primary: str
    Secondary: str
    ContractName: str
    ShortName: str
    WalletTag: str
