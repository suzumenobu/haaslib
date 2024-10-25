from typing import List, Dict, Any, Optional
from ..executor import RequestsExecutor, Authenticated
from ..models.base import ApiResponse
from ..models.backtest import (
    BacktestSettings, 
    QuickTestRequest,
    BacktestRequest, 
    BacktestInfo,
    BacktestLog
)
from ..exceptions import HaasApiError

def get_backtest_accounts(executor: RequestsExecutor[Authenticated]) -> List[str]:
    """Returns a list of accounts which can be used for backtesting goals"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="GET_BACKTEST_ACCOUNTS"
    )
    return response.data

def execute_debugtest(
    executor: RequestsExecutor[Authenticated],
    script_id: str,
    script_type: str,
    settings: Dict[str, Any]
) -> bool:
    """Does a debug run of the script"""
    settings = BacktestSettings(
        script_id=script_id,
        script_type=script_type,
        settings=settings
    )
    response = executor.execute(
        endpoint="BacktestAPI",
        command="EXECUTE_DEBUGTEST",
        params=settings.model_dump()
    )
    return response.success

def execute_backtest(
    executor: RequestsExecutor[Authenticated],
    request: BacktestRequest
) -> str:
    """Executes a backtest"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="EXECUTE_BACKTEST",
        params=request.model_dump(exclude_none=True)
    )
    return response.data

def get_backtest_history(
    executor: RequestsExecutor[Authenticated],
    next_page_id: str,
    page_length: int
) -> List[BacktestInfo]:
    """Returns a list of all stored backtest results"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="GET_BACKTEST_HISTORY",
        params={
            "nextpageid": next_page_id,
            "pagelength": page_length
        }
    )
    return [BacktestInfo(**item) for item in response.data]

def execute_quicktest(
    executor: RequestsExecutor,
    request: QuickTestRequest
) -> str:
    """Does a brief backtest"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="EXECUTE_QUICKTEST",
        params=request.model_dump()
    )
    return response.data

def cancel_backtest(
    executor: RequestsExecutor,
    backtest_id: str,
    service_id: str
) -> bool:
    """Cancels a running backtest"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="CANCEL_BACKTEST",
        params={
            "backtestid": backtest_id,
            "serviceid": service_id
        }
    )
    return response.success

def get_backtest_info(
    executor: RequestsExecutor,
    backtest_id: str
) -> BacktestInfo:
    """Returns the information of a backtest"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="GET_BACKTEST_INFO",
        params={"backtestid": backtest_id}
    )
    return BacktestInfo(**response.data)

def get_backtest_logs(
    executor: RequestsExecutor[Authenticated],
    backtest_id: str
) -> List[BacktestLog]:
    """Returns the backtest execution log"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="GET_BACKTEST_LOGS",
        params={"backtestid": backtest_id}
    )
    return [BacktestLog(**log) for log in response.data]

def archive_backtest(
    executor: RequestsExecutor[Authenticated],
    backtest_id: str,
    archive_result: bool
) -> bool:
    """Controls to archive a backtest result or not"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="ARCHIVE_BACKTEST",
        params={
            "backtestid": backtest_id,
            "archiveresult": archive_result
        }
    )
    return response.success

def edit_backtest_tag(
    executor: RequestsExecutor[Authenticated],
    backtest_id: str,
    backtest_tag: str
) -> bool:
    """Changes a backtest tag"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="EDIT_BACKTEST_TAG",
        params={
            "backtestid": backtest_id,
            "backtesttag": backtest_tag
        }
    )
    return response.success

def delete_backtest(
    executor: RequestsExecutor[Authenticated],
    backtest_id: str
) -> bool:
    """Delete/remove a backtest result"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="DELETE_BACKTEST",
        params={"backtestid": backtest_id}
    )
    return response.success

def delete_unarchived_backtest(
    executor: RequestsExecutor
) -> bool:
    """Deletes/removes all unarchived backtest results"""
    response = executor.execute(
        endpoint="BacktestAPI",
        command="DELETE_UNARCHIVED_BACKTEST"
    )
    return response.success

# ... implementing remaining functions from BacktestAPI.php lines 17-180
