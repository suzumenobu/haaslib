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
    """Market information"""
    price_source: str = Field(alias="PriceSource")
    primary: str = Field(alias="Primary")
    secondary: str = Field(alias="Secondary")
    contract_name: str = Field(alias="ContractName")
    short_name: str = Field(alias="ShortName")
    wallet_tag: str = Field(alias="WalletTag")

    class Config:
        populate_by_name = True
