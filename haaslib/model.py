from __future__ import annotations

import sys
import os
import dataclasses
import enum
from typing import Any, Generic, Literal, Optional, Type, TypeVar, List, Union, Dict

# Add the path to the Phyton_automatically_generated folder
current_dir = os.path.dirname(os.path.abspath(__file__))
auto_gen_path = os.path.join(current_dir, 'Phyton_automatically_generated')
sys.path.append(auto_gen_path)

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    from pydantic import BaseModel, Field
    print("Pydantic imported successfully")
except ImportError as e:
    print(f"Failed to import pydantic: {e}")
    print("Defining fallback BaseModel and Field")
    
    class BaseModel:
        pass
    
    def Field(*args, **kwargs):
        return None

from haaslib.domain import MarketTag, Script

# Import classes from Phyton_automatically_generated folder
try:
    from DataModel.HaasBot import HaasBot
    from DataModel.LicenseDetails import LicenseDetails
    from DataModel.UserLabDetails import UserLabDetails
    from DataModel.UserLabRecord import UserLabRecord
    from DataModel.UserAccount import UserAccount
    print("Successfully imported classes from Phyton_automatically_generated")
except ImportError as e:
    print(f"Failed to import classes from Phyton_automatically_generated: {e}")
    print("Using fallback class definitions")
    
    # Define fallback classes
    class HaasBot(BaseModel):
        pass
    
    class LicenseDetails(BaseModel):
        pass
    
    class UserLabDetails(BaseModel):
        pass
    
    class UserLabRecord(BaseModel):
        pass
    
    class UserAccount(BaseModel):
        UserId: str
        AccountId: str
        Name: str
        ExchangeCode: str
        ExchangeType: str
        Status: str
        IsSimulated: bool
        IsTestNet: bool
        IsPublic: bool
        PositionMode: str
        MarginSettings: Any

T = TypeVar("T")

@dataclasses.dataclass
class UserAccount:
    UserId: str
    AccountId: str
    Name: str
    ExchangeCode: str
    ExchangeType: str
    Status: str
    IsSimulated: bool
    IsTestNet: bool
    IsPublic: bool
    PositionMode: str
    MarginSettings: Any

class ApiResponse(BaseModel, Generic[T]):
    Success: bool
    Error: str
    Data: T

class AuthenticatedSessionResponseData(BaseModel):
    UserId: str
    Username: Optional[str]
    InterfaceSecret: str
    UserRights: int
    IsAffiliate: bool
    IsProductSeller: bool
    LicenseDetails: LicenseDetails
    SupportHash: Optional[str]

class AuthenticatedSessionResponse(BaseModel):
    R: int
    D: AuthenticatedSessionResponseData
    DID: str

class HaasScriptItemWithDependencies(BaseModel):
    dependencies: list[str] = Field(alias="D")
    user_id: str = Field(alias="UID")
    script_id: str = Field(alias="SID")
    script_name: str = Field(alias="SN")
    script_description: str = Field(alias="SD")
    script_type: int = Field(alias="ST")
    script_status: int = Field(alias="SS")
    command_name: str = Field(alias="CN")
    is_command: bool = Field(alias="IC")
    is_valid: bool = Field(alias="IV")
    created_unix: int = Field(alias="CU")
    updated_unix: int = Field(alias="UU")
    folder_id: int = Field(alias="FID")

    @property
    def id(self) -> str:
        return self.script_id

    @property
    def type(self) -> int:
        return self.script_type

class CloudMarket(BaseModel):
    category: str = Field(alias="C")
    price_source: str = Field(alias="PS")
    primary: str = Field(alias="P")
    secondary: str = Field(alias="S")

    def as_market_tag(self) -> MarketTag:
        return MarketTag(
            f"{self.price_source}_{self.primary}_{self.secondary}_{self.category}"
        )

@dataclasses.dataclass
class CreateBotRequest:
    bot_name: str
    script: Union[Script, HaasScriptItemWithDependencies]
    account_id: str
    market: CloudMarket
    leverage: int = dataclasses.field(default=0)
    interval: int = dataclasses.field(default=15)
    chartstyle: int = dataclasses.field(default=301)

PriceDataStyle = Literal[
    "CandleStick",
    "CandleStickHLC",
    "HeikinAshi",
    "OHLC",
    "HLC",
    "CloseLine",
    "Line",
    "Mountain",
]

@dataclasses.dataclass
class CreateLabRequest:
    script_id: str
    name: str
    account_id: str
    market: MarketTag
    interval: int
    default_price_data_style: PriceDataStyle

    @classmethod
    def with_generated_name(
        cls: Type[CreateLabRequest],
        script_id: str,
        account_id: str,
        market: MarketTag,
        interval: int,
        default_price_data_style: PriceDataStyle,
    ) -> CreateLabRequest:
        name = f"{interval}_{market.tag}_{script_id}_{account_id}"
        return cls(
            script_id=script_id,
            account_id=account_id,
            market=market,
            interval=interval,
            default_price_data_style=default_price_data_style,
            name=name,
        )

class GetBacktestResultRequest(BaseModel):
    lab_id: str
    next_page_id: int
    page_lenght: int

@dataclasses.dataclass
class AddBotFromLabRequest:
    lab_id: str
    backtest_id: str
    bot_name: str
    account_id: str
    market: CloudMarket
    leverage: int = 0

class StartLabExecutionRequest(BaseModel):
    lab_id: str
    start_unix: int
    end_unix: int
    send_email: bool

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T] = Field(alias="I")
    next_page_id: int = Field(alias="NP")

class UserLabBacktestResult(BaseModel):
    # Define the fields for UserLabBacktestResult here
    pass

# Add any other classes that are not imported from Phyton_automatically_generated

class LoginResponse(ApiResponse[AuthenticatedSessionResponse]):
    pass
