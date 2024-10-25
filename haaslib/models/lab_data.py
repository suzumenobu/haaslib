from typing import List, Dict
from typing_extensions import Any
from pydantic import BaseModel, Field

class UserLabConfig(BaseModel):
    """Lab configuration"""
    max_population: int = Field(alias="MaxPopulation")
    max_generations: int = Field(alias="MaxGenerations")
    max_elites: int = Field(alias="MaxElites")
    mix_rate: float = Field(alias="MixRate")
    adjust_rate: float = Field(alias="AdjustRate")

    class Config:
        populate_by_name = True

class UserLabsBacktestResult(BaseModel):
    """Lab backtest result"""
    record_id: str = Field(alias="RecordId")
    user_id: str = Field(alias="UserId")
    lab_id: str = Field(alias="LabId")
    backtest_id: str = Field(alias="BacktestId")
    no_generation: int = Field(alias="NoGeneration")
    no_population: int = Field(alias="NoPopulation")
    status: str = Field(alias="Status")
    settings: Any = Field(alias="Settings")
    parameters: Any = Field(alias="Parameters")
    runtime: Any = Field(alias="Runtime")
    chart: Any = Field(alias="Chart")
    logs: List[Any] = Field(alias="Logs")
    summary: Any = Field(alias="Summary")
    service_id: str = Field(alias="ServiceId")
    is_elite: bool = Field(alias="IsElite")

    class Config:
        populate_by_name = True

class UserLabsBacktestSummary(BaseModel):
    """Lab backtest summary"""
    orders: Any = Field(alias="Orders")
    trades: Any = Field(alias="Trades")
    positions: Any = Field(alias="Positions")
    fee_costs: float = Field(alias="FeeCosts")
    realized_profits: float = Field(alias="RealizedProfits")
    return_on_investment: float = Field(alias="ReturnOnInvestment")
    custom_report: Any = Field(alias="CustomReport")

    class Config:
        populate_by_name = True
