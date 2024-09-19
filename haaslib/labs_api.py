from typing import Any, List

from haaslib.api import SyncExecutor, Authenticated
from haaslib.model import UserLabRecord, UserLabDetails, BacktestResult, BacktestRuntime, BacktestChart, BacktestLog

class LabsAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def get_labs(self) -> List[UserLabRecord]:
        """
        Returns the saved labs records.

        This method retrieves all the lab records associated with the authenticated user.

        :return: A list of UserLabRecord objects representing the saved labs.
        :raises HaasApiError: If there's an error retrieving the lab records.
        """
        return self.executor.execute(
            endpoint="Labs",
            response_type=List[UserLabRecord],
            query_params={"channel": "GET_LABS"},
        )

    def create_lab(self, script_id: str, name: str, account_id: str, market: str, interval: int, style: str) -> UserLabDetails:
        """Creates a new lab record."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=UserLabDetails,
            query_params={
                "channel": "CREATE_LAB",
                "scriptid": script_id,
                "name": name,
                "accountid": account_id,
                "market": market,
                "interval": interval,
                "style": style,
            },
        )

    def clone_lab(self, lab_id: str) -> UserLabDetails:
        """Clones an existing lab record."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=UserLabDetails,
            query_params={
                "channel": "CLONE_LAB",
                "labid": lab_id,
            },
        )

    def delete_lab(self, lab_id: str) -> bool:
        """Deletes a specific lab record."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=bool,
            query_params={
                "channel": "DELETE_LAB",
                "labid": lab_id,
            },
        )

    def get_lab_details(self, lab_id: str) -> UserLabDetails:
        """Returns the details of a specific lab record."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=UserLabDetails,
            query_params={
                "channel": "GET_LAB_DETAILS",
                "labid": lab_id,
            },
        )

    def change_lab_script(self, lab_id: str, script_id: str) -> UserLabDetails:
        """Changes the script of the lab record."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=UserLabDetails,
            query_params={
                "channel": "CHANGE_LAB_SCRIPT",
                "labid": lab_id,
                "scriptid": script_id,
            },
        )

    def update_lab_details(self, lab_id: str, name: str, type: int, config: Any, settings: Any, parameters: Any) -> UserLabDetails:
        """Updates the lab's configuration."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=UserLabDetails,
            query_params={
                "channel": "UPDATE_LAB_DETAILS",
                "labid": lab_id,
                "name": name,
                "type": type,
                "config": config,
                "settings": settings,
                "parameters": parameters,
            },
        )

    def start_lab_execution(self, lab_id: str, start_unix: int, end_unix: int) -> UserLabDetails:
        """Starts the lab execution."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=UserLabDetails,
            query_params={
                "channel": "START_LAB_EXECUTION",
                "labid": lab_id,
                "startunix": start_unix,
                "endunix": end_unix,
            },
        )

    def cancel_lab_execution(self, lab_id: str) -> bool:
        """Cancels the lab execution."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=bool,
            query_params={
                "channel": "CANCEL_LAB_EXECUTION",
                "labid": lab_id,
            },
        )

    def get_lab_execution_update(self, lab_id: str) -> Any:
        """Gets an update on the lab execution."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=Any,  # Replace with a more specific type if known
            query_params={
                "channel": "GET_LAB_EXECUTION_UPDATE",
                "labid": lab_id,
            },
        )

    def get_backtest_result(self, lab_id: str, backtest_id: str) -> BacktestResult:
        """Gets a specific backtest result."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=BacktestResult,
            query_params={
                "channel": "GET_BACKTEST_RESULT",
                "labid": lab_id,
                "backtestid": backtest_id,
            },
        )

    def get_backtest_result_page(self, lab_id: str, next_page_id: int, page_length: int) -> List[BacktestResult]:
        """Gets a page of backtest results."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=List[BacktestResult],
            query_params={
                "channel": "GET_BACKTEST_RESULT_PAGE",
                "labid": lab_id,
                "nextpageid": next_page_id,
                "pagelength": page_length,
            },
        )

    def get_backtest_runtime(self, lab_id: str, backtest_id: str) -> BacktestRuntime:
        """Gets the runtime information for a specific backtest."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=BacktestRuntime,
            query_params={
                "channel": "GET_BACKTEST_RUNTIME",
                "labid": lab_id,
                "backtestid": backtest_id,
            },
        )

    def get_backtest_chart(self, lab_id: str, backtest_id: str) -> BacktestChart:
        """Gets the chart data for a specific backtest."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=BacktestChart,
            query_params={
                "channel": "GET_BACKTEST_CHART",
                "labid": lab_id,
                "backtestid": backtest_id,
            },
        )

    def get_backtest_log(self, lab_id: str, backtest_id: str) -> List[BacktestLog]:
        """Gets the log for a specific backtest."""
        return self.executor.execute(
            endpoint="Labs",
            response_type=List[BacktestLog],
            query_params={
                "channel": "GET_BACKTEST_LOG",
                "labid": lab_id,
                "backtestid": backtest_id,
            },
        )