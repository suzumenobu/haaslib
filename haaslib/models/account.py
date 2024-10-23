from typing import List, Any, Optional
from pydantic import BaseModel, Field

class AccountData(BaseModel):
    balances: List[Any] = Field(alias="Balances")
    orders: List[Any] = Field(alias="Orders")
    positions: List[Any] = Field(alias="Positions")
    trades: List[Any] = Field(alias="Trades")

    class Config:
        populate_by_name = True

class AccountBalance(BaseModel):
    account_id: str = Field(alias="AccountId")
    balance: float = Field(alias="Balance")
    currency: str = Field(alias="Currency")

    class Config:
        populate_by_name = True

class AccountList(BaseModel):
    root: List[AccountData]

    class Config:
        populate_by_name = True
