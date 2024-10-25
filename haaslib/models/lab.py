from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class LabConfig(BaseModel):
    """Lab configuration settings"""
    max_population: int = Field(alias="MP")
    max_generations: int = Field(alias="MG")
    max_elites: int = Field(alias="ME")
    mix_rate: float = Field(alias="MR")
    adjust_rate: float = Field(alias="AR")

    class Config:
        from_attributes = True

class LabSettings(BaseModel):
    """Lab settings configuration"""
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

    class Config:
        populate_by_name = True

class CreateLabRequest(BaseModel):
    """Request to create a new lab"""
    script_id: str
    name: str
    account_id: str
    market: str
    interval: int
    default_price_data_style: str

class GetBacktestResultRequest(BaseModel):
    """Request to get backtest results"""
    lab_id: str

class StartLabExecutionRequest(BaseModel):
    """Request to start lab execution"""
    lab_id: str
    start_unix: Optional[int] = None
    end_unix: Optional[int] = None

class AddBotFromLabRequest(BaseModel):
    """Request to add bot from lab"""
    lab_id: str

class UserLabBacktestResult(BaseModel):
    """Backtest results"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class UserLabDetails(BaseModel):
    """Detailed lab information"""
    Config: Optional[LabConfig]
    Settings: Optional[LabSettings]
    Parameters: Dict[str, Any]
    UserId: str
    LabId: str
    ScriptId: str
    Name: str
    Type: str
    Status: str
    ScheduledBacktests: int
    CompletedBacktests: int
    CreatedAt: int
    UpdatedAt: int
    StartedAt: int
    RunningSince: int
    StartUnix: int
    EndUnix: int

    class Config:
        from_attributes = True

class UserLabRecord(BaseModel):
    """Lab record data"""
    lab_id: str = Field(alias="LabId")
    name: str = Field(alias="Name")
    script_id: str = Field(alias="ScriptId")
    account_id: str = Field(alias="AccountId")
    market: str = Field(alias="CloudMarket")
    status: str = Field(alias="Status")
    created_at: int = Field(alias="CreatedAt")
    updated_at: int = Field(alias="UpdatedAt")
    
    class Config:
        populate_by_name = True

class LabExecutionUpdate(BaseModel):
    """Lab execution status update"""
    status: str = Field(alias="Status")
    progress: float = Field(alias="Progress")
    message: Optional[str] = Field(alias="Message", default=None)
    error: Optional[str] = Field(alias="Error", default=None)
    completed_backtests: int = Field(alias="CompletedBacktests")
    total_backtests: int = Field(alias="TotalBacktests")
    
    class Config:
        populate_by_name = True

class BacktestResultPage(BaseModel):
    """Paginated backtest results"""
    results: List[UserLabBacktestResult]
    next_page_id: Optional[str] = Field(alias="NextPageId")
    has_more: bool = Field(alias="HasMore")

class BacktestRuntime(BaseModel):
    """Backtest runtime information"""
    execution_id: str = Field(alias="ExecutionId")
    status: str = Field(alias="Status")
    start_time: int = Field(alias="StartTime")
    end_time: int = Field(alias="EndTime")
    current_time: int = Field(alias="CurrentTime")
    positions: List[Dict[str, Any]] = Field(alias="Positions")
    orders: List[Dict[str, Any]] = Field(alias="Orders")
    trades: List[Dict[str, Any]] = Field(alias="Trades")
    performance: Dict[str, Any] = Field(alias="Performance")
    
    class Config:
        populate_by_name = True

class BacktestChart(BaseModel):
    """Backtest chart data"""
    candles: List[Dict[str, Any]] = Field(alias="Candles")
    indicators: List[Dict[str, Any]] = Field(alias="Indicators")
    trades: List[Dict[str, Any]] = Field(alias="Trades")
    signals: List[Dict[str, Any]] = Field(alias="Signals")
    
    class Config:
        populate_by_name = True

class BacktestLog(BaseModel):
    """Backtest execution log"""
    entries: List[Dict[str, Any]] = Field(alias="Entries")
    warnings: List[str] = Field(alias="Warnings")
    errors: List[str] = Field(alias="Errors")
    
    class Config:
        populate_by_name = True
