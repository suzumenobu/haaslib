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
    from pydantic import BaseModel, Field, ConfigDict
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
        pass
    
    T = TypeVar("T")

@dataclasses.dataclass
class UserAccount:
    uid: str = Field(alias="UID")  # User ID (email)
    aid: str = Field(alias="AID")  # Account ID (hash)
    name: str = Field(alias="N")   # Account name
    exchange_code: str = Field(alias="EC")  # Exchange code (e.g., BINANCEQUARTERLY)
    exchange_type: int = Field(alias="ET")  # Exchange type (numeric)
    status: int = Field(alias="S")  # Account status
    is_simulated: bool = Field(alias="IS")  # Is simulated account
    is_test: bool = Field(alias="IT")  # Is test account
    paper_account: bool = Field(alias="PA")  # Is paper trading account
    watchlist: bool = Field(alias="WL")  # Is watchlist
    position_mode: int = Field(alias="PM")  # Position mode
    margin_source: Optional[str] = Field(alias="MS")  # Margin source
    version: int = Field(alias="V")  # Version

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"

    @property
    def account_id(self) -> str:
        return self.aid

    @property
    def user_id(self) -> str:
        return self.uid

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
    symbol: str
    base_asset: str
    quote_asset: str
    price_source: str

    class Config:
        allow_population_by_field_name = True

class Market(BaseModel):
    symbol: str = Field(alias="S")
    base_asset: str = Field(alias="B")
    quote_asset: str = Field(alias="Q")
    price_source: str = Field(alias="P")

    class Config:
        populate_by_name = True

    @property
    def tag(self) -> str:
        return f"{self.price_source}:{self.symbol}"

@dataclasses.dataclass
class CreateBotRequest:
    bot_name: str
    script: Union[Script, HaasScriptItemWithDependencies]
    account_id: str
    market: CloudMarket
    leverage: int = dataclasses.field(default=0)
    interval: int = dataclasses.field(default=15)
    chartstyle: int = dataclasses.field(default=301)

class CreateLabRequest(BaseModel):
    script_id: str
    name: str
    account_id: str
    market: str
    interval: int
    default_price_data_style: PriceDataStyle

    @classmethod
    def from_market_tag(cls, script_id: str, account_id: str, market: MarketTag, interval: int, default_price_data_style: PriceDataStyle):
        name = f"{interval}_{market.tag}_{script_id}_{account_id}"
        return cls(
            script_id=script_id,
            account_id=account_id,
            market=market.tag,
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

class Account(BaseModel):
    uid: str = Field(alias="UID")
    aid: str = Field(alias="AID")
    name: str = Field(alias="N")
    exchange_code: str = Field(alias="EC")
    exchange_type: int = Field(alias="ET")
    status: int = Field(alias="S")
    is_simulated: bool = Field(alias="IS")
    is_test: bool = Field(alias="IT")
    paper_account: bool = Field(alias="PA")
    watchlist: bool = Field(alias="WL")
    position_mode: int = Field(alias="PM")
    margin_source: Optional[str] = Field(alias="MS")
    version: int = Field(alias="V")

class UserLabDetails(BaseModel):
    lab_id: str
    script_id: str
    name: str
    interval: int
    default_price_data_style: str
    market: str
    account_id: Optional[str]
    style: str
    parameters: Dict[str, Any]
    haas_script_settings: Dict[str, Any]
    user_lab_config: Dict[str, Any]
    algorithm: str

class UserAccount(BaseModel):
    aid: str
    uid: str
    name: str
    exchange: str
    status: int = Field(alias="S")
    is_simulated: bool = Field(alias="IS")
    is_test: bool = Field(alias="IT")
    paper_account: bool = Field(alias="PA")
    watchlist: bool = Field(alias="WL")
    position_mode: int = Field(alias="PM")
    margin_source: Optional[str] = Field(alias="MS")
    version: int = Field(alias="V")

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"

class AccountList(BaseModel):
    Data: List[UserAccount] = Field(default_factory=list)

from typing import List
from pydantic import BaseModel, Field
from .Phyton_automatically_generated.DataModel.MarketInformation import MarketInformation

class CloudMarket(BaseModel):
    symbol: str
    base_asset: str
    quote_asset: str
    price_source: str

    class Config:
        allow_population_by_field_name = True

class MarketList(BaseModel):
    root: List[MarketInformation] = Field(default_factory=list)
