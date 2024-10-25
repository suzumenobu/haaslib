from typing import Dict, Any
from pydantic import Field
from .base import BaseModel

class MarketInfo(BaseModel):
    market: str = Field(alias="CloudMarket")
    info: Dict[str, Any] = Field(alias="Info")
    
    class Config:
        populate_by_name = True

class MarketPriceInfo(BaseModel):
    market: str = Field(alias="CloudMarket")
    price_info: Dict[str, Any] = Field(alias="PriceInfo")
    
    class Config:
        populate_by_name = True

class MarketTechnicalInfo(BaseModel):
    market: str = Field(alias="CloudMarket")
    technical_info: Dict[str, Any] = Field(alias="TechnicalInfo")
    
    class Config:
        populate_by_name = True
