from typing import Optional
from pydantic import BaseModel, Field

class LicenseProfile(BaseModel):
    MaxSimulatedAccounts: int = 0
    MaxBacktestMonths: int = 0
    HireSignalsEnabled: bool = False

    class Config:
        populate_by_name = True

class AuthenticatedSessionResponseData(BaseModel):
    UserId: str
    InterfaceKey: str

    class Config:
        populate_by_name = True
