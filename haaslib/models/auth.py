from typing import Any, Optional
from pydantic import BaseModel, Field

class AppLoginDetails(BaseModel):
    """Login details returned after successful authentication"""
    user_id: str = Field(alias="UserId")
    interface_secret: str = Field(alias="InterfaceSecret")
    license_details: Any = Field(alias="LicenseDetails")

    class Config:
        populate_by_name = True

class AppLoginResult(BaseModel):
    """Result of login attempt"""
    is_success: bool = Field(alias="IsSuccess")
    error: str = Field(alias="Error")
    details: Any = Field(alias="Details")

    class Config:
        populate_by_name = True

class AuthResponse(BaseModel):
    """Response from authentication endpoint"""
    Success: bool
    Error: Optional[str] = None
    Data: Optional[dict] = None

    class Config:
        populate_by_name = True
