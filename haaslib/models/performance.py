from typing import List, Dict
from typing_extensions import Any
from pydantic import BaseModel, Field

class RuntimePerformanceReport(BaseModel):
    """Runtime performance metrics"""
    sharpe_ratio: float = Field(alias="SharpeRatio")
    sortino_ratio: float = Field(alias="SortinoRatio")
    win_percentage: float = Field(alias="WinPercentage")
    win_loss_percentage: float = Field(alias="WinLossPercentage")
    profit_factor: float = Field(alias="ProfitFactor")
    cpc_index: float = Field(alias="CPCIndex")
    tail_ratio: float = Field(alias="TailRatio")
    common_sense_ratio: float = Field(alias="CommonSenseRatio")
    outlier_win_ratio: float = Field(alias="OutlierWinRatio")
    outlier_loss_ratio: float = Field(alias="OutlierLossRatio")
    profit_margin_ratio: float = Field(alias="ProfitMarginRatio")
    biggest_win: float = Field(alias="BiggestWin")
    biggest_loss: float = Field(alias="BiggestLoss")
    highest_point_in_profit: float = Field(alias="HighestPointInProfit")
    lowest_point_in_profit: float = Field(alias="LowestPointInProfit")
    total_margin_used: float = Field(alias="TotalMarginUsed")
    is_set: bool = Field(alias="IsSet")
    peak: float = Field(alias="Peak")
    trough: float = Field(alias="Trough")
    max_draw_down: float = Field(alias="MaxDrawDown")

    class Config:
        populate_by_name = True
