from typing import Optional
from pydantic import BaseModel, Field

class UserTrade(BaseModel):
    """User trade information"""
    user_id: str = Field(alias="UserId")
    account_id: str = Field(alias="AccountId")
    trade_id: str = Field(alias="TradeId")
    order_id: str = Field(alias="OrderId")
    unix: int = Field(alias="Unix")
    type: str = Field(alias="Type")
    market: str = Field(alias="Market")
    direction: str = Field(alias="Direction")
    trade_price: float = Field(alias="TradePrice")
    trade_amount: float = Field(alias="TradeAmount")
    fee_costs: float = Field(alias="FeeCosts")
    fee_currency: str = Field(alias="FeeCurrency")
    notes: str = Field(alias="Notes")
    search_tag: str = Field(alias="SearchTag")

    class Config:
        populate_by_name = True
