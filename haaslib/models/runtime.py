from typing import Any, List, Optional
from pydantic import BaseModel, Field

class RuntimeReport(BaseModel):
    """Base runtime report containing account and market information"""
    AccountId: str
    Market: str
    AmountLabel: str
    MarginLabel: str
    ProfitLabel: str
    Fees: Any
    Profits: Any
    Orders: Any
    Positions: Any
    Performance: Any
    total_trades: int = Field(alias="TotalTrades")
    winning_trades: int = Field(alias="WinningTrades")
    losing_trades: int = Field(alias="LosingTrades")
    break_even_trades: int = Field(alias="BreakEvenTrades")
    total_profit: float = Field(alias="TotalProfit")
    total: Any

class RuntimeOrdersReport(BaseModel):
    """Report containing order execution statistics"""
    Filled: int
    PartiallyFilled: int
    Cancelled: int
    Failed: int
    Total: int
    AverageOpenTime: int
    LastCompletedOrder: Any
    ProfitableTrades: int
    LoosingTrades: int
    BiggestWin: float
    BiggestLoss: float
    total_orders: int = Field(alias="TotalOrders")
    filled_orders: int = Field(alias="FilledOrders")
    cancelled_orders: int = Field(alias="CancelledOrders")
    pending_orders: int = Field(alias="PendingOrders")

class RuntimePositionsReport(BaseModel):
    """Report containing position statistics"""
    ClosedPositions: int
    WinningPositions: int
    AverageProfits: float
    AveragePositionSize: float
    AveragePositionMargin: float
    TotalEnterMargin: float
    AverageWin: float
    BiggestWin: float
    TotalWin: float
    AverageLoss: float
    BiggestLoss: float
    TotalLoss: float
    ProfitHistory: List[Any]

class RuntimeProfitReport(BaseModel):
    """Report containing profit and balance information"""
    StartPrice: float
    StartBalance: float
    PriceChange: float
    BalanceChange: float
    GrossProfits: float
    RealizedProfits: float
    UnrealizedProfits: float
    ReturnOnInvestment: float
    RoiMargin: float
    CustomRoiMargin: float

class RuntimePerformanceReport(BaseModel):
    """Report containing trading performance metrics"""
    SharpeRatio: float
    SortinoRatio: float
    WinPercentage: float
    WinLossPercentage: float
    ProfitFactor: float
    CPCIndex: float
    TailRatio: float
    CommonSenseRatio: float
    OutlierWinRatio: float
    OutlierLossRatio: float
    ProfitMarginRatio: float
    BiggestWin: float
    BiggestLoss: float
    HighestPointInProfit: float
    LowestPointInProfit: float
    TotalMarginUsed: float
    IsSet: bool
    Peak: float
    Trough: float
    MaxDrawDown: float

class RuntimePosition(BaseModel):
    """Individual position information"""
    PositionGuid: str
    PositionId: str
    AccountId: str
    Market: str
    Leverage: float
    Direction: str
    MarketType: str
    ProfitLabel: str
    AmountLabel: str
    PriceDecimals: int
    AmountDecimals: int
    OpenTime: int
    CloseTime: int
    IsClosed: bool
    AveragePrice: float
    Total: float
    Available: float
    InOrder: float
    EnterOrders: List[Any]
    ExitOrders: List[Any]
    CurrentPrice: float
    FeeCosts: float
    RealizedProfits: float
    UnrealizedProfits: float
    ROI: float
    HighestPointInProfit: float
    LowestPointInProfit: float
    IsSet: bool
    Peak: float
    Trough: float
    MaxDrawDown: float
    position_type: str = Field(alias="PositionType")
    entry_price: float = Field(alias="EntryPrice")
    amount: float = Field(alias="Amount")
    leverage: float = Field(alias="Leverage")
    liquidation_price: Optional[float] = Field(alias="LiquidationPrice", default=None)
    unrealized_pnl: float = Field(alias="UnrealizedPnL")

class HaasScriptRuntime(BaseModel):
    """Complete runtime state for a Haas script"""
    CompilerErrors: List[Any]
    MainExecutor: Any
    ExecutionStack: List[Any]
    CurrentExecutor: Any
    CurrentTradeSignal: Any
    Reports: RuntimeReport
    CustomReport: Any
    ScriptNote: str
    OpenOrders: List[Any]
    FailedOrders: List[Any]
    OrderExecutionRequests: List[Any]
    OrderCancelRequests: List[Any]
    FinishedOrdersIds: List[str]
    FinishedPositionIds: List[str]
    ManagedLongPosition: Optional[RuntimePosition]
    ManagedShortPosition: Optional[RuntimePosition]
    UnmanagedPositions: List[RuntimePosition]
    DatabasePositions: List[RuntimePosition]
    FinishedPositions: List[RuntimePosition]
    CachedPositions: List[RuntimePosition]
    SplitOrderCount: int
    InputFields: List[Any]
    ScriptMemory: Any
    LocalMemory: Any
    RedisKeys: List[Any]
    SessionMemory: Any
    ButtonMemory: Any
    LogId: str
    LogCount: int
    ExecutionLog: List[Any]
    ExecutionToken: Any
    ScriptType: str
    IsCommandScript: bool
    UserId: str
    BotId: str
    BotName: str
    ScriptId: str
    ScriptName: str
    Activated: bool
    Paused: bool
    ActivatedSince: int
    DeactivatedSince: int
    AccountId: str
    AccountIds: List[str]
    PriceMarket: str
    BotMarketType: str
    Leverage: float
    MarginMode: str
    PositionMode: str
    TradeAmount: float
    OrderTemplate: Any
    DefaultInterval: str
    DefaultChartType: str
    HideTradeAmountSettings: bool
    HideOrderSettings: bool
    OrderPersistenceEnabled: bool
    OrderPersistenceLimit: int
    EnableHighSpeedUpdates: bool
    UpdateAfterCompletedOrder: bool
    IndicatorContainerLogs: List[Any]
    IsDoingInit: bool
    IsDoingDebug: bool
    IsDoingBacktest: bool
    IsDoingBacktestFinalize: bool
    IsDoingLabsBacktests: bool
    IsScriptOk: bool
    TradeAmountError: str
    ScriptTradeAmountError: str
    UpdateCounter: int
    IsSpotSupported: bool
    IsMarginSupported: bool
    IsLeverageSupported: bool
    IsManagedTrading: bool
    IsOneDirection: bool
    IsMultiMarket: bool
    IsRemoteSignalBased: bool
    IsTAUsed: bool
    Timestamp: int
    MinuteTimestamp: int
    LastUpdateTimestamp: int
    BacktestStartUnix: int
    BacktestEndUnix: int

    class Config:
        from_attributes = True

class RuntimeFeeReport(BaseModel):
    """Report containing fee information"""
    total_fees: float = Field(alias="TotalFees")
    maker_fees: float = Field(alias="MakerFees")
    taker_fees: float = Field(alias="TakerFees")
    funding_fees: Optional[float] = Field(alias="FundingFees", default=None)
    
    class Config:
        populate_by_name = True
