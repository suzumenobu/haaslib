from __future__ import annotations
from typing import TypeVar, Generic, Optional, Union, List, Dict, Any
from pydantic import BaseModel

T = TypeVar('T')
ApiResponseData = TypeVar(
    'ApiResponseData',
    bound=Union[BaseModel, List[BaseModel], bool, str, Dict[str, Any]]
)

class ApiResponse(BaseModel, Generic[T]):
    """Base API response model"""
    Success: bool
    Error: Optional[str] = None
    Data: Optional[T] = None

    class Config:
        populate_by_name = True

ModelApiResponse = ApiResponse[Dict[str, Any]]

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
