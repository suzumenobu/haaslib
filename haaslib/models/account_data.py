from typing import Any, List
from pydantic import BaseModel, Field

class UserAccountDataContainer(BaseModel):
    """Container for user account data"""
    balances: List[Any] = Field(alias="Balances")
    orders: List[Any] = Field(alias="Orders")
    positions: List[Any] = Field(alias="Positions")

    class Config:
        populate_by_name = True

class UserMarginSettings(BaseModel):
    """User margin settings"""
    long_leverage: float = Field(alias="LongLeverage")
    short_leverage: float = Field(alias="ShortLeverage")
    margin_mode: str = Field(alias="MarginMode")

    class Config:
        populate_by_name = True

class UserPosition(BaseModel):
    """User position information"""
    position_id: str = Field(alias="PositionId")
    direction: str = Field(alias="Direction")
    market: str = Field(alias="CloudMarket")
    leverage: float = Field(alias="Leverage")
    margin_mode: str = Field(alias="MarginMode")
    price: float = Field(alias="Price")
    amount: float = Field(alias="Amount")
    margin: float = Field(alias="Margin")
    profit_loss: float = Field(alias="ProfitLoss")
    profit_loss_ratio: float = Field(alias="ProfitLossRatio")
    liquidation_price: float = Field(alias="LiquidationPrice")

    class Config:
        populate_by_name = True

class UserPositionContainer(BaseModel):
    """Container for user positions"""
    account_id: str = Field(alias="AccountId")
    items: List[Any] = Field(alias="Items")

    class Config:
        populate_by_name = True
