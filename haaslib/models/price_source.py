from typing import Optional, List
from pydantic import BaseModel, Field
from .base import ApiResponse

class PriceSourceDetail(BaseModel):
    """Detailed price source information from the API"""
    full_name: str = Field(..., alias="F")
    friendly_name: str = Field(..., alias="FN")
    description: Optional[str] = Field(None, alias="D")
    enabled: bool = Field(..., alias="E")
    login_required: bool = Field(False, alias="LR")
    is_beta: bool = Field(False, alias="IBD")

    class Config:
        populate_by_name = True

class PriceSourceDetailResponse(ApiResponse):
    """Response wrapper for price source details"""
    Data: Optional[List[PriceSourceDetail]] = None
