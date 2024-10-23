from typing import List, Optional
from pydantic import BaseModel, Field

class CloudMarket(BaseModel):
    """Market from cloud API"""
    id: str
    name: str
    price_source: str
    base_currency: str
    quote_currency: str
    enabled: bool
    description: Optional[str] = None

    class Config:
        populate_by_name = True

class MarketList(BaseModel):
    """Container for market list"""
    root: List[CloudMarket] = Field(default_factory=list)

    class Config:
        populate_by_name = True
