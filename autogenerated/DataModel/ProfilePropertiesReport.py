import dataclasses

@dataclasses.dataclass
class ProfilePropertiesReport:
    HideTradeAmount: bool
    HideOrderTemplate: bool
    IsSpotSupported: bool
    IsMarginSupported: bool
    IsLeverageSupported: bool
    IsManagedTrading: bool
    IsOneDirection: bool
    IsMultiMarket: bool
    IsRemoteSignalBased: bool
    IsTAUsed: bool
