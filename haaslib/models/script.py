from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class HaasScriptItem(BaseModel):
    """Basic script information"""
    UserId: str
    ScriptId: str
    ScriptName: str
    ScriptDescription: str
    ScriptType: str
    ScriptStatus: str
    CommandName: str
    IsCommand: bool
    IsValid: bool
    CreatedUnix: int
    UpdatedUnix: int

class HaasScriptItemWithDependencies(HaasScriptItem):
    """Script information with dependencies"""
    Dependencies: List[str]
    CompileResult: Any

class HaasScriptRecord(BaseModel):
    """Complete script record"""
    SourceCode: str
    CompileResult: Any
    UserId: str
    ScriptId: str
    ScriptName: str
    ScriptDescription: str
    ScriptType: str
    ScriptStatus: str
    CommandName: str
    IsCommand: bool
    IsValid: bool
    CreatedUnix: int
    UpdatedUnix: int

class HaasScriptExecutionPackage(BaseModel):
    """Script execution package"""
    ScriptId: str
    ScriptName: str
    ScriptType: str
    IsCommand: bool
    CommandName: str
    SourceCode: str
    Commands: List[Any]

class HaasScriptSettings(BaseModel):
    """Script settings configuration"""
    BotId: str
    BotName: str
    AccountId: str
    CloudMarket: str
    PositionMode: str
    MarginMode: str
    Leverage: float
    TradeAmount: float
    Interval: int
    ChartStyle: str
    OrderTemplate: str
    ScriptParameters: Any

    class Config:
        from_attributes = True

class HaasScriptProfile(BaseModel):
    """Script profile information"""
    script_id: str = Field(alias="ScriptId")
    public_rating: float = Field(alias="PublicRating")
    details: Any = Field(alias="Details")
    script_name: str = Field(alias="ScriptName")
    script_description: str = Field(alias="ScriptDescription")
    user_id: str = Field(alias="UserId")
    user_name: str = Field(alias="UserName")
    script_status: str = Field(alias="ScriptStatus")

    class Config:
        populate_by_name = True

class HaasScriptBacktestRecord(BaseModel):
    """Script backtest record"""
    record_id: str = Field(alias="RecordId")
    unix: int = Field(alias="Unix")
    user_id: str = Field(alias="UserId")
    backtest_id: str = Field(alias="BacktestId")
    backtest_start: int = Field(alias="BacktestStart")
    backtest_end: int = Field(alias="BacktestEnd")
    backtest_tag: str = Field(alias="BacktestTag")
    execution_start: int = Field(alias="ExecutionStart")
    execution_end: int = Field(alias="ExecutionEnd")
    script_tag: str = Field(alias="ScriptTag")
    account_tag: str = Field(alias="AccountTag")
    market_tag: str = Field(alias="MarketTag")
    profit_tags: List[Any] = Field(alias="ProfitTags")
    roi_tags: List[Any] = Field(alias="ROITags")
    is_archived: bool = Field(alias="IsArchived")
    runtime: Any = Field(alias="Runtime")
    chart: Any = Field(alias="Chart")
    logs: List[Any] = Field(alias="Logs")

    class Config:
        populate_by_name = True

class ScriptConfig(BaseModel):
    """Script configuration"""
    script_id: str = Field(alias="ScriptId")
    name: str = Field(alias="Name")
    type: str = Field(alias="Type")
    version: str = Field(alias="Version")
    description: str = Field(alias="Description")
    parameters: Dict[str, Any] = Field(alias="Parameters")

    class Config:
        populate_by_name = True

class FiatConversion(BaseModel):
    """Dictionary of fiat currency conversion rates"""
    data: Dict[str, float]

    class Config:
        populate_by_name = True
