from typing import List, Optional, Any
from ..executor import RequestsExecutor, Authenticated
from ..models.lab import (
    UserLabDetails,
    UserLabRecord,
    LabExecutionUpdate,
    BacktestChart,
    BacktestLog,
    BacktestRuntime,
    BacktestResultPage,
    UserLabBacktestResult
)
from ..exceptions import LabError

def get_labs(
    executor: RequestsExecutor[Authenticated]
) -> List[UserLabRecord]:
    """Returns the saved labs records"""
    response = executor.execute(
        endpoint="Labs",
        response_type=List[UserLabRecord],
        query_params={
            "channel": "GET_LABS"
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get labs: {response.Error}")
    return response.Data

def create_lab(
    executor: RequestsExecutor[Authenticated],
    script_id: str,
    name: str,
    account_id: str,
    market: str,  # Name of the market, like BINANCE_BTC_USDT_
    interval: int,
    style: str
) -> UserLabDetails:
    """Creates a new lab record"""
    response = executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "CREATE_LAB",
            "scriptId": script_id,
            "name": name,
            "accountId": account_id,
            "market": market,
            "interval": interval,
            "style": style
        }
    )
    if not response.Success:
        raise LabError(f"Failed to create lab: {response.Error}")
    return response.Data

def clone_lab(
    executor: RequestsExecutor[Authenticated],
    lab_id: str
) -> UserLabDetails:
    """Clones an existing lab record"""
    response = executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "CLONE_LAB",
            "labId": lab_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to clone lab: {response.Error}")
    return response.Data

def delete_lab(
    executor: RequestsExecutor[Authenticated],
    lab_id: str
) -> None:
    """Deletes a specific lab record"""
    response = executor.execute(
        endpoint="Labs",
        response_type=None,
        query_params={
            "channel": "DELETE_LAB",
            "labId": lab_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to delete lab: {response.Error}")

def get_lab_details(
    executor: RequestsExecutor[Authenticated],
    lab_id: str
) -> UserLabDetails:
    """Returns the details of a specific lab record"""
    response = executor.execute(
        endpoint="Labs",
        response_type=UserLabDetails,
        query_params={
            "channel": "GET_LAB_DETAILS",
            "labId": lab_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get lab details: {response.Error}")
    return response.Data

def change_lab_script(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    script_id: str
) -> None:
    """Changes the script of the lab record"""
    response = executor.execute(
        endpoint="Labs",
        response_type=None,
        query_params={
            "channel": "CHANGE_LAB_SCRIPT",
            "labId": lab_id,
            "scriptId": script_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to change lab script: {response.Error}")

def update_lab_config(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    name: str,
    type: str,
    config: Any,
    settings: Any,
    parameters: Any
) -> None:
    """Updates the labs configuration"""
    response = executor.execute(
        endpoint="Labs",
        response_type=None,
        query_params={
            "channel": "UPDATE_LAB_CONFIG",
            "labId": lab_id,
            "name": name,
            "type": type,
            "config": config,
            "settings": settings,
            "parameters": parameters
        }
    )
    if not response.Success:
        raise LabError(f"Failed to update lab config: {response.Error}")

def start_lab_execution(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    start_unix: int,
    end_unix: int
) -> None:
    """Starts the lab execution"""
    response = executor.execute(
        endpoint="Labs",
        response_type=None,
        query_params={
            "channel": "START_LAB_EXECUTION",
            "labId": lab_id,
            "startUnix": start_unix,
            "endUnix": end_unix
        }
    )
    if not response.Success:
        raise LabError(f"Failed to start lab execution: {response.Error}")

def cancel_lab_execution(
    executor: RequestsExecutor[Authenticated],
    lab_id: str
) -> bool:
    """Cancels lab execution"""
    response = executor.execute(
        endpoint="Labs",
        response_type=bool,
        query_params={
            "channel": "CANCEL_LAB_EXECUTION",
            "labId": lab_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to cancel lab execution: {response.Error}")
    return response.Data

def get_lab_execution_update(
    executor: RequestsExecutor[Authenticated],
    lab_id: str
) -> LabExecutionUpdate:
    """Gets lab execution status update"""
    response = executor.execute(
        endpoint="Labs",
        response_type=LabExecutionUpdate,
        query_params={
            "channel": "GET_LAB_EXECUTION_UPDATE",
            "labId": lab_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get lab execution update: {response.Error}")
    return response.Data

def get_backtest_result(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    backtest_id: str
) -> UserLabBacktestResult:
    """Gets a specific backtest result"""
    response = executor.execute(
        endpoint="Labs",
        response_type=UserLabBacktestResult,
        query_params={
            "channel": "GET_BACKTEST_RESULT",
            "labId": lab_id,
            "backtestId": backtest_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get backtest result: {response.Error}")
    return response.Data

def get_backtest_result_page(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    next_page_id: str,
    page_length: int
) -> BacktestResultPage:
    """Gets paginated backtest results"""
    response = executor.execute(
        endpoint="Labs",
        response_type=BacktestResultPage,
        query_params={
            "channel": "GET_BACKTEST_RESULT_PAGE",
            "labId": lab_id,
            "nextPageId": next_page_id,
            "pageLength": page_length
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get backtest result page: {response.Error}")
    return response.Data

def get_backtest_runtime(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    backtest_id: str
) -> BacktestRuntime:
    """Gets the backtest runtime information"""
    response = executor.execute(
        endpoint="Labs",
        response_type=BacktestRuntime,
        query_params={
            "channel": "GET_BACKTEST_RUNTIME",
            "labId": lab_id,
            "backtestId": backtest_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get backtest runtime: {response.Error}")
    return response.Data

def get_backtest_chart(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    backtest_id: str
) -> BacktestChart:
    """Gets the backtest chart data"""
    response = executor.execute(
        endpoint="Labs",
        response_type=BacktestChart,
        query_params={
            "channel": "GET_BACKTEST_CHART",
            "labId": lab_id,
            "backtestId": backtest_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get backtest chart: {response.Error}")
    return response.Data

def get_backtest_log(
    executor: RequestsExecutor[Authenticated],
    lab_id: str,
    backtest_id: str
) -> BacktestLog:
    """Gets the backtest execution log"""
    response = executor.execute(
        endpoint="Labs",
        response_type=BacktestLog,
        query_params={
            "channel": "GET_BACKTEST_LOG",
            "labId": lab_id,
            "backtestId": backtest_id
        }
    )
    if not response.Success:
        raise LabError(f"Failed to get backtest log: {response.Error}")
    return response.Data
