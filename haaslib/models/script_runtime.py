from typing import List
from typing_extensions import Any, Optional
from pydantic import BaseModel, Field

class RuntimeResetConfig(BaseModel):
    """Runtime reset configuration"""
    reset_logs: bool = Field(alias="ResetLogs")
    reset_reports: bool = Field(alias="ResetReports")
    reset_positions: bool = Field(alias="ResetPositions")
    reset_chart: bool = Field(alias="ResetChart")

    class Config:
        populate_by_name = True

class HaasCallback(BaseModel):
    """Callback configuration"""
    pass  # Add specific callback properties as needed

class HaasScriptRuntime(BaseModel):
    """Script runtime information"""
    compiler_errors: List[Any] = Field(alias="CompilerErrors")
    main_executor: Any = Field(alias="MainExecutor")
    execution_stack: List[Any] = Field(alias="ExecutionStack")
    current_executor: Any = Field(alias="CurrentExecutor")
    current_trade_signal: Any = Field(alias="CurrentTradeSignal")
    reports: Any = Field(alias="Reports")
    custom_report: Any = Field(alias="CustomReport")
    script_note: str = Field(alias="ScriptNote")
    open_orders: List[Any] = Field(alias="OpenOrders")
    failed_orders: List[Any] = Field(alias="FailedOrders")
    order_execution_requests: List[Any] = Field(alias="OrderExecutionRequests")
    order_cancel_requests: List[Any] = Field(alias="OrderCancelRequests")
    finished_orders_ids: List[str] = Field(alias="FinishedOrdersIds")
    finished_position_ids: List[str] = Field(alias="FinishedPositionIds")
    managed_long_position: Any = Field(alias="ManagedLongPosition")
    managed_short_position: Any = Field(alias="ManagedShortPosition")
    unmanaged_positions: List[Any] = Field(alias="UnmanagedPositions")
    database_positions: List[Any] = Field(alias="DatabasePositions")
    finished_positions: List[Any] = Field(alias="FinishedPositions")
    cached_positions: List[Any] = Field(alias="CachedPositions")
    split_order_count: int = Field(alias="SplitOrderCount")
    input_fields: List[Any] = Field(alias="InputFields")
    script_memory: Any = Field(alias="ScriptMemory")
    local_memory: Any = Field(alias="LocalMemory")
    redis_keys: List[Any] = Field(alias="RedisKeys")
    session_memory: Any = Field(alias="SessionMemory")
    button_memory: Any = Field(alias="ButtonMemory")
    log_id: str = Field(alias="LogId")
    log_count: int = Field(alias="LogCount")
    execution_log: List[Any] = Field(alias="ExecutionLog")
    execution_token: Any = Field(alias="ExecutionToken")
    script_type: str = Field(alias="ScriptType")
    is_command_script: bool = Field(alias="IsCommandScript")

    class Config:
        populate_by_name = True
