from typing import List
from pydantic import BaseModel, Field

class NumberStatistics(BaseModel):
    """Statistical calculations for numeric values"""
    min: float = Field(alias="Min")
    max: float = Field(alias="Max")
    avg: float = Field(alias="Avg")
    median: float = Field(alias="Median")
    values: List[float] = Field(alias="Values")

    class Config:
        populate_by_name = True
