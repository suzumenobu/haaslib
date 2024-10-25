from typing import List, Dict, TypeVar, Generic
from typing_extensions import Any
from pydantic import BaseModel, Field

T = TypeVar('T')

class ConcurrentDictionary(BaseModel, Generic[T]):
    """Thread-safe dictionary implementation"""
    item: T = Field(alias="Item")
    is_empty: bool = Field(alias="IsEmpty")
    keys: List[Any] = Field(alias="Keys")
    values: List[T] = Field(alias="Values")

    class Config:
        populate_by_name = True
