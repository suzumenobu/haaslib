from pydantic import BaseModel, Field
from typing import List, Optional

class Market(BaseModel):
    """Market model matching the API's CloudMarket structure"""
    price_source: str = Field(alias='PS')
    base_currency: str = Field(alias='P')
    quote_currency: str = Field(alias='S')
    contract_name: str = Field(alias='C', default='')
    enabled: bool = Field(default=True)
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    @property
    def market_name(self) -> str:
        """Generate market name in format: PRICESOURCE_BASE_QUOTE"""
        return f"{self.price_source}_{self.base_currency}_{self.quote_currency}"
