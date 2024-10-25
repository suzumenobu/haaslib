from typing import List, Optional
from pydantic import BaseModel, Field

class UserBalanceItem(BaseModel):
    """User balance information"""
    currency: str = Field(alias="Currency")
    wallet_id: str = Field(alias="WalletId")
    available: float = Field(alias="Available")
    total: float = Field(alias="Total")

    class Config:
        populate_by_name = True

class UserBalanceMutation(BaseModel):
    """User balance mutation record"""
    id: str = Field(alias="Id")
    user_id: str = Field(alias="UserId")
    account_id: str = Field(alias="AccountId")
    mutation_id: str = Field(alias="MutationId")
    wallet_id: str = Field(alias="WalletId")
    currency: str = Field(alias="Currency")
    timestamp: int = Field(alias="Timestamp")
    type: str = Field(alias="Type")
    amount: float = Field(alias="Amount")

    class Config:
        populate_by_name = True

class UserBalanceContainer(BaseModel):
    """Container for user balance items"""
    account_id: str = Field(alias="AccountId")
    items: List[Any] = Field(alias="Items")

    class Config:
        populate_by_name = True
