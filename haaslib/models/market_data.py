from typing import List
from typing_extensions import Optional
from pydantic import BaseModel, Field

class CloudLastTrade(BaseModel):
    """Last trade information"""
    timestamp: int = Field(alias="Timestamp")
    is_buy_order: bool = Field(alias="IsBuyOrder")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")

    class Config:
        populate_by_name = True

class CloudTradeContract(BaseModel):
    """Trade contract information"""
    type: str = Field(alias="Type")
    margin_currency: str = Field(alias="MarginCurrency")
    display_name: str = Field(alias="DisplayName")
    amount_label: str = Field(alias="AmountLabel")
    profit_label: str = Field(alias="ProfitLabel")
    contract_value: float = Field(alias="ContractValue")
    contract_value_currency: str = Field(alias="ContractValueCurrency")
    settlement_date: int = Field(alias="SettlementDate")
    lowest_leverage: float = Field(alias="LowestLeverage")
    highest_leverage: float = Field(alias="HighestLeverage")

    class Config:
        populate_by_name = True

class MarketInformation(BaseModel):
    """Market information with optional fields"""
    price_source: Optional[str] = Field(None, alias="PriceSource")
    primary: Optional[str] = Field(None, alias="Primary")
    secondary: Optional[str] = Field(None, alias="Secondary")
    contract_name: Optional[str] = Field(None, alias="ContractName")
    short_name: Optional[str] = Field(None, alias="ShortName")
    wallet_tag: Optional[str] = Field(None, alias="WalletTag")
    
    # Remove leading underscores from field names
    price_source_alt: Optional[str] = Field(None, alias="PS")
    primary_alt: Optional[str] = Field(None, alias="P")
    secondary_alt: Optional[str] = Field(None, alias="S")
    contract_name_alt: Optional[str] = Field(None, alias="C")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    def __init__(self, **data):
        # Handle both full and shortened field names
        if "PS" in data and "PriceSource" not in data:
            data["PriceSource"] = data["PS"]
        if "P" in data and "Primary" not in data:
            data["Primary"] = data["P"]
        if "S" in data and "Secondary" not in data:
            data["Secondary"] = data["S"]
        if "C" in data and "ContractName" not in data:
            data["ContractName"] = data["C"]
        super().__init__(**data)

class Market(BaseModel):
    """Market data model with field aliases for shortened API response"""
    price_source: str = Field(alias='PS')
    base_currency: str = Field(alias='P')
    quote_currency: str = Field(alias='S')
    contract_name: Optional[str] = Field(alias='C', default='')
    enabled: bool = Field(default=True)
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class MarketListResponse(BaseModel):
    """Wrapper for list of markets response"""
    Success: bool
    Error: Optional[str] = None
    Data: Optional[List[Market]] = None

    class Config:
        populate_by_name = True
