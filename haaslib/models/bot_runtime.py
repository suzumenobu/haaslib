from typing import Any
from pydantic import BaseModel, Field

class HaasBotAndRuntime(BaseModel):
    """Combined bot and runtime information"""
    bot: Any = Field(alias="Bot")
    runtime: Any = Field(alias="Runtime")

    class Config:
        populate_by_name = True

class RuntimeFailedOrder(BaseModel):
    """Failed order information"""
    pass  # Add specific failed order properties as needed

class RuntimeOrderBase(BaseModel):
    """Base order runtime information"""
    pass  # Add base order runtime properties as needed
