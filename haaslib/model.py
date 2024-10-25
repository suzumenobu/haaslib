from __future__ import annotations

import sys
import os
from dataclasses import dataclass, field
from typing import Any, Generic, Literal, Optional, Type, TypeVar, List, Union, Dict

# Import pydantic first
try:
    from pydantic import BaseModel, Field, ConfigDict
    print("Pydantic imported successfully")
except ImportError as e:
    print(f"Failed to import pydantic: {e}")
    print("Defining fallback BaseModel and Field")
    
    class BaseModel:
        pass
    
    def Field(*args, **kwargs):
        return None

# Then define TypeVars using BaseModel
T = TypeVar('T')
ApiResponseData = TypeVar(
    'ApiResponseData',
    bound=Union[BaseModel, List[BaseModel], bool, str, Dict[str, Any]]
)

# Add the path to the Phyton_automatically_generated folder
current_dir = os.path.dirname(os.path.abspath(__file__))
auto_gen_path = os.path.join(current_dir, 'Phyton_automatically_generated')
sys.path.append(auto_gen_path)

# Base API Response
class ApiResponse(BaseModel, Generic[T]):
    Success: bool
    Error: Optional[str] = None
    Data: Optional[T] = None

    class Config:
        populate_by_name = True

ModelApiResponse = ApiResponse

# Account Models
class AccountData(BaseModel):
    balances: List[Any] = Field(alias="Balances")
    orders: List[Any] = Field(alias="Orders")
    positions: List[Any] = Field(alias="Positions")
    trades: List[Any] = Field(alias="Trades")

class AccountBalance(BaseModel):
    account_id: str = Field(alias="AccountId")
    balance: float = Field(alias="Balance")
    currency: str = Field(alias="Currency")

class AccountList(BaseModel):
    root: List[AccountData]

# CloudMarket Models
from .models.market import CloudMarket, MarketListResponse

# Lab Models
class LabConfig(BaseModel):
    max_population: int = Field(alias="MP")
    max_generations: int = Field(alias="MG")
    max_elites: int = Field(alias="ME")
    mix_rate: float = Field(alias="MR")
    adjust_rate: float = Field(alias="AR")

class LabSettings(BaseModel):
    bot_id: Optional[str] = Field(alias="botId")
    bot_name: Optional[str] = Field(alias="botName")
    account_id: Optional[str] = Field(alias="accountId")
    market_tag: Optional[str] = Field(alias="marketTag")
    position_mode: int = Field(alias="positionMode")
    margin_mode: int = Field(alias="marginMode")
    leverage: float = Field(alias="leverage")
    trade_amount: float = Field(alias="tradeAmount")
    interval: int = Field(alias="interval")
    chart_style: int = Field(alias="chartStyle")
    order_template: int = Field(alias="orderTemplate")
    script_parameters: Any = Field(alias="scriptParameters")

# Request Models
class CreateLabRequest(BaseModel):
    script_id: str
    name: str
    account_id: str
    market: str
    interval: int
    default_price_data_style: str

class GetBacktestResultRequest(BaseModel):
    lab_id: str

class StartLabExecutionRequest(BaseModel):
    lab_id: str

class AddBotFromLabRequest(BaseModel):
    lab_id: str

class CreateBotRequest(BaseModel):
    pass  # Add fields as needed

# Response Models
class UserLabBacktestResult(BaseModel):
    pass  # Add fields as needed

class UserLabDetails(BaseModel):
    lab_id: str
    status: int

class UserLabRecord(BaseModel):
    pass  # Add fields as needed

class HaasBot(BaseModel):
    pass  # Add fields as needed

class HaasScriptItemWithDependencies(BaseModel):
    script_id: str
    name: str

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int

# Import classes from Phyton_automatically_generated folder
try:
    from .Phyton_automatically_generated.DataModel.HaasBot import HaasBot
    from .Phyton_automatically_generated.DataModel.LicenseProfile import LicenseProfile  # Changed from LicenseDetails
    from .Phyton_automatically_generated.DataModel.UserLabDetails import UserLabDetails
    from .Phyton_automatically_generated.DataModel.UserLabRecord import UserLabRecord
    from .Phyton_automatically_generated.DataModel.UserAccount import UserAccount
    print("Successfully imported classes from Phyton_automatically_generated")
except ImportError as e:
    print(f"Failed to import classes from Phyton_automatically_generated: {e}")
    print("Using fallback class definitions")
    
    # Define fallback classes
    class HaasBot(BaseModel):
        pass
    
    class LicenseProfile(BaseModel):  # Changed from LicenseDetails
        LicenseName: str = ""
        ValidUntill: int = 0
        Rights: List[Any] = Field(default_factory=list)
        Enterprise: bool = False
        AllowedExchanges: List[Any] = Field(default_factory=list)
        MaxBots: int = 0
        MaxSimulatedAccounts: int = 0
        MaxRealAccounts: int = 0
        MaxDashboards: int = 0
        MaxBacktestMonths: int = 0
        RentedSignals: List[Any] = Field(default_factory=list)
        RentedStrategies: List[Any] = Field(default_factory=list)
        HireSignalsEnabled: bool = False
        HireStrategiesEnabled: bool = False
        HaasLabsEnabled: bool = False
        ResellSignalsEnabled: bool = False
        MarketDetailsEnabled: bool = False
        LocalAPIEnabled: bool = False
        ScriptedExchangesEnabled: bool = False
        MachinelearningEnabled: bool = False

# Update AuthenticatedSessionResponseData to use LicenseProfile
class AuthenticatedSessionResponseData(BaseModel):
    UserId: str
    Username: Optional[str]
    InterfaceSecret: str
    UserRights: int
    IsAffiliate: bool
    IsProductSeller: bool
    LicenseDetails: LicenseProfile  # Using LicenseProfile instead of LicenseDetails
    SupportHash: Optional[str]

# ... rest of your existing model classes ...

# Remove any duplicate ApiResponse definitions
# Remove @dataclass ApiResponse
# Remove class ApiResponse with __init__

# At the end of the file, ensure we're exporting the correct names
__all__ = [
    'ApiResponse',
    'ModelApiResponse',
    'AccountData',
    'AccountBalance',
    'AccountList',
    'CloudMarket',
    'MarketListResponse',
    'LabConfig',
    'LabSettings',
    'CreateLabRequest',
    'GetBacktestResultRequest',
    'StartLabExecutionRequest',
    'AddBotFromLabRequest',
    'CreateBotRequest',
    'UserLabBacktestResult',
    'UserLabDetails',
    'UserLabRecord',
    'HaasBot',
    'HaasScriptItemWithDependencies',
    'PaginatedResponse',
    'T',
    'ApiResponseData',
    'LicenseProfile',  # Changed from LicenseDetails
    'AuthenticatedSessionResponseData',
    # ... other exports ...
]
