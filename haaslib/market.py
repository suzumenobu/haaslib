from typing import List, Optional
from pydantic import BaseModel

class CloudMarket(BaseModel):
    """Represents a market from the cloud API"""
    id: str
    name: str
    price_source: str
    base_currency: str
    quote_currency: str
    enabled: bool
    description: Optional[str] = None

class MarketList(BaseModel):
    """Container for list of markets"""
    root: List[CloudMarket]
