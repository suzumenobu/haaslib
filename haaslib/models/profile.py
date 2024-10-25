from typing import Any, Optional
from pydantic import BaseModel, Field

class ProfileDetailsReport(BaseModel):
    """Profile details report"""
    settings: Any = Field(alias="Settings")
    profits: Any = Field(alias="Profits")
    orders: Any = Field(alias="Orders")
    performance: Any = Field(alias="Performance")

    class Config:
        populate_by_name = True

class ProfilePerformanceReport(BaseModel):
    """Profile performance metrics"""
    sharpe_ratio: float = Field(alias="SharpeRatio")
    sortino_ratio: float = Field(alias="SortinoRatio")
    win_percentage: float = Field(alias="WinPercentage")
    profit_factor: float = Field(alias="ProfitFactor")
    cpc_index: float = Field(alias="CPCIndex")
    tail_ratio: float = Field(alias="TailRatio")
    common_sense_ratio: float = Field(alias="CommonSenseRatio")
    profit_margin_ratio: float = Field(alias="ProfitMarginRatio")

    class Config:
        populate_by_name = True

class ProfilePropertiesReport(BaseModel):
    """Profile properties report"""
    hide_trade_amount: bool = Field(alias="HideTradeAmount")
    hide_order_template: bool = Field(alias="HideOrderTemplate")
    is_spot_supported: bool = Field(alias="IsSpotSupported")
    is_margin_supported: bool = Field(alias="IsMarginSupported")
    is_leverage_supported: bool = Field(alias="IsLeverageSupported")
    is_managed_trading: bool = Field(alias="IsManagedTrading")
    is_one_direction: bool = Field(alias="IsOneDirection")
    is_multi_market: bool = Field(alias="IsMultiMarket")
    is_remote_signal_based: bool = Field(alias="IsRemoteSignalBased")
    is_ta_used: bool = Field(alias="IsTAUsed")

    class Config:
        populate_by_name = True
