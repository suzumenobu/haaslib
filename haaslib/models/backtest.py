from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field

class HaasScriptBacktestRecord(BaseModel):
    """Backtest record information"""
    RecordId: str
    Unix: int
    UserId: str
    BacktestId: str
    BacktestStart: int
    BacktestEnd: int
    BacktestTag: str
    ExecutionStart: int
    ExecutionEnd: int
    ScriptTag: str
    AccountTag: str
    MarketTag: str
    ProfitTags: List[Any]
    ROITags: List[Any]
    IsArchived: bool
    Runtime: Any
    Chart: Any
    Logs: List[Any]

class UserLabsBacktestResult(BaseModel):
    """Lab backtest result"""
    RecordId: str
    UserId: str
    LabId: str
    BacktestId: str
    NoGeneration: int
    NoPopulation: int
    Status: str
    Settings: Any
    Parameters: Any
    Runtime: Any
    Chart: Any
    Logs: List[Any]
    Summary: Any
    ServiceId: str
    IsElite: bool

class UserLabsBacktestSummary(BaseModel):
    """Summary of lab backtest results"""
    Orders: Any
    Trades: Any
    Positions: Any
    FeeCosts: float
    RealizedProfits: float
    ReturnOnInvestment: float
    CustomReport: Any

class BacktestSettings(BaseModel):
    script_id: str = Field(alias="ScriptId")
    script_type: str = Field(alias="ScriptType")
    settings: Dict[str, Any] = Field(alias="Settings")
    
    class Config:
        populate_by_name = True

class QuickTestRequest(BaseModel):
    backtest_id: str = Field(alias="BacktestId")
    script_id: str = Field(alias="ScriptId")
    settings: Dict[str, Any] = Field(alias="Settings")
    
    class Config:
        populate_by_name = True

class BacktestRequest(BaseModel):
    backtest_id: str = Field(alias="BacktestId")
    script_id: str = Field(alias="ScriptId")
    settings: Dict[str, Any] = Field(alias="Settings")
    start_unix: int = Field(alias="StartUnix")
    end_unix: int = Field(alias="EndUnix")
    
    class Config:
        populate_by_name = True

class BacktestLog(BaseModel):
    timestamp: int = Field(alias="Timestamp")
    message: str = Field(alias="Message")
    level: str = Field(alias="Level")
    
    class Config:
        populate_by_name = True

class BacktestInfo(BaseModel):
    backtest_id: str = Field(alias="BacktestId")
    tag: str = Field(alias="Tag")
    archived: bool = Field(alias="Archived")
    results: Dict[str, Any] = Field(alias="Results")
    logs: List[BacktestLog] = Field(alias="Logs", default_factory=list)
    
    class Config:
        populate_by_name = True
