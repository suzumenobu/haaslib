from typing import List, Any

from haaslib.api import SyncExecutor, Authenticated
from haaslib.model import BacktestAccount, BacktestResult, BacktestInfo, BacktestLog

class BacktestAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def get_backtest_accounts(self) -> List[BacktestAccount]:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=List[BacktestAccount],
            query_params={"channel": "GET_BACKTEST_ACCOUNTS"},
        )

    def execute_debugtest(self, script_id: str, script_type: int, settings: Any) -> Any:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "EXECUTE_DEBUGTEST",
                "scriptid": script_id,
                "scripttype": script_type,
                "settings": settings,
            },
        )

    def execute_quicktest(self, backtest_id: str, script_id: str, settings: Any) -> BacktestResult:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=BacktestResult,
            query_params={
                "channel": "EXECUTE_QUICKTEST",
                "backtestid": backtest_id,
                "scriptid": script_id,
                "settings": settings,
            },
        )

    def execute_backtest(self, backtest_id: str, script_id: str, settings: Any, start_unix: int, end_unix: int) -> BacktestResult:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=BacktestResult,
            query_params={
                "channel": "EXECUTE_BACKTEST",
                "backtestid": backtest_id,
                "scriptid": script_id,
                "settings": settings,
                "startunix": start_unix,
                "endunix": end_unix,
            },
        )

    def cancel_backtest(self, backtest_id: str, service_id: str) -> bool:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=bool,
            query_params={
                "channel": "CANCEL_BACKTEST",
                "backtestid": backtest_id,
                "serviceid": service_id,
            },
        )

    def get_backtest_history(self, next_page_id: int, page_length: int) -> List[BacktestInfo]:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=List[BacktestInfo],
            query_params={
                "channel": "GET_BACKTEST_HISTORY",
                "nextpageid": next_page_id,
                "pagelength": page_length,
            },
        )

    def get_backtest_info(self, backtest_id: str) -> BacktestInfo:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=BacktestInfo,
            query_params={
                "channel": "GET_BACKTEST_INFO",
                "backtestid": backtest_id,
            },
        )

    def get_backtest_logs(self, backtest_id: str) -> List[BacktestLog]:
        return self.executor.execute(
            endpoint="Backtest",
            response_type=List[BacktestLog],
            query_params={
                "channel": "GET_BACKTEST_LOGS",
                "backtestid": backtest_id,
            },
        )