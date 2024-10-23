from typing import Any, Optional, List
from pydantic import BaseModel, Field

class LabConfig(BaseModel):
    max_population: int = Field(alias="MP")
    max_generations: int = Field(alias="MG")
    max_elites: int = Field(alias="ME")
    mix_rate: float = Field(alias="MR")
    adjust_rate: float = Field(alias="AR")

    class Config:
        populate_by_name = True

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

    class Config:
        populate_by_name = True

class CreateLabRequest(BaseModel):
    script_id: str
    name: str
    account_id: str
    market: str
    interval: int
    default_price_data_style: str

class GetBacktestResultRequest(BaseModel):
    lab_id: str
    start_unix: int
    end_unix: int

class StartLabExecutionRequest(BaseModel):
    lab_id: str
    start_unix: int
    end_unix: int

class UserLabBacktestResult(BaseModel):
    pass  # Add fields based on API response

class UserLabDetails(BaseModel):
    lab_id: str
    name: str
    status: str

class UserLabRecord(BaseModel):
    pass  # Add fields based on API response
