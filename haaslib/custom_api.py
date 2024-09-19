from typing import Any, Dict

from haaslib.api import SyncExecutor, Authenticated

class CustomAPI:
    def __init__(self, executor: SyncExecutor[Authenticated]):
        self.executor = executor

    def get_default_commands(self, driver_code: str, market_tag: str, orderbook: Any = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "channel": "GET_DEFAULT_COMMANDS",
            "drivercode": driver_code,
            "markettag": market_tag,
        }
        if orderbook is not None:
            params["orderbook"] = orderbook

        return self.executor.execute(
            endpoint="Custom",
            response_type=Dict[str, Any],
            query_params=params,
        )