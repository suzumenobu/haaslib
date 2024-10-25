from typing import List, Optional
from pydantic import BaseModel

class UserAccount(BaseModel):
    """User account information"""
    account_id: str
    name: str
    description: Optional[str] = None
    enabled: bool = True
    is_demo: bool = False
    
    class Config:
        from_attributes = True

class AccountData(BaseModel):
    """Detailed account information"""
    account_id: str
    name: str
    description: Optional[str] = None
    enabled: bool = True
    is_demo: bool = False
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    additional_settings: Optional[dict] = None
    
    class Config:
        from_attributes = True

class AccountBalance(BaseModel):
    """Account balance information"""
    currency: str
    balance: float
    available: float
    reserved: float
    
    class Config:
        from_attributes = True

class AccountList(BaseModel):
    """List of user accounts"""
    root: List[UserAccount]
    
    class Config:
        from_attributes = True
