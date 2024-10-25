from typing import Any, List, Optional
from pydantic import BaseModel, Field

class HaasChartContainer(BaseModel):
    """Chart container information"""
    guid: str = Field(alias="Guid")
    interval: str = Field(alias="Interval")
    status: str = Field(alias="Status")
    charts: List[Any] = Field(alias="Charts")
    colors: Any = Field(alias="Colors")

    class Config:
        populate_by_name = True

class HaasChartDataLine(BaseModel):
    """Chart data line configuration"""
    guid: str = Field(alias="Guid")
    name: str = Field(alias="Name")
    interval: str = Field(alias="Interval")
    visible: bool = Field(alias="Visible")
    behind: bool = Field(alias="Behind")
    ignore_on_axis: bool = Field(alias="IgnoreOnAxis")
    color: Any = Field(alias="Color")
    width: int = Field(alias="Width")
    type: str =
